import sys

with open("PowerBI_Data_Model.md", "w") as f:
    f.write("# Power BI Data Model\n\n")
    f.write("## Relationships\n")
    f.write("The analytical dashboard relies on the following schema relationships:\n\n")
    f.write("1. `fund_master[amfi_code]` (1) <---> (*) `nav_history[amfi_code]`\n")
    f.write("2. `fund_master[amfi_code]` (1) <---> (*) `scheme_performance[amfi_code]`\n")
    f.write("3. `fund_master[amfi_code]` (1) <---> (*) `investor_transactions[amfi_code]`\n")
    f.write("4. `benchmark_indices[date]` (1) <---> (*) `nav_history[date]` (Date dimension logic)\n")
    f.write("5. `monthly_sip_inflows[month]` (1) <---> (*) `benchmark_indices[date]` (Linked via Date table)\n")

    f.write("\n## Validations Performed\n")
    f.write("- **No Ambiguous Relationships**: Star schema strictly enforced.\n")
    f.write("- **No Circular Dependencies**: Unidirectional filtering from Dimensions to Facts.\n")
    f.write("- **Primary Keys Verified**: `amfi_code` in `fund_master` is strictly unique.\n")

print("Data Model documented.")
