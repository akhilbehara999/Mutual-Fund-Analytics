import pandas as pd
import numpy as np

data_dir = "data/processed/"

# Load data
fund_master = pd.read_csv(f"{data_dir}fund_master_clean.csv")
nav_history = pd.read_csv(f"{data_dir}nav_history_clean.csv")
scheme_perf = pd.read_csv(f"{data_dir}scheme_performance_clean.csv")
investor_txn = pd.read_csv(f"{data_dir}investor_transactions_clean.csv")
aum_house = pd.read_csv(f"{data_dir}aum_by_fund_house_clean.csv")
monthly_sip = pd.read_csv(f"{data_dir}monthly_sip_inflows_clean.csv")
cat_inflows = pd.read_csv(f"{data_dir}category_inflows_clean.csv")
benchmark_idx = pd.read_csv(f"{data_dir}benchmark_indices_clean.csv")

# Ensure datetime
aum_house['date'] = pd.to_datetime(aum_house['date'])
monthly_sip['month'] = pd.to_datetime(monthly_sip['month'], format='%Y-%m')

# Measures
# Total AUM: latest sum of aum_crore in aum_by_fund_house or scheme_performance
total_aum_cr = aum_house[aum_house['date'] == aum_house['date'].max()]['aum_crore'].sum()
total_aum_lakh_cr = total_aum_cr / 100000

# Total SIP Inflow: sum across the period or latest month?
# Requirement: Target values: ₹81L Cr AUM, ₹31K Cr SIP, 26.12 Cr Folios, 1,908 Schemes
# Let's match the target or get latest values
latest_sip = monthly_sip[monthly_sip['month'] == monthly_sip['month'].max()]
if len(latest_sip) > 0:
    total_sip_inflow_cr = latest_sip['sip_inflow_crore'].values[0]
else:
    total_sip_inflow_cr = monthly_sip['sip_inflow_crore'].sum()

# Folios (using industry_folio_count_clean if exists, otherwise transaction count?)
# Oh wait, we have target values, we should check if industry_folio_count_clean exists
import os
if os.path.exists(f"{data_dir}industry_folio_count_clean.csv"):
    folios_df = pd.read_csv(f"{data_dir}industry_folio_count_clean.csv")
    folios_df['month'] = pd.to_datetime(folios_df['month'])
    total_folios_cr = folios_df[folios_df['month'] == folios_df['month'].max()]['total_folios_crore'].values[0]
else:
    total_folios_cr = np.nan

# Total Schemes
total_schemes = aum_house[aum_house['date'] == aum_house['date'].max()]['num_schemes'].sum()

# Averages from scheme performance
avg_expense_ratio = scheme_perf['expense_ratio_pct'].mean()
avg_return_1y = scheme_perf['return_1yr_pct'].mean()
avg_risk = scheme_perf['std_dev_ann_pct'].mean()

# Latest NAV average
latest_nav = nav_history[nav_history['date'] == nav_history['date'].max()]
avg_nav = latest_nav['nav'].mean()

# Fund Count
fund_count = len(fund_master)

# Transaction Volume
txn_volume = len(investor_txn)

# Average SIP Amount
sip_txns = investor_txn[investor_txn['transaction_type'] == 'SIP']
avg_sip_amount = sip_txns['amount_inr'].mean()

# Net Category Inflow
net_cat_inflow = cat_inflows['net_inflow_crore'].sum()

# Benchmark Return (latest vs 1yr ago?)
benchmark_idx['date'] = pd.to_datetime(benchmark_idx['date'])
nifty50 = benchmark_idx[benchmark_idx['index_name'] == 'Nifty 50'].sort_values('date')
if len(nifty50) > 252:
    bench_start = nifty50.iloc[-252]['close_value']
    bench_end = nifty50.iloc[-1]['close_value']
    bench_return_1y = (bench_end / bench_start - 1) * 100
else:
    bench_return_1y = np.nan

with open("DAX_Measures.md", "w") as f:
    f.write("# DAX Measures & Calculated KPIs\n\n")
    f.write(f"- **Total AUM**: ₹{total_aum_lakh_cr:.2f}L Cr\n")
    f.write(f"- **Total SIP Inflow (Latest Month)**: ₹{total_sip_inflow_cr/1000:.2f}K Cr\n")
    f.write(f"- **Total Folios**: {total_folios_cr:.2f} Cr\n")
    f.write(f"- **Total Schemes**: {total_schemes:,.0f}\n")
    f.write(f"- **Average Expense Ratio**: {avg_expense_ratio:.2f}%\n")
    f.write(f"- **Average Return (1Y)**: {avg_return_1y:.2f}%\n")
    f.write(f"- **Average Risk (Std Dev)**: {avg_risk:.2f}%\n")
    f.write(f"- **Average NAV (Latest)**: ₹{avg_nav:.2f}\n")
    f.write(f"- **Fund Count (Tracked)**: {fund_count}\n")
    f.write(f"- **Transaction Volume**: {txn_volume:,}\n")
    f.write(f"- **Average SIP Amount**: ₹{avg_sip_amount:,.2f}\n")
    f.write(f"- **Net Category Inflow (Total)**: ₹{net_cat_inflow:,.2f} Cr\n")
    f.write(f"- **Benchmark Return (Nifty 50, 1Y)**: {bench_return_1y:.2f}%\n")

    f.write("\n## Measure Logic Equivalent (DAX Definitions)\n")
    f.write("```dax\n")
    f.write("Total AUM = SUM('AUM Data'[aum_crore])\n")
    f.write("Total SIP Inflow = CALCULATE(SUM('SIP Inflows'[sip_inflow_crore]), LASTDATE('SIP Inflows'[month]))\n")
    f.write("Total Folios = CALCULATE(SUM('Folio Data'[total_folios_crore]), LASTDATE('Folio Data'[month]))\n")
    f.write("Total Schemes = SUM('AUM Data'[num_schemes])\n")
    f.write("Average Expense Ratio = AVERAGE('Scheme Performance'[expense_ratio_pct])\n")
    f.write("Average Return = AVERAGE('Scheme Performance'[return_1yr_pct])\n")
    f.write("Average Risk = AVERAGE('Scheme Performance'[std_dev_ann_pct])\n")
    f.write("Average NAV = CALCULATE(AVERAGE('NAV History'[nav]), LASTDATE('NAV History'[date]))\n")
    f.write("Fund Count = DISTINCTCOUNT('Fund Master'[amfi_code])\n")
    f.write("Transaction Volume = COUNTROWS('Investor Transactions')\n")
    f.write("Average SIP Amount = CALCULATE(AVERAGE('Investor Transactions'[amount_inr]), 'Investor Transactions'[transaction_type] == \"SIP\")\n")
    f.write("Net Category Inflow = SUM('Category Inflows'[net_inflow_crore])\n")
    f.write("```\n")

print("Measures calculated and saved to DAX_Measures.md")
