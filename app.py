import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os
from dotenv import load_dotenv
import yagmail

# Load environment variables
load_dotenv("mail.env")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

st.set_page_config(page_title="AgriTrial Insight Tool", layout="wide")
st.title("🌾 AgriTrial Insight Tool")
st.markdown("""
A decision-support tool for visualizing and validating root, biomass, and canopy data collected in field trials. Upload your trial data in `.csv`, `.xlsx`, or `.xls` format to begin.
""")

uploaded_file = st.file_uploader("Upload Trial Data File", type=["csv", "xlsx", "xls"])
df = None
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.session_state["df"] = df
        st.success("✅ Data successfully uploaded.")

        # Column validation
        required_columns = ["Biomass (g)", "Root Score (1-10)", "Emergence (%)", "Canopy Score (1-5)"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        extra_columns = [col for col in df.columns if col not in required_columns]

        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            st.stop()

        if extra_columns:
            st.info(f"Additional columns detected: {', '.join(extra_columns)}")

    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")

if "df" in st.session_state:
    df = st.session_state["df"]

    # Filters
    with st.sidebar:
        st.header("🔎 Filter Data")
        trial_types = st.multiselect("Trial Type", options=df["Trial Type"].unique() if "Trial Type" in df.columns else [])
        hybrids = st.multiselect("Hybrid", options=df["Hybrid"].unique() if "Hybrid" in df.columns else [])
        locations = st.multiselect("Location", options=df["Location"].unique() if "Location" in df.columns else [])

    filtered_df = df.copy()
    if trial_types:
        filtered_df = filtered_df[filtered_df["Trial Type"].isin(trial_types)]
    if hybrids:
        filtered_df = filtered_df[filtered_df["Hybrid"].isin(hybrids)]
    if locations:
        filtered_df = filtered_df[filtered_df["Location"].isin(locations)]

    st.dataframe(filtered_df)

    st.markdown("### 📝 Admin Notes")
    admin_notes = st.text_area("Enter notes or field observations:", height=100)

    st.markdown("### 📋 Export & Email Summary Report")
    recipient_email = st.text_input("Enter recipient email (optional):")

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "AgriTrial Summary Report", ln=True, align="C")
            self.ln(5)

        def chapter_title(self, title):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, title, ln=True)
            self.ln(2)

        def chapter_body(self, body):
            self.set_font("Arial", "", 10)
            self.multi_cell(0, 10, body)
            self.ln()

    def generate_pdf(dataframe, notes):
        pdf = PDF()
        pdf.add_page()

        pdf.chapter_title("Tool Purpose")
        pdf.chapter_body(
            "The AgriTrial Insight Tool enables agricultural scientists to upload, filter, and analyze hybrid trial data. "
            "It generates quick insights and formatted summaries to support research decisions and reporting."
        )

        if notes:
            pdf.chapter_title("Admin Notes")
            pdf.chapter_body(notes)

        pdf.chapter_title("Summary Statistics")
        try:
            avg_biomass = round(dataframe["Biomass (g)"].mean(), 2)
            avg_emergence = round(dataframe["Emergence (%)"].mean(), 2)
            avg_root = round(dataframe["Root Score (1-10)"].mean(), 2)
            canopy_avg = round(dataframe["Canopy Score (1-5)"].mean(), 2)

            summary_text = f"""Number of Records: {len(dataframe)}
Average Biomass: {avg_biomass} g
Average Emergence: {avg_emergence} %
Average Root Score: {avg_root}
Average Canopy Score: {canopy_avg}"""
        except:
            summary_text = "Summary stats could not be computed. Check column names or missing values."

        pdf.chapter_body(summary_text)

        pdf.chapter_title("Included Columns")
        for col in dataframe.columns:
            pdf.chapter_body(f"- {col}")

        file_path = "report_summary.pdf"
        pdf.output(file_path)
        return file_path

    # Show charts in app
    st.markdown("### 📊 Visual Insights")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Average Biomass by Hybrid**")
        try:
            biomass_plot = filtered_df.groupby("Hybrid")["Biomass (g)"].mean().sort_values()
            fig1, ax1 = plt.subplots()
            biomass_plot.plot(kind="barh", color="green", ax=ax1)
            ax1.set_xlabel("Average Biomass (g)")
            st.pyplot(fig1)
        except Exception as e:
            st.warning(f"Could not plot biomass chart: {e}")

    with col2:
        st.markdown("**Root Score vs Emergence**")
        try:
            fig2, ax2 = plt.subplots()
            sns.scatterplot(data=filtered_df, x="Root Score (1-10)", y="Emergence (%)", hue="Hybrid", ax=ax2)
            st.pyplot(fig2)
        except Exception as e:
            st.warning(f"Could not plot scatter chart: {e}")

    if st.button("📄 Generate PDF"):
        try:
            pdf_path = generate_pdf(filtered_df, admin_notes)
            st.success("✅ PDF generated successfully.")
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download PDF Report", f, file_name="AgriTrial_Report.pdf")

            if recipient_email:
                yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
                yag.send(
                    to=recipient_email,
                    subject="Your AgriTrial Summary Report",
                    contents="Attached is your AgriTrial report.",
                    attachments=pdf_path
                )
                st.success(f"📧 Report sent to {recipient_email}")
        except Exception as e:
            st.error(f"❌ Failed to send email or generate report: {e}")
