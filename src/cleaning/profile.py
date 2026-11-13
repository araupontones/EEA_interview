import pandas as pd

def profile(df: pd.DataFrame, lookups: dict, dim : str | None = None) -> None:
    """Print a short structural profile of a raw table. Changes nothing."""
    print(f"shape: {df.shape}")
    print("\ndata types:")
    print(df.dtypes.to_string())

    print(f"\nTime frequency:")
    if 'freq' in df.columns:
        for value, count in df["freq"].value_counts(dropna=False).items():
            print(f"{value}: {count}")
    else:
        print('freq not in columns')


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


# End of profile function
#function to check the amount of negative values in the 'value' column
def profile_indicator(df: pd.DataFrame, lookups: dict, dim: str) -> None:
    """Print the amount of negative values in the 'value' column."""
    print(f"\nCategories in {dim}:")
    #print all the categories in the specified dimension (make so the print makes it vertical)
    for code, description in lookups[dim].items():
        print(f"{code}: {description}")
    print(f"\nCategories in {dim} that have negative values:")
    # Get the unique codes in the specified dimension where the 'value' column is negative
    codes = df.loc[df['value'] < 0, dim].unique()

    if len(codes) > 0 :
        for code in codes:
             print(f"{code}: {lookups[dim].get(code, 'unknown')}")
    else:
        print("All values are positive")