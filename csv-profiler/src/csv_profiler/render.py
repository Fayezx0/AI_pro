from __future__ import annotations
from pathlib import Path
import json

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
    
#     # الاستراتيجية: 1. Build lines (إنشاء قائمة للأسطر)
#     lines = []
    
#     # إضافة العنوان
#     lines.append("# CSV Profiling Report")
#     lines.append("")  # سطر فارغ للتنسيق
    
#     # استخدام f-strings لدمج الأرقام داخل النص
#     rows_count = report.get('rows', 0)
#     lines.append(f"- **Total Rows**: {rows_count}")
    
#     # دمج أسماء الأعمدة بفاصلة
#     cols_list = report.get('columns', [])
#     lines.append(f"- **Columns**: {', '.join(cols_list)}")
#     lines.append("")
    
#     # جدول القيم المفقودة
#     lines.append("## Missing Values")
#     lines.append("| Column | Missing Count |")
#     lines.append("|---|---|")
    
#     # حلقة تكرار لإضافة أسطر الجدول
#     missing = report.get("missing", {})
#     for col, count in missing.items():
#         lines.append(f"| {col} | {count} |")
        
#     # الاستراتيجية: 2. Join lines (دمج الأسطر بنزول سطر)
#     final_text = "\n".join(lines) + "\n"
    
#     # الاستراتيجية: 3. Write to file (الحفظ)
#     path.write_text(final_text, encoding="utf-8")


# from __future__ import annotations
# import json
# from pathlib import Path
from datetime import datetime

# # -----------------------------------------------------------------------------
# # Part 1: Writing JSON (Machine Readable)
# # -----------------------------------------------------------------------------
# def write_json(report: dict, path: str | Path) -> None:
#     """Write the report dictionary to a JSON file."""
#     path = Path(path)
#     # Ensure the folder exists
#     path.parent.mkdir(parents=True, exist_ok=True)
    
#     # Dump to text with indentation for readability
#     text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
#     path.write_text(text, encoding="utf-8")


# # -----------------------------------------------------------------------------
# # Part 2: Writing Markdown Helpers (Human Readable)
# # -----------------------------------------------------------------------------
# def md_header(source: str) -> list[str]:
#     """Return the header lines for the report."""
#     ts = datetime.now().isoformat(timespec="seconds")
#     return [
#         "# CSV Profiling Report",
#         "",
#         f"- **Source:** `{source}`",
#         f"- **Generated:** `{ts}`",
#         ""
#     ]

# def format_value(val: any) -> str:
#     """Helper to format float numbers nicely (2 decimal places)."""
#     if isinstance(val, float):
#         return f"{val:.2f}"
#     return str(val)


# # -----------------------------------------------------------------------------
# # Part 3: Main Markdown Function
# # -----------------------------------------------------------------------------
# def write_markdown(report: dict, path: str | Path) -> None:
#     """Generate a Markdown report from the stats."""
#     path = Path(path)
#     path.parent.mkdir(parents=True, exist_ok=True)
    
#     # 1. Start with the header
#     lines = md_header(path.name)
    
#     # 2. Add Summary Section
#     rows_count = report["summary"]["rows"]
#     cols_count = report["summary"]["columns"]
#     lines.append("## Summary")
#     lines.append(f"- **Rows:** {rows_count:,}")
#     lines.append(f"- **Columns:** {cols_count}")
#     lines.append("")

#     # 3. Add Overview Table
#     lines.append("## Column Overview")
#     lines.append("| Column | Type | Missing | Unique |")
#     lines.append("|---|---|---:|---:|")
    
#     for col_name, data in report["columns"].items():
#         # Get basic stats
#         typ = data.get("type", "unknown")
#         missing = data.get("missing", 0)
#         unique = data.get("unique", 0)
        
#         # Calculate percentage of missing data
#         missing_pct = 0.0
#         if rows_count > 0:
#             missing_pct = (missing / rows_count) * 100
            
#         # Add a row to the table
#         row_str = f"| {col_name} | {typ} | {missing} ({missing_pct:.1f}%) | {unique} |"
#         lines.append(row_str)
    
#     lines.append("")

#     # 4. Add Detailed Stats per Column
#     lines.append("## Detailed Statistics")
    
#     for col_name, data in report["columns"].items():
#         lines.append(f"### Column: `{col_name}`")
#         lines.append(f"- **Type:** {data.get('type')}")
        
#         # If it's a number, show min/max/mean
#         if data.get("type") == "number":
#             lines.append(f"- **Min:** {format_value(data.get('min'))}")
#             lines.append(f"- **Max:** {format_value(data.get('max'))}")
#             lines.append(f"- **Mean:** {format_value(data.get('mean'))}")
            
#         # If it's text, show top common values
#         elif "top" in data:
#             lines.append("- **Top Values:**")
#             for item in data["top"]:
#                 val = item["value"]
#                 count = item["count"]
#                 lines.append(f"  - `{val}`: {count} times")
        
#         lines.append("") # Empty line between sections

#     # Join all lines and write to file
#     final_text = "\n".join(lines)
#     path.write_text(final_text, encoding="utf-8")

from datetime import datetime

def render_markdown(report: dict) -> str:
    """
    Convert the profiling report dict into a Markdown string.
    """
    lines = []
    
    # 1. Header & Timestamp
    lines.append("# CSV Profiling Report")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    
    # 2. Summary Section
    lines.append("## Summary")
    lines.append(f"- **Rows**: {report['n_rows']}")
    lines.append(f"- **Columns**: {report['n_cols']}")
    lines.append("")
    
    # 3. Columns Table
    lines.append("## Column Details")
    # Table Header
    lines.append("| Name | Type | Missing (%) | Unique | Stats |")
    lines.append("|---|---|---:|---:|---|")
    
    # Table Rows
    for col in report["columns"]:
        name = col['name']
        typ = col['type']
        missing_pct = f"{col['missing']} ({col['missing_pct']:.1f}%)"
        unique = col['unique']
        
        # Format specific stats (min/max or top values) into a short string
        stats_str = ""
        if typ == "number":
            if "mean" in col:
                stats_str = f"Mean: {col['mean']:.2f}, Min: {col['min']}, Max: {col['max']}"
        else:
            if "top" in col:
                # Show top 1 value as example
                top_val = col['top'][0]['value']
                stats_str = f"Top: {top_val}"

        lines.append(f"| {name} | {typ} | {missing_pct} | {unique} | {stats_str} |")

    # 4. Footer notes
    lines.append("")
    lines.append("---")
    lines.append("*Report generated by CSV Profiler CLI*")
    
    return "\n".join(lines)