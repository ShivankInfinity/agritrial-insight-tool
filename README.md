# agritrial-insight-tool
A data visualization and reporting app for agricultural field trial analysis.
## Demo Instructions

- Upload `sample_data.csv` to try the AgriTrial Insight Tool instantly, no setup required!


# AgriTrial Insight Tool

A data visualization and reporting app for agricultural field trial analysis.

## Features

- Upload field trial data (.csv, .xlsx, .xls)
- Filter and analyze by trial type, hybrid, or location
- Visual graphs for quick insights
- PDF report export (with summary and charts)
- Email report delivery

## Setup

1. Clone/download the repo
2. Run `pip install -r requirements.txt`
3. Rename `mail.env.example` to `mail.env` and fill with your email/app password (Gmail app password recommended)
4. Start the app: `streamlit run app.py`

## Sample Data

Try the app using the included `sample_data.csv`.

## Security

Never commit your real `mail.env` with passwords to the repo.

## How to set up email sending

1. Copy `Sample mail.env` to a new file called `mail.env`
2. Fill in your email and app password.
   - Example:
     ```
     EMAIL_USER=your_email@gmail.com
     EMAIL_PASS=your_app_password
     ```
3. **Never share your real `mail.env` or app password publicly.**

(See README demo block from earlier message for full getting started steps.)

---

**You’re 100% ready to share this app as a safe, open-source tool.**  
If you want deployment help (Streamlit Cloud, Heroku, etc), just ask!  
If you want a custom README, I can make it now.

## Contact

For help, open an issue or contact the developer.
