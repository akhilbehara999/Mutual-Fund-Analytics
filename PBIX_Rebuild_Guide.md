# PBIX Rebuild Guide

**Important Note:** A genuine `.pbix` (Power BI Desktop) file cannot be generated programmatically in a headless Linux environment. The requested dashboard artifacts have been rendered via Python to match the analytical requirements.

To rebuild this dashboard directly within Power BI Desktop, follow these steps:

## 1. Import Data
1. Open Power BI Desktop.
2. Go to **Home > Get Data > Text/CSV**.
3. Import all files from the `data/processed/` directory.

## 2. Establish Data Model
Recreate the star schema in the **Model View** as documented in `PowerBI_Data_Model.md`.
Ensure:
- 1-to-many relationships from Dimensions to Facts.
- Cross-filter direction is set to "Single".

## 3. Create Measures
Navigate to the **Data View** or **Report View**, create a new measure table, and input the DAX formulas provided in `DAX_Measures.md`.

## 4. Build Visuals (Page by Page)
1. **Industry Overview:** Use KPI cards and Line/Bar charts. Apply Bluestock branding colors.
2. **Fund Performance:** Use a Scatter chart (Risk vs Return) and a Matrix visual for the Scorecard. Use conditional formatting for scores.
3. **Investor Analytics:** Use Donut, Bar, and Line charts. Enable cross-filtering across state, age, and transaction type.
4. **SIP & Market Trends:** Use the "Line and clustered column chart" visual to combine SIP inflows (bars) and Nifty 50 (line).

## 5. Add Interactivity
1. Add slicers for `fund_house`, `category`, and `state`.
2. Configure **Drill-through** on the Fund Scorecard matrix to jump to a specific fund detail page.
3. Add a **Reset Bookmark** button to clear all active slicers.
