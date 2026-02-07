import json
import os
from fpdf import FPDF

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def format_report(report, format="md"):
    if format == "json":
        return export_json(report)
    elif format == "pdf":
        return export_pdf(report)
    else:
        return export_markdown(report)


def export_markdown(report):
    file_path = os.path.join(OUTPUT_DIR, "report.md")

    md = f"# {report['title']}\n\n"
    md += f"**Topic:** {report['topic']}\n\n"
    md += f"**Date:** {report['date']}\n\n"

    md += "## Introduction\n"
    md += report["introduction"] + "\n\n"

    md += "## Key Findings\n"
    for i, item in enumerate(report["findings"], 1):
        md += f"- **Finding {i}:** {item}\n"

    md += "\n## Conclusion\n"
    md += report["conclusion"]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md)

    return file_path


def export_json(report):
    file_path = os.path.join(OUTPUT_DIR, "report.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    return file_path


def export_pdf(report):
    file_path = os.path.join(OUTPUT_DIR, "report.pdf")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, report["title"], ln=True)
    pdf.ln(5)

    pdf.multi_cell(0, 8, f"Topic: {report['topic']}")
    pdf.multi_cell(0, 8, f"Date: {report['date']}")
    pdf.ln(5)

    pdf.multi_cell(0, 8, "Introduction")
    pdf.multi_cell(0, 8, report["introduction"])
    pdf.ln(5)

    pdf.multi_cell(0, 8, "Key Findings")
    for item in report["findings"]:
        pdf.multi_cell(0, 8, f"- {item}")

    pdf.ln(5)
    pdf.multi_cell(0, 8, "Conclusion")
    pdf.multi_cell(0, 8, report["conclusion"])

    pdf.output(file_path)
    return file_path
