import pandas as pd
import os
import glob
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def process_datasets():
    csv_files = glob.glob('data/raw/*.csv')

    # Check if there are other datasets (10 provided datasets as per instructions)
    # They should be copied to data/raw/
    # However we only have the NAV datasets we just downloaded.
    # Let's list what we have and process them

    if not csv_files:
        logging.warning("No CSV files found in data/raw/")
        return

    logging.info(f"Found {len(csv_files)} CSV files in data/raw/")

    anomalies = []

    # Process all CSVs
    for file in csv_files:
        logging.info(f"\n--- Processing {file} ---")
        try:
            df = pd.read_csv(file)
            logging.info(f"Shape: {df.shape}")
            logging.info(f"\nDtypes:\n{df.dtypes}")
            logging.info(f"\nHead:\n{df.head()}")

            # Missing values
            missing = df.isnull().sum()
            logging.info(f"\nMissing values:\n{missing}")

            # Duplicates
            duplicates = df.duplicated().sum()
            logging.info(f"\nDuplicate rows: {duplicates}")

            # Basic stats
            logging.info(f"\nBasic statistics:\n{df.describe(include='all')}")

            # Check for anomalies
            if duplicates > 0:
                anomalies.append(f"{file}: Found {duplicates} duplicate rows.")
            if missing.sum() > 0:
                anomalies.append(f"{file}: Found missing values: \n{missing[missing > 0]}")

        except Exception as e:
            logging.error(f"Error processing {file}: {e}")
            anomalies.append(f"{file}: Error reading file - {e}")

    # Print anomalies
    if anomalies:
        logging.info("\n--- Anomalies Found ---")
        for anomaly in anomalies:
            logging.info(anomaly)
    else:
        logging.info("\n--- No Anomalies Found in datasets ---")

def fund_master_analysis():
    # If fund_master is not yet present in data/raw, create a dummy or try to load it
    fund_master_path = 'data/raw/fund_master.csv'
    if not os.path.exists(fund_master_path):
        logging.warning(f"fund_master.csv not found at {fund_master_path}. Please place all required datasets in data/raw/")
        return None

    logging.info("\n--- Fund Master Analysis ---")
    try:
        df_master = pd.read_csv(fund_master_path)
        logging.info(f"Unique Fund Houses: {df_master['fund_house'].nunique()}")
        logging.info(f"List: {df_master['fund_house'].unique()}")

        logging.info(f"\nCategories: {df_master['category'].unique()}")
        logging.info(f"Sub-categories: {df_master['sub_category'].unique()}")

        logging.info(f"\nRisk Grades:\n{df_master['risk_grade'].value_counts()}")

        logging.info("\nAMFI Scheme Code Structure:")
        logging.info(f"Type: {df_master['scheme_code'].dtype}")
        logging.info(f"Min length: {df_master['scheme_code'].astype(str).str.len().min()}")
        logging.info(f"Max length: {df_master['scheme_code'].astype(str).str.len().max()}")
        return df_master
    except Exception as e:
        logging.error(f"Error in fund master analysis: {e}")
        return None

def data_quality_validation(df_master):
    if df_master is None:
        return

    nav_history_path = 'data/raw/nav_history.csv'
    if not os.path.exists(nav_history_path):
        logging.warning(f"nav_history.csv not found at {nav_history_path}")
        return

    logging.info("\n--- Data Quality Validation ---")
    try:
        df_nav = pd.read_csv(nav_history_path)

        master_codes = set(df_master['scheme_code'].unique())
        nav_codes = set(df_nav['scheme_code'].unique())

        missing_in_nav = master_codes - nav_codes
        missing_in_master = nav_codes - master_codes

        report = []
        report.append("Data Quality Validation Report")
        report.append("==============================")
        report.append(f"Total schemes in fund_master: {len(master_codes)}")
        report.append(f"Total schemes in nav_history: {len(nav_codes)}")

        if len(missing_in_nav) == 0:
            msg = "SUCCESS: Every scheme code in fund_master exists in nav_history."
            logging.info(msg)
            report.append(msg)
        else:
            msg = f"WARNING: {len(missing_in_nav)} scheme codes from fund_master are missing in nav_history."
            logging.info(msg)
            report.append(msg)

        if len(missing_in_master) > 0:
            msg = f"NOTE: {len(missing_in_master)} scheme codes from nav_history are missing in fund_master."
            logging.info(msg)
            report.append(msg)

        # Save report
        os.makedirs("reports", exist_ok=True)
        report_path = "reports/data_quality_summary.txt"
        with open(report_path, "w") as f:
            f.write("\n".join(report))
        logging.info(f"\nData quality report saved to {report_path}")

    except Exception as e:
        logging.error(f"Error in data quality validation: {e}")

def main():
    process_datasets()
    df_master = fund_master_analysis()
    data_quality_validation(df_master)

if __name__ == "__main__":
    main()
