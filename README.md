# CSV Profiler
A Python tool to analyze CSV datasets and generate reports.
Built as part of the **AI Professionals Bootcamp**.

## Demo
![CSV Profiler Dashboard](images/image.png)

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
- `app.py`: Streamlit web interface.

├── data/                   # Sample datasets
├── outputs/                # Generated reports (created automatically)
├── src/
│   └── csv_profiler/       # Main Package
│       ├── __init__.py
│       ├── app.py          # Streamlit Dashboard Entrypoint
│       ├── cli.py          # CLI Entrypoint (Typer)
│       ├── io.py           # File handling logic
│       ├── profiling.py    # Core statistical logic
│       └── render.py       # Markdown generation logic
├── .gitignore
├── requirements.txt
└── README.md

## Installation
Ensure you have Python 3.11+ and **uv** installed. This project uses uv for dependency management, then follow these steps:

```bash
git clone https://github.com/Fayezx0/AI_pro.git
cd AI_pro/csv-profiler
python -m venv .venv
.venv\Scripts\activate
uv pip install -r requirements.txt

uv run streamlit run src/csv_profiler/app.py




Built With
-Python 3.11
-Typer (CLI)
-Streamlit (GUI)
-httpx (URL handling)