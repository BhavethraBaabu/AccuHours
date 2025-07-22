import streamlit as st
import pandas as pd
from io import BytesIO
from sklearn.ensemble import IsolationForest
import numpy as np

# Page config
st.set_page_config(page_title="Timesheet Discrepancy Finder", layout="centered")
st.title("🕵️ Timesheet Discrepancy Finder + 🤖 Anomaly Detector")
st.write("Upload client and company timesheet Excel files to find working hour discrepancies and detect anomalies using ML.")

# File upload
client_file = st.file_uploader("📂 Upload Client Timesheet (Excel)", type=["xlsx"])
company_file = st.file_uploader("📂 Upload Company Timesheet (Excel)", type=["xlsx"])

if client_file and company_file:
    try:
        # Read Excel files
        client_df = pd.read_excel(client_file)
        company_df = pd.read_excel(company_file)

        st.subheader("🔄 Discrepancy Comparison")
        # Merge on Employee ID and Date
        merged_df = pd.merge(
            client_df,
            company_df,
            on=["Employee ID", "Date"],
            suffixes=("_client", "_company")
        )

        # Calculate discrepancy
        merged_df["Hour Discrepancy"] = merged_df["Hours Worked_client"] - merged_df["Hours Worked_company"]
        discrepancies = merged_df[merged_df["Hour Discrepancy"] != 0]

        if not discrepancies.empty:
            st.warning("⚠️ Discrepancies Found Between Timesheets")
            st.dataframe(discrepancies)

            # Export discrepancy report
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                discrepancies.to_excel(writer, index=False)
            output.seek(0)

            st.download_button(
                label="📥 Download Discrepancy Report",
                data=output,
                file_name="discrepancy_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.success("✅ No discrepancies found! Working hours match.")

        # Anomaly detection block
        st.markdown("---")
        st.subheader("🤖 Anomaly Detection on Company Timesheet")

        if st.button("🔍 Detect Anomalies"):
            try:
                anomaly_df = company_df.copy()
                anomaly_df['Date'] = pd.to_datetime(anomaly_df['Date'])

                # Optional: Focus only on weekdays
                anomaly_df = anomaly_df[anomaly_df['Date'].dt.weekday < 5]

                # Pivot table: Employee ID vs Date matrix
                pivot_df = anomaly_df.pivot_table(
                    index='Employee ID',
                    columns='Date',
                    values='Hours Worked',
                    fill_value=0
                )

                # Run Isolation Forest
                model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
                preds = model.fit_predict(pivot_df)

                pivot_df['Anomaly'] = preds
                anomalies = pivot_df[pivot_df['Anomaly'] == -1]

                if not anomalies.empty:
                    st.error("🚨 Anomalies Detected in Company Timesheet!")
                    st.dataframe(anomalies.drop(columns='Anomaly'))

                    # Export anomaly report
                    output_anomaly = BytesIO()
                    with pd.ExcelWriter(output_anomaly, engine='openpyxl') as writer:
                        anomalies.drop(columns='Anomaly').to_excel(writer)
                    output_anomaly.seek(0)

                    st.download_button(
                        label="📥 Download Anomaly Report",
                        data=output_anomaly,
                        file_name="anomaly_report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.success("✅ No anomalies found. Timesheet appears normal.")

            except Exception as e:
                st.error(f"❌ Error during anomaly detection: {str(e)}")

    except Exception as e:
        st.error(f"❌ File Processing Error: {str(e)}")

else:
    st.info("📌 Please upload both Excel files to begin.")
