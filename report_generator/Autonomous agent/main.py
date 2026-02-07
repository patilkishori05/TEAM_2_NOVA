import asyncio
from reporting.report_generator import generate_report
from reporting.output_controller import format_report

# Dummy summaries for testing
summaries = [
    "AI agents can autonomously search the web.",
    "They summarize large volumes of online data.",
    "Automated report generation saves time."
]

async def main():
    report = await generate_report(
        summaries=summaries,
        topic="Autonomous Web Research Agent",
        length="short",
        format="md"
    )

    output_path = format_report(report, format="pdf")
    print("Report generated at:", output_path)

asyncio.run(main())
