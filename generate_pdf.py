from fpdf import FPDF
import os

pdf = FPDF(orientation='L', unit='mm', format='A4')
pages = [
    "Page1_Industry_Overview.png",
    "Page2_Fund_Performance.png",
    "Page3_Investor_Analytics.png",
    "Page4_SIP_Market_Trends.png"
]

for page in pages:
    if os.path.exists(page):
        pdf.add_page()
        # A4 Landscape is 297x210 mm
        pdf.image(page, x=0, y=0, w=297, h=210)

pdf.output("Dashboard.pdf")
print("Dashboard.pdf created successfully.")
