import pandas as pd


#tranform time to number
def time_to_int(df):
    '''Convert the 'time' column of a DataFrame to integer, ensuring annual frequency only.
    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with 'time' and 'freq' columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with 'time' column converted to integer.

    Raises
    ------
    ValueError
        If the 'freq' column contains values other than 'A' (annual).
    '''
    #check that the time frequency of the dataset is annually only
    annual_freq = "A"
    if not df['freq'].eq(annual_freq).all():
        bad = df.loc[df['freq'].ne(annual_freq), 'freq'].unique().tolist()
        raise ValueError(f"time_to_int expects annual data only; found freq values: {bad}")

    df = df.copy()
    df['time'] = pd.to_numeric(df['time'], errors="raise").astype("Int64")
    return df

# create a function that does 