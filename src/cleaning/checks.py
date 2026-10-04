from dataclasses import dataclass, asdict
import pandas as pd
from pandas.api.types import is_numeric_dtype

@dataclass
class CheckResult:
    check: str
    severity: str        # "error" | "warning" | "info"
    passed: bool
    n_issues: int
    detail: str = ""

def unique_key(df, key):
    dup = df.duplicated(key, keep=False)
    return CheckResult("unique_key", "error", not dup.any(), int(dup.sum()), f"key={key}")

def codes_in_lookup(df, lookups):
    bad = {d: sorted(set(df[d].dropna()) - set(m))
           for d, m in lookups.items() if d in df.columns}
    bad = {d: v for d, v in bad.items() if v}
    return CheckResult("codes_in_lookup", "error", not bad, sum(map(len, bad.values())), str(bad))

def non_negative(df, col="value"):
    n = int((df[col] < 0).sum())
    return CheckResult("non_negative", "error", n == 0, n, col)

def numeric_dtypes(df, cols=("time", "value"), severity="warning"):
    """Columns that should be numeric but are stored as strings (or other non-numeric types)."""
    detail = {}
    for c in cols:
        if c not in df.columns:
            detail[c] = "missing column"
        elif not is_numeric_dtype(df[c]):
            # how many entries could not be converted to numbers?
            bad = int(pd.to_numeric(df[c], errors="coerce").isna().sum() - df[c].isna().sum())
            detail[c] = f"dtype={df[c].dtype}, not convertible={bad}"
    return CheckResult("numeric_dtypes", severity, not detail, len(detail), str(detail))



def missing_share(df, max_share = 0, severity = 'warning'):
    '''Columns with missing values'''
    miss = [f"{m}: {df[m].isna().mean():.2%}"
            for m in df.columns
            if df[m].isna().mean() > max_share]
    
    return CheckResult("missing_share_2", severity, not miss, len(miss), str(miss))
   

def constant_columns(df, severity="info"):
    """Columns with a single distinct value (including all-missing columns)."""
    if df.empty:
        return CheckResult("constant_columns", severity, True, 0, "empty dataframe")
    const = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
    return CheckResult("constant_columns", severity, not const, len(const), str(const))


def dims_match_lookup(df, lookups, non_dim_cols=("value", "flag"), severity="error"):
    """Dimensions in the lookup versus dimension columns in the data (compared as sets, not just counts)."""
    data_dims = set(df.columns) - set(non_dim_cols)
    lookup_dims = set(lookups)
    only_lookup = sorted(lookup_dims - data_dims)
    only_data = sorted(data_dims - lookup_dims)
    passed = not only_lookup and not only_data
    return CheckResult("dims_match_lookup", severity, passed,
                       len(only_lookup) + len(only_data),
                       f"n_lookup={len(lookup_dims)}, n_data={len(data_dims)}; "
                       f"only in lookup={only_lookup}; only in data={only_data}")

# def completeness(df, geos, years, by=("wst_oper", "unit")):
#     """Missing country-year combinations per group (rows absent or value NaN)."""
#     expected = pd.MultiIndex.from_product([geos, years], names=["geo", "time"])
#     missing = 0
#     for _, g in df.dropna(subset=["value"]).groupby(list(by)):
#         have = pd.MultiIndex.from_frame(g[["geo", "time"]].drop_duplicates())
#         missing += len(expected.difference(have))
#     return CheckResult("completeness", "warning", missing == 0, missing,
#                        f"{len(geos)} geos x {len(years)} years")

# def hierarchy_sums(df, parent, children, tol=0.02):
#     """Parent should equal the sum of its children (relative tolerance)."""
#     w = (df.pivot_table(index=["geo", "time", "unit"], columns="wst_oper", values="value")
#            .dropna(subset=[parent] + children))
#     diff = (w[children].sum(axis=1) - w[parent]).abs() / w[parent].replace(0, pd.NA)
#     n = int((diff > tol).sum())
#     return CheckResult(f"sum_{parent}", "warning", n == 0, n, f"{parent} vs {children}, tol={tol}")