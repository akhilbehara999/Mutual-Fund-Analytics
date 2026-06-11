import pandas as pd
import os

expected_datasets = [
    "fund_master_clean.csv",
    "nav_history_clean.csv",
    "benchmark_indices_clean.csv",
    "scheme_performance_clean.csv",
    "investor_transactions_clean.csv",
    "aum_by_fund_house_clean.csv",
    "monthly_sip_inflows_clean.csv",
    "category_inflows_clean.csv"
]

data_dir = "data/processed/"
missing_datasets = []

with open("Data_Discovery_Validation.md", "w") as f:
    f.write("# Phase 1: Data Discovery & Validation\n\n")
    f.write("## Dataset Inventory\n")
    for file in expected_datasets:
        path = os.path.join(data_dir, file)
        if os.path.exists(path):
            df = pd.read_csv(path)
            f.write(f"### {file}\n")
            f.write(f"- Row count: {len(df)}\n")
            f.write(f"- Column count: {len(df.columns)}\n")
            f.write("- Data types:\n")
            for col, dtype in df.dtypes.items():
                f.write(f"  - `{col}`: {dtype}\n")

            missing = df.isnull().sum()
            if missing.sum() > 0:
                f.write("- Missing values:\n")
                for col, count in missing.items():
                    if count > 0:
                        f.write(f"  - `{col}`: {count} ({count/len(df)*100:.2f}%)\n")
            else:
                f.write("- No missing values.\n")
            f.write("\n")
        else:
            missing_datasets.append(file)

    f.write("## Missing Datasets\n")
    if missing_datasets:
        for ds in missing_datasets:
            f.write(f"- {ds}\n")
    else:
        f.write("None. All expected datasets are present.\n")

    f.write("\n## Relationship Validation\n")
    f.write("Checked relationships based on primary keys:\n")

    # Load for validation
    fund_master = pd.read_csv(os.path.join(data_dir, "fund_master_clean.csv"))
    nav_history = pd.read_csv(os.path.join(data_dir, "nav_history_clean.csv"))
    scheme_perf = pd.read_csv(os.path.join(data_dir, "scheme_performance_clean.csv"))
    investor_txn = pd.read_csv(os.path.join(data_dir, "investor_transactions_clean.csv"))

    # Check amfi_code relationship
    fund_codes = set(fund_master['amfi_code'])
    nav_codes = set(nav_history['amfi_code'])
    perf_codes = set(scheme_perf['amfi_code'])
    txn_codes = set(investor_txn['amfi_code'])

    f.write(f"- `fund_master` -> `nav_history`: all `nav_history` amfi_codes in `fund_master`? {nav_codes.issubset(fund_codes)}\n")
    f.write(f"- `fund_master` -> `scheme_performance`: all `scheme_performance` amfi_codes in `fund_master`? {perf_codes.issubset(fund_codes)}\n")
    f.write(f"- `fund_master` -> `investor_transactions`: all `investor_transactions` amfi_codes in `fund_master`? {txn_codes.issubset(fund_codes)}\n")

print("Validation complete. Check Data_Discovery_Validation.md")
