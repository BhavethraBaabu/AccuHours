import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Timesheet Discrepancy Finder", layout="centered")
st.title("🕵️ Timesheet Discrepancy Finder")
st.write("Upload client and company timesheet Excel files to find discrepancies in working hours.")

# Upload files
client_file = st.file_uploader("Upload Client Timesheet (Excel)", type=["xlsx"])
company_file = st.file_uploader("Upload Company Timesheet (Excel)", type=["xlsx"])

if client_file and company_file:
    try:
        # Read files
        client_df = pd.read_excel(client_file)
        company_df = pd.read_excel(company_file)

        # Merge on Employee ID and Date
        merged_df = pd.merge(
            client_df,
            company_df,
            on=["Employee ID", "Date"],
            suffixes=("_client", "_company")
        )

        # Calculate discrepancy
        merged_df["Hour Discrepancy"] = merged_df["Hours Worked_client"] - merged_df["Hours Worked_company"]

        # Filter discrepancies
        discrepancies = merged_df[merged_df["Hour Discrepancy"] != 0]

        if not discrepancies.empty:
            st.subheader("Discrepancy Report")
            st.dataframe(discrepancies)

            # Prepare Excel file in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                discrepancies.to_excel(writer, index=False)
            output.seek(0)

            # Download option
            st.download_button(
                label="📥 Download Discrepancy Report",
                data=output,
                file_name="discrepancy_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.success("✅ No discrepancies found! Working hours match.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
else:
    st.info("Please upload both Excel files to proceed.")
