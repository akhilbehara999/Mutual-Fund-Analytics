# Phase 1: Data Discovery & Validation

## Dataset Inventory
### fund_master_clean.csv
- Row count: 40
- Column count: 15
- Data types:
  - `amfi_code`: int64
  - `fund_house`: str
  - `scheme_name`: str
  - `category`: str
  - `sub_category`: str
  - `plan`: str
  - `launch_date`: str
  - `benchmark`: str
  - `expense_ratio_pct`: float64
  - `exit_load_pct`: float64
  - `min_sip_amount`: int64
  - `min_lumpsum_amount`: int64
  - `fund_manager`: str
  - `risk_category`: str
  - `sebi_category_code`: str
- No missing values.

### nav_history_clean.csv
- Row count: 46000
- Column count: 3
- Data types:
  - `amfi_code`: int64
  - `date`: str
  - `nav`: float64
- No missing values.

### benchmark_indices_clean.csv
- Row count: 8050
- Column count: 3
- Data types:
  - `date`: str
  - `index_name`: str
  - `close_value`: float64
- No missing values.

### scheme_performance_clean.csv
- Row count: 40
- Column count: 20
- Data types:
  - `amfi_code`: int64
  - `scheme_name`: str
  - `fund_house`: str
  - `category`: str
  - `plan`: str
  - `return_1yr_pct`: float64
  - `return_3yr_pct`: float64
  - `return_5yr_pct`: float64
  - `benchmark_3yr_pct`: float64
  - `alpha`: float64
  - `beta`: float64
  - `sharpe_ratio`: float64
  - `sortino_ratio`: float64
  - `std_dev_ann_pct`: float64
  - `max_drawdown_pct`: float64
  - `aum_crore`: int64
  - `expense_ratio_pct`: float64
  - `morningstar_rating`: int64
  - `risk_grade`: str
  - `expense_ratio_anomaly_flag`: bool
- No missing values.

### investor_transactions_clean.csv
- Row count: 32778
- Column count: 13
- Data types:
  - `investor_id`: str
  - `transaction_date`: str
  - `amfi_code`: int64
  - `transaction_type`: str
  - `amount_inr`: int64
  - `state`: str
  - `city`: str
  - `city_tier`: str
  - `age_group`: str
  - `gender`: str
  - `annual_income_lakh`: float64
  - `payment_mode`: str
  - `kyc_status`: str
- No missing values.

### aum_by_fund_house_clean.csv
- Row count: 90
- Column count: 5
- Data types:
  - `date`: str
  - `fund_house`: str
  - `aum_lakh_crore`: float64
  - `aum_crore`: int64
  - `num_schemes`: int64
- No missing values.

### monthly_sip_inflows_clean.csv
- Row count: 48
- Column count: 6
- Data types:
  - `month`: str
  - `sip_inflow_crore`: int64
  - `active_sip_accounts_crore`: float64
  - `new_sip_accounts_lakh`: float64
  - `sip_aum_lakh_crore`: float64
  - `yoy_growth_pct`: float64
- Missing values:
  - `yoy_growth_pct`: 12 (25.00%)

### category_inflows_clean.csv
- Row count: 144
- Column count: 3
- Data types:
  - `month`: str
  - `category`: str
  - `net_inflow_crore`: float64
- No missing values.

## Missing Datasets
None. All expected datasets are present.

## Relationship Validation
Checked relationships based on primary keys:
- `fund_master` -> `nav_history`: all `nav_history` amfi_codes in `fund_master`? True
- `fund_master` -> `scheme_performance`: all `scheme_performance` amfi_codes in `fund_master`? True
- `fund_master` -> `investor_transactions`: all `investor_transactions` amfi_codes in `fund_master`? True
