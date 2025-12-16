import json
import time
import typer
from pathlib import Path

# نستورد الأدوات التي صنعناها بأنفسنا!
from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown

app = typer.Typer()

@app.command(help="Profile a CSV file and write JSON + Markdown reports")
def profile(
    input_path: Path = typer.Argument(..., help="Path to input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Folder to save reports"),
    report_name: str = typer.Option("report", "--report-name", help="Base name for the output files"),
):
    """
    هذه الدالة هي التي يتم استدعاؤها عندما تكتب الأمر في التيرمينال.
    """
    try:
        # 1. Start timer
        start_time = time.perf_counter_ns()
        
        # 2. Read Data (Using io.py)
        typer.echo(f"Reading {input_path}...")
        rows = read_csv_rows(input_path)
        
        # 3. Analyze Data (Using profiling.py)
        typer.echo("Analyzing data...")
        report = profile_rows(rows)
        
        # 4. Stop timer and save timing info
        end_time = time.perf_counter_ns()
        elapsed_ms = (end_time - start_time) / 1_000_000
        report["timing_ms"] = elapsed_ms
        
        # 5. Ensure output directory exists
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # 6. Save JSON Report
        json_path = out_dir / f"{report_name}.json"
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        typer.secho(f"✔ Saved JSON: {json_path}", fg=typer.colors.GREEN)
        
        # 7. Save Markdown Report (Using render.py)
        md_path = out_dir / f"{report_name}.md"
        markdown_text = render_markdown(report)
        md_path.write_text(markdown_text, encoding="utf-8")
        typer.secho(f"✔ Saved Markdown: {md_path}", fg=typer.colors.GREEN)
        
        # Print final summary
        typer.echo(f"Done! Processed {report['n_rows']} rows in {elapsed_ms:.2f}ms")

    except Exception as e:
        # التعامل مع الأخطاء بطريقة أنيقة (لون أحمر)
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()