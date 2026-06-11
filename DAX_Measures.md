# DAX Measures & Calculated KPIs

- **Total AUM**: ₹62.74L Cr
- **Total SIP Inflow (Latest Month)**: ₹31.00K Cr
- **Total Folios**: 26.12 Cr
- **Total Schemes**: 1,522
- **Average Expense Ratio**: 1.24%
- **Average Return (1Y)**: 14.38%
- **Average Risk (Std Dev)**: 14.96%
- **Average NAV (Latest)**: ₹357.61
- **Fund Count (Tracked)**: 40
- **Transaction Volume**: 32,778
- **Average SIP Amount**: ₹11,018.13
- **Net Category Inflow (Total)**: ₹932,239.00 Cr
- **Benchmark Return (Nifty 50, 1Y)**: nan%

## Measure Logic Equivalent (DAX Definitions)
```dax
Total AUM = SUM('AUM Data'[aum_crore])
Total SIP Inflow = CALCULATE(SUM('SIP Inflows'[sip_inflow_crore]), LASTDATE('SIP Inflows'[month]))
Total Folios = CALCULATE(SUM('Folio Data'[total_folios_crore]), LASTDATE('Folio Data'[month]))
Total Schemes = SUM('AUM Data'[num_schemes])
Average Expense Ratio = AVERAGE('Scheme Performance'[expense_ratio_pct])
Average Return = AVERAGE('Scheme Performance'[return_1yr_pct])
Average Risk = AVERAGE('Scheme Performance'[std_dev_ann_pct])
Average NAV = CALCULATE(AVERAGE('NAV History'[nav]), LASTDATE('NAV History'[date]))
Fund Count = DISTINCTCOUNT('Fund Master'[amfi_code])
Transaction Volume = COUNTROWS('Investor Transactions')
Average SIP Amount = CALCULATE(AVERAGE('Investor Transactions'[amount_inr]), 'Investor Transactions'[transaction_type] == "SIP")
Net Category Inflow = SUM('Category Inflows'[net_inflow_crore])
```
