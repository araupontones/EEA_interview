import pandas as pd

def profile(df: pd.DataFrame, lookups: dict | None = None) -> None:
    """Print a short structural profile of a raw table. Changes nothing."""
    print(f"shape: {df.shape}")
    print("\ndtypes:")
    print(df.dtypes.to_string())

   #Type of date variable
    if "time" in df.columns:
        time = df["time"].dropna().astype(str)
        print("\ntype of time variable:")
        print("Annual:", time.str.match(r"^\d{4}$").sum())
        print("Quarterly:", time.str.match(r"^\d{4}-Q[1-4]$").sum())
        print("Monthly:", time.str.match(r"^\d{4}-\d{2}$").sum())
        print("Daily:", time.str.match(r"^\d{4}-\d{2}-\d{2}$").sum())

    print("\nmissing share per column:")
    print(df.isna().mean().round(3).to_string())

    constant = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
    print(f"\nconstant columns: {constant}")

    if "flag" in df.columns:
        print("\nflag counts:")
        print(df["flag"].value_counts(dropna=False).to_string())

    if "value" in df.columns:
        print("\nvalue summary:")
        print(df["value"].describe().to_string())

    if lookups:
        print("\nlookup vs data (code counts/values in dimension):")
        for d, m in lookups.items():
            if d in df.columns:
                print(f"  {d}: lookup={len(m)}, in data={df[d].nunique()}")