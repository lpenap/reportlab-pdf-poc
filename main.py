"""
Module to demonstrate the use of ReportLab to generate PDFs
This PoC generates a PDF with the following elements:
- A Sample Sales graph using Matplotlib
- A Sample Ledger table with mocked data
- A Sample 20 x 10 table

"""

import matplotlib.pyplot as plot
import pandas
import numpy
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

output_folder = "out/"


# Function to create a simulated ledger table
def create_ledger_table():
    data = {
        "Date": pandas.date_range("2023-10-01", periods=30).strftime("%Y-%m-%d"),
        "Debit": numpy.random.randint(100, 1000, 30),
        "Credit": numpy.random.randint(100, 1000, 30),
    }
    data_frame = pandas.DataFrame(data)
    return data_frame


# Function to create a 20x10 sample table
def create_sample_table():
    data_frame = pandas.DataFrame([["sample"] * 10] * 20)
    return data_frame


# Saving the sales graph and progress bar images
sales_graph_file = output_folder + "sales_graph.png"
plot.figure(figsize=(6, 4))
plot.plot([1, 2, 3, 4], [10, 20, 30, 40], "go-", label="line 1", linewidth=2)
plot.title("Sample Sales Report")
plot.xlabel("Quarter")
plot.ylabel("Sales")
plot.legend()
plot.savefig(sales_graph_file)
plot.close()

# Prepare the ledger and sample tables for PDF
ledger_table = create_ledger_table()
ledger_pdf_table = Table(
    ledger_table.values.tolist(), colWidths=[100] * 3, rowHeights=20
)

sample_table = create_sample_table()
sample_pdf_table = Table(
    sample_table.values.tolist(), colWidths=[50] * 10, rowHeights=20
)

# Styling the tables
ledger_pdf_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )
)
sample_pdf_table.setStyle(
    TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 1, colors.blue),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]
    )
)

# Generating the PDF with each element on a different page
pdf_path = output_folder + "sales_report.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)
margin = 72  # 1 inch margin

# Add the sales graph on the first page
c.drawImage(
    sales_graph_file, margin, 300, width=400, height=300, preserveAspectRatio=True
)
c.showPage()

# Add the ledger table on the second page
ledger_table_width, ledger_table_height = ledger_pdf_table.wrap(0, 0)
ledger_pdf_table.drawOn(c, x=margin, y=letter[1] - margin - ledger_table_height)
c.showPage()

# Add the sample table on the third page
sample_table_width, sample_table_height = sample_pdf_table.wrap(0, 0)
sample_pdf_table.drawOn(c, x=margin, y=letter[1] - margin - sample_table_height)
c.showPage()

# Save the PDF
c.save()
