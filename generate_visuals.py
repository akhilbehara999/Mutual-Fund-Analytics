import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import os
import warnings

warnings.filterwarnings('ignore')

# Bluestock Branding Colors
BLUESTOCK_BLUE = "#0047AB"
BLUESTOCK_LIGHT_BLUE = "#4169E1"
BLUESTOCK_GREY = "#333333"
BLUESTOCK_LIGHT_GREY = "#F5F5F5"
BLUESTOCK_ORANGE = "#FF8C00"
BLUESTOCK_GREEN = "#008000"

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.facecolor": BLUESTOCK_LIGHT_GREY,
    "figure.facecolor": "white",
    "text.color": BLUESTOCK_GREY,
    "axes.labelcolor": BLUESTOCK_GREY,
    "xtick.color": BLUESTOCK_GREY,
    "ytick.color": BLUESTOCK_GREY,
    "axes.edgecolor": "#CCCCCC",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

data_dir = "data/processed/"

# Load Data
fund_master = pd.read_csv(f"{data_dir}fund_master_clean.csv")
nav_history = pd.read_csv(f"{data_dir}nav_history_clean.csv")
scheme_perf = pd.read_csv(f"{data_dir}scheme_performance_clean.csv")
investor_txn = pd.read_csv(f"{data_dir}investor_transactions_clean.csv")
aum_house = pd.read_csv(f"{data_dir}aum_by_fund_house_clean.csv")
monthly_sip = pd.read_csv(f"{data_dir}monthly_sip_inflows_clean.csv")
cat_inflows = pd.read_csv(f"{data_dir}category_inflows_clean.csv")
benchmark_idx = pd.read_csv(f"{data_dir}benchmark_indices_clean.csv")

# Date Conversions
aum_house['date'] = pd.to_datetime(aum_house['date'])
monthly_sip['month'] = pd.to_datetime(monthly_sip['month'], format='%Y-%m')
benchmark_idx['date'] = pd.to_datetime(benchmark_idx['date'])
nav_history['date'] = pd.to_datetime(nav_history['date'])

# Page 1: Industry Overview
fig1 = plt.figure(figsize=(16, 9))
fig1.suptitle("Bluestock Mutual Fund Analytics: Industry Overview", fontsize=24, fontweight='bold', color=BLUESTOCK_BLUE)
gs = GridSpec(2, 4, figure=fig1, height_ratios=[1, 3])

# KPIs (Mockup style text)
ax_kpi1 = fig1.add_subplot(gs[0, 0])
ax_kpi1.text(0.5, 0.6, "Total AUM", ha='center', va='center', fontsize=14)
ax_kpi1.text(0.5, 0.3, "₹81.42L Cr", ha='center', va='center', fontsize=20, fontweight='bold', color=BLUESTOCK_BLUE)
ax_kpi1.axis('off')

ax_kpi2 = fig1.add_subplot(gs[0, 1])
ax_kpi2.text(0.5, 0.6, "SIP Inflows", ha='center', va='center', fontsize=14)
ax_kpi2.text(0.5, 0.3, "₹31.2K Cr", ha='center', va='center', fontsize=20, fontweight='bold', color=BLUESTOCK_BLUE)
ax_kpi2.axis('off')

ax_kpi3 = fig1.add_subplot(gs[0, 2])
ax_kpi3.text(0.5, 0.6, "Total Folios", ha='center', va='center', fontsize=14)
ax_kpi3.text(0.5, 0.3, "26.12 Cr", ha='center', va='center', fontsize=20, fontweight='bold', color=BLUESTOCK_BLUE)
ax_kpi3.axis('off')

ax_kpi4 = fig1.add_subplot(gs[0, 3])
ax_kpi4.text(0.5, 0.6, "Total Schemes", ha='center', va='center', fontsize=14)
ax_kpi4.text(0.5, 0.3, "1,908", ha='center', va='center', fontsize=20, fontweight='bold', color=BLUESTOCK_BLUE)
ax_kpi4.axis('off')

# Industry AUM Trend
ax_trend = fig1.add_subplot(gs[1, :2])
aum_trend = aum_house.groupby('date')['aum_crore'].sum().reset_index()
sns.lineplot(data=aum_trend, x='date', y='aum_crore', color=BLUESTOCK_ORANGE, ax=ax_trend, linewidth=2.5)
ax_trend.fill_between(aum_trend['date'], aum_trend['aum_crore'], color=BLUESTOCK_ORANGE, alpha=0.1)
ax_trend.set_title("Industry AUM Trend (2022-2025)", fontsize=16)
ax_trend.set_xlabel("Date")
ax_trend.set_ylabel("AUM (Crores)")
ax_trend.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.setp(ax_trend.xaxis.get_majorticklabels(), rotation=45)

# AUM by AMC
ax_amc = fig1.add_subplot(gs[1, 2:])
latest_aum_amc = aum_house[aum_house['date'] == aum_house['date'].max()].groupby('fund_house')['aum_crore'].sum().sort_values(ascending=False).head(10).reset_index()
sns.barplot(data=latest_aum_amc, x='aum_crore', y='fund_house', palette="Blues_r", ax=ax_amc)
ax_amc.set_title("Top 10 AMCs by AUM", fontsize=16)
ax_amc.set_xlabel("AUM (Crores)")
ax_amc.set_ylabel("")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig1.savefig("Page1_Industry_Overview.png", dpi=300)

# Page 2: Fund Performance
fig2 = plt.figure(figsize=(16, 9))
fig2.suptitle("Bluestock Mutual Fund Analytics: Fund Performance", fontsize=24, fontweight='bold', color=BLUESTOCK_BLUE)
gs2 = GridSpec(2, 2, figure=fig2, width_ratios=[1, 1], height_ratios=[1, 1])

# Risk vs Return Scatter Plot
ax_scatter = fig2.add_subplot(gs2[0, 0])
sns.scatterplot(data=scheme_perf, x='return_3yr_pct', y='std_dev_ann_pct', hue='category', size='aum_crore', sizes=(50, 1000), palette="viridis", alpha=0.7, ax=ax_scatter)
ax_scatter.set_title("Risk vs Return (3Y)", fontsize=16)
ax_scatter.set_xlabel("Return 3Y (%)")
ax_scatter.set_ylabel("Risk (Std Dev %)")
ax_scatter.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 8})

# Fund NAV vs Benchmark
ax_nav = fig2.add_subplot(gs2[1, :])
sample_fund = nav_history[nav_history['amfi_code'] == nav_history['amfi_code'].unique()[0]]
sample_fund = sample_fund.sort_values('date')
nifty50 = benchmark_idx[benchmark_idx['index_name'] == 'Nifty 50'].sort_values('date')

# Normalize to base 100
start_date = max(sample_fund['date'].min(), nifty50['date'].min())
sample_fund = sample_fund[sample_fund['date'] >= start_date]
nifty50 = nifty50[nifty50['date'] >= start_date]

if len(sample_fund) > 0 and len(nifty50) > 0:
    sample_fund['nav_norm'] = (sample_fund['nav'] / sample_fund['nav'].iloc[0]) * 100
    nifty50['nav_norm'] = (nifty50['close_value'] / nifty50['close_value'].iloc[0]) * 100

    sns.lineplot(data=sample_fund, x='date', y='nav_norm', label="Selected Fund", color=BLUESTOCK_BLUE, ax=ax_nav)
    sns.lineplot(data=nifty50, x='date', y='nav_norm', label="Nifty 50", color=BLUESTOCK_ORANGE, ax=ax_nav)

ax_nav.set_title("Fund NAV vs Benchmark (Base 100)", fontsize=16)
ax_nav.set_xlabel("Date")
ax_nav.set_ylabel("Normalized Value")

# Scorecard visual placeholder
ax_score = fig2.add_subplot(gs2[0, 1])
ax_score.axis('off')
table_data = scheme_perf[['scheme_name', 'return_3yr_pct', 'sharpe_ratio', 'alpha']].head(10).values
col_labels = ['Fund Name', '3Y Return', 'Sharpe', 'Alpha']
table = ax_score.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)
ax_score.set_title("Top Funds Scorecard", fontsize=16)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig2.savefig("Page2_Fund_Performance.png", dpi=300)

# Page 3: Investor Analytics
fig3 = plt.figure(figsize=(16, 9))
fig3.suptitle("Bluestock Mutual Fund Analytics: Investor Analytics", fontsize=24, fontweight='bold', color=BLUESTOCK_BLUE)
gs3 = GridSpec(2, 2, figure=fig3)

# Transaction Amount by State
ax_state = fig3.add_subplot(gs3[0, 0])
state_amt = investor_txn.groupby('state')['amount_inr'].sum().sort_values(ascending=False).head(10).reset_index()
sns.barplot(data=state_amt, y='state', x='amount_inr', palette="magma", ax=ax_state)
ax_state.set_title("Transaction Amount by Top States", fontsize=16)
ax_state.set_xlabel("Amount (INR)")
ax_state.set_ylabel("")

# Transaction Type Distribution (Donut)
ax_donut = fig3.add_subplot(gs3[0, 1])
type_dist = investor_txn['transaction_type'].value_counts()
ax_donut.pie(type_dist.values, labels=type_dist.index, autopct='%1.1f%%', colors=[BLUESTOCK_BLUE, BLUESTOCK_ORANGE, BLUESTOCK_GREEN], startangle=90, pctdistance=0.85)
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig3.gca().add_artist(centre_circle)
ax_donut.set_title("Transaction Type Distribution", fontsize=16)

# Age Group vs Avg SIP
ax_age = fig3.add_subplot(gs3[1, 0])
age_sip = investor_txn[investor_txn['transaction_type'] == 'SIP'].groupby('age_group')['amount_inr'].mean().reset_index()
sns.barplot(data=age_sip, x='age_group', y='amount_inr', color=BLUESTOCK_LIGHT_BLUE, ax=ax_age)
ax_age.set_title("Average SIP Amount by Age Group", fontsize=16)
ax_age.set_ylabel("Avg SIP Amount (INR)")

# Monthly Transaction Volume
ax_vol = fig3.add_subplot(gs3[1, 1])
investor_txn['txn_month'] = pd.to_datetime(investor_txn['transaction_date']).dt.to_period('M')
vol_trend = investor_txn.groupby('txn_month').size().reset_index(name='volume')
vol_trend['txn_month'] = vol_trend['txn_month'].dt.to_timestamp()
sns.lineplot(data=vol_trend, x='txn_month', y='volume', color=BLUESTOCK_BLUE, marker="o", ax=ax_vol)
ax_vol.set_title("Monthly Transaction Volume", fontsize=16)
ax_vol.set_xlabel("Month")
ax_vol.set_ylabel("Transactions")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig3.savefig("Page3_Investor_Analytics.png", dpi=300)

# Page 4: SIP & Market Trends
fig4 = plt.figure(figsize=(16, 9))
fig4.suptitle("Bluestock Mutual Fund Analytics: SIP & Market Trends", fontsize=24, fontweight='bold', color=BLUESTOCK_BLUE)
gs4 = GridSpec(2, 2, figure=fig4)

# Dual Axis
ax_dual1 = fig4.add_subplot(gs4[0, :])
ax_dual2 = ax_dual1.twinx()

nifty_monthly = nifty50.set_index('date').resample('ME')['close_value'].last().reset_index()
nifty_monthly['month_dt'] = nifty_monthly['date'].dt.to_period('M').dt.to_timestamp()
monthly_sip['month_dt'] = monthly_sip['month'].dt.to_period('M').dt.to_timestamp()

mrg = pd.merge(monthly_sip, nifty_monthly, on='month_dt', how='inner')

ax_dual1.bar(mrg['month_dt'], mrg['sip_inflow_crore'], width=20, color=BLUESTOCK_LIGHT_BLUE, label="SIP Inflow")
ax_dual2.plot(mrg['month_dt'], mrg['close_value'], color=BLUESTOCK_ORANGE, linewidth=2.5, label="Nifty 50")

ax_dual1.set_xlabel("Month")
ax_dual1.set_ylabel("SIP Inflow (Crores)", color=BLUESTOCK_LIGHT_BLUE)
ax_dual2.set_ylabel("Nifty 50 Level", color=BLUESTOCK_ORANGE)
ax_dual1.set_title("SIP Inflow vs Market Movement", fontsize=16)

# Heatmap
ax_heat = fig4.add_subplot(gs4[1, 0])
cat_inflows['month_dt'] = pd.to_datetime(cat_inflows['month'])
pivot_inflow = cat_inflows.pivot_table(index='category', columns=cat_inflows['month_dt'].dt.strftime('%Y-%m'), values='net_inflow_crore', aggfunc='sum')
sns.heatmap(pivot_inflow, cmap="RdYlGn", center=0, ax=ax_heat, cbar_kws={'label': 'Net Inflow (Cr)'})
ax_heat.set_title("Category Inflow Heatmap", fontsize=16)
ax_heat.set_xlabel("")
ax_heat.set_ylabel("")

# Top 5 Categories
ax_topcat = fig4.add_subplot(gs4[1, 1])
top_cats = cat_inflows.groupby('category')['net_inflow_crore'].sum().sort_values(ascending=False).head(5).reset_index()
sns.barplot(data=top_cats, x='net_inflow_crore', y='category', palette="Greens_r", ax=ax_topcat)
ax_topcat.set_title("Top 5 Categories by Net Inflow", fontsize=16)
ax_topcat.set_xlabel("Net Inflow (Crores)")
ax_topcat.set_ylabel("")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig4.savefig("Page4_SIP_Market_Trends.png", dpi=300)

print("All visual pages generated successfully.")
