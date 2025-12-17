
# CSV Profiler 

A Python tool to analyze CSV datasets and a reports. This project was built as part of the **AI Professionals Bootcamp**.

## Features
- **Data Ingestion:** reads CSV files using `pandas`.
- **Data Analysis:** Calculates descriptive statistics and profiling metrics.
- **Reporting:** Generates reports (Markdown/JSON).
- **Modern Tooling:** Built using `uv` for fast and reliable dependency management.

## Project Structure
The source code is organized under the `src/` directory:
- `cli.py`: Handles command-line arguments and interface.
- `io.py`: Manages file input/output operations.
- `profiling.py`: Contains the core logic for data analysis.
- `render.py`: formatting and generating the final report.

## Installation

Ensure you have **uv** installed, then follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Fayezx0/AI_pro.git
   cd AI_pro