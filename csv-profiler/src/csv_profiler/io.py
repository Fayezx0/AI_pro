# from __future__ import annotations
# import json
# from pathlib import Path
# from csv import DictReader

# def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
#     """Read a CSV as a list of rows (each row is a dict of strings)."""
    
#     path = Path(path)
    
#     # فتح الملف وقراءته
#     with path.open("r", encoding="utf-8", newline="") as f:
#         reader = DictReader(f)
#         # تحويل البيانات إلى قائمة من القواميس (List of Dictionaries)
#         return [dict(row) for row in reader]

# def write_json(report: dict, path: str | Path) -> None:
#     """Write the report dictionary to a JSON file."""
#     path = Path(path)
#     # Create parent directories (e.g., outputs/) if they don't exist
#     path.parent.mkdir(parents=True, exist_ok=True)
    
#     # Write JSON with indentation for readability
#     path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# def write_markdown(report: dict, path: str | Path) -> None:
#     """Write a human-readable Markdown report."""
#     path = Path(path)
#     path.parent.mkdir(parents=True, exist_ok=True)
    
#     # Prepare lines for the Markdown file
#     lines = []
#     lines.append("# CSV Profiling Report")
#     lines.append("")
#     lines.append(f"- **Total Rows**: {report.get('rows', 0)}")
#     lines.append(f"- **Columns**: {', '.join(report.get('columns', []))}")
#     lines.append("")
#     lines.append("## Missing Values")
#     lines.append("| Column | Missing Count |")
#     lines.append("|---|---|")
    
#     missing = report.get("missing", {})
#     for col, count in missing.items():
#         lines.append(f"| {col} | {count} |")
        
#     # Join lines and write to file
#     path.write_text("\n".join(lines) + "\n", encoding="utf-8")

# if __name__ == "__main__":
#     print("Reports written successfully.")


from pathlib import Path
import csv

def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """
    Read a CSV file and return a list of rows (dicts).
    Raises errors if file is not found or empty.
    """
    # 1. Check if file exists before trying to open
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    # 2. Open and read
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # 3. Check if empty
    if not rows:
        raise ValueError("CSV has no data rows")

    return rows