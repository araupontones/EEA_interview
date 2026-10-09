import pandas as pd


#tranform time to number
def time_to_int(df):
    #check that the time frequency of the dataset is annually only
    annual_freq = "A"
    if not df['freq'].eq(annual_freq).all():
        bad = df.loc[df['freq'].ne(annual_freq), 'freq'].unique().tolist()
        raise ValueError(f"time_to_int expects annual data only; found freq values: {bad}")

    df = df.copy()
    df['time'] = pd.to_numeric(df['time'], errors="raise").astype("Int64")
    return df

# create a function that does 