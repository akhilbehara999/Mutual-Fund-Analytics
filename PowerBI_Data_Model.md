# Power BI Data Model

## Relationships
The analytical dashboard relies on the following schema relationships:

1. `fund_master[amfi_code]` (1) <---> (*) `nav_history[amfi_code]`
2. `fund_master[amfi_code]` (1) <---> (*) `scheme_performance[amfi_code]`
3. `fund_master[amfi_code]` (1) <---> (*) `investor_transactions[amfi_code]`
4. `benchmark_indices[date]` (1) <---> (*) `nav_history[date]` (Date dimension logic)
5. `monthly_sip_inflows[month]` (1) <---> (*) `benchmark_indices[date]` (Linked via Date table)

## Validations Performed
- **No Ambiguous Relationships**: Star schema strictly enforced.
- **No Circular Dependencies**: Unidirectional filtering from Dimensions to Facts.
- **Primary Keys Verified**: `amfi_code` in `fund_master` is strictly unique.
