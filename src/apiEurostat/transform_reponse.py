#functions to transform JSON file containing Eurostat data into a pandas dataframe. and to create lookup tables for the dimensions of the data.

from pyjstat import pyjstat

def print_data_keys(data):
    """
    from
    Print the keys of the data dictionary to understand the structure of the dataset.
    
    Parameters:
    data (dict): The data dictionary.
    
    Returns:
    None
    """
    print("Keys in the data dictionary:\n")
    for key in data.keys():
         print(f"{key}: {data[key]}")


#-----------------------------------------------------------------------

def response_to_dataframe(data):
    """
    Convert a JSON object containing Eurostat data into a pandas DataFrame.
    
    Parameters:
    data (dict): The JSON object containing Eurostat data.
    
    Returns:
    pd.DataFrame: A pandas DataFrame containing the Eurostat data.
    """

    print(pyjstat)
    print(type(pyjstat))
    print(hasattr(pyjstat, "from_json_stat"))

    # Convert the JSON object to a pandas DataFrame
    df = pyjstat.from_json_stat(data, naming = "id")[0]

    return df

def create_lookup_tables(data):
    """
    Create lookup tables for the dimensions of the Eurostat data.
    
    Parameters:
    data (dict): The JSON object containing Eurostat data.
    
    Returns:
    dict: A dictionary containing lookup tables for each dimension of the Eurostat data.
    """
    lookups = {}
    for dim in data['id']:
        lookups[dim] = data['dimension'][dim]['category']['label']
    
    return lookups