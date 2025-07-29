# ⏱️ AccuHours

**AccuHours** is a lightweight, AI-assisted Streamlit web app that identifies discrepancies in employee timesheets by comparing two data sources — usually actual work hours vs. reported hours. It simplifies manual auditing, improves accuracy, and boosts operational transparency.

🔗 **Live App**: [accuhours-024.streamlit.app](https://accuhours-024.streamlit.app/)

---

## 🚀 Features

- ✅ Upload two Excel/CSV timesheet files
- 🔍 Automatically detects mismatched or missing hours
- 📊 Presents discrepancies in an easy-to-read table
- 💾 Download report of differences for auditing
- 🧠 Built using Python and Streamlit with data comparison logic

---

## 📁 How to Use

1. Open the [AccuHours App](https://accuhours-024.streamlit.app/)
2. Upload your **reference file** (actual or approved hours)
3. Upload your **target file** (reported hours)
4. View differences instantly
5. Download the discrepancy report (optional)

---

## ⚙️ Tech Stack

- **Frontend & Backend**: [Streamlit](https://streamlit.io/)
- **Data Processing**: `pandas`, `numpy`
- **Deployment**: Streamlit Cloud

---

## 📌 Use Cases

- Audit employee-reported timesheets
- Verify vendor-submitted work hours
- Cross-check project billing data
- Ensure timesheet compliance in teams

---



## 🛠️ Setup Locally (Optional)

```bash
git clone https://github.com/yourusername/accuhours.git
cd accuhours
pip install -r requirements.txt
streamlit run app.py
