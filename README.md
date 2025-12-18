# CSV Profiler
A Python tool to analyze CSV datasets and generate reports.
Built as part of the **AI Professionals Bootcamp**.

## Features
- CSV ingestion using pandas
- Descriptive statistics and profiling
- Report generation (Markdown / JSON)
- CLI and Streamlit interface

## Project Structure
The source code is organized under the `src/` directory:
- `cli.py`: Handles command-line arguments and interface.
- `io.py`: Manages file input/output operations.
- `profiling.py`: Core analysis logic.
- `render.py`: Formats and generates the report.

## Installation
Ensure you have **uv** installed, then follow these steps:

```bash
git clone https://github.com/Fayezx0/AI_pro.git
cd AI_pro/csv-profiler
python -m venv .venv
.venv\Scripts\activate
pip install pandas streamlit typer

uv run streamlit run src/csv_profiler/app.py
