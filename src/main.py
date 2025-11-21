import json
from pathlib import Path

from dotenv import load_dotenv

# Load env before importing anything that may use API keys
load_dotenv()

from .extract_text import extract_text_from_pdf
from .summarise import summarise_act
from .extract_sections import extract_key_sections
from .rules_check import run_rule_checks


def main():
    pdf_path = "data/ukpga_20250022_en.pdf"

    print("📄 Extracting text from PDF...")
    full_text = extract_text_from_pdf(pdf_path)

    print("📝 Creating 5–10 bullet-point summary...")
    summary_bullets = summarise_act(full_text)

    print("📚 Extracting key legislative sections...")
    sections = extract_key_sections(full_text)

    print("✅ Running rule checks...")
    rule_checks = run_rule_checks(full_text, sections)

    report = {
        "summary_bullets": summary_bullets,
        "sections": sections,
        "rule_checks": rule_checks,
    }

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "report.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"🎉 Done! JSON report saved to: {output_path}")


if __name__ == "__main__":
    main()
