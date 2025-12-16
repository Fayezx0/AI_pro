from __future__ import annotations
from collections import Counter

# --- Helpers ---

def is_missing(value: str | None) -> bool:
    """Check if a value is effectively missing."""
    if value is None:
        return True
    return value.strip().casefold() in {"", "na", "n/a", "null", "none", "nan"}

def try_float(value: str) -> float | None:
    """Try to convert string to float, return None if fails."""
    try:
        return float(value)
    except ValueError:
        return None

def infer_type(values: list[str]) -> str:
    """Decide if a column is 'number' or 'text'."""
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"

# --- Main Profiling Logic ---

def profile_rows(rows: list[dict[str, str]]) -> dict:
    """
    Takes raw CSV rows and returns a full statistical report (dict).
    """
    # 1. Setup summary info
    if not rows:
        return {"n_rows": 0, "n_cols": 0, "columns": []}

    columns = list(rows[0].keys())
    n_rows = len(rows)
    col_profiles = []

    # 2. Loop through each column
    for col in columns:
        # Extract all values for this column
        values = [r.get(col, "") for r in rows]
        
        # Basic stats
        usable = [v for v in values if not is_missing(v)]
        missing = len(values) - len(usable)
        inferred = infer_type(values)
        unique = len(set(usable))
        
        # Calculate missing percentage safely
        missing_pct = 0.0
        if n_rows > 0:
            missing_pct = (missing / n_rows) * 100.0

        # Build column report
        col_report = {
            "name": col,
            "type": inferred,
            "missing": missing,
            "missing_pct": missing_pct,
            "unique": unique,
        }

        # Add specific stats based on type
        if inferred == "number":
            # Numeric stats: min, max, mean
            nums = [try_float(v) for v in usable]
            # remove None just in case
            valid_nums = [x for x in nums if x is not None]
            
            if valid_nums:
                col_report["min"] = min(valid_nums)
                col_report["max"] = max(valid_nums)
                col_report["mean"] = sum(valid_nums) / len(valid_nums)
        
        else:
            # Text stats: Top 5 common values
            # Using Counter makes finding top values very easy!
            counts = Counter(usable)
            # Get top 5: returns list of (value, count)
            top_5 = [{"value": k, "count": v} for k, v in counts.most_common(5)]
            col_report["top"] = top_5

        col_profiles.append(col_report)

    # 3. Return final structure
    return {
        "n_rows": n_rows,
        "n_cols": len(columns),
        "columns": col_profiles
    }