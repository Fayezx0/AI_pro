
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown


def main() -> None:
    rows = read_csv_rows("data/sample.csv")    # 1. Read data
    report = basic_profile(rows) # 2. Process data
    print(report)

    # 3. Output results
    write_json(report, "outputs/report.json")
    write_markdown(report, "outputs/report.md")
    
    print("Wrote successfully outputs/report.json and outputs/report.md")


if __name__ == "__main__":
    main()