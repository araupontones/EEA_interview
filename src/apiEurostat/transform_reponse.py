#functions to transform JSON file containing Eurostat data into a pandas dataframe. and to create lookup tables for the dimensions of the data.

from datetime import datetime, timezone
from pyjstat import pyjstat
from pathlib import Path
import json
from pathlib import Path




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

def get_metadata(data):
    """
    Extract metadata from the Eurostat data.
    
    Parameters:
    data (dict): The JSON object containing Eurostat data.
    
    Returns:
    dict: A dictionary containing the metadata.
    """
    metadata = {
        "label": data.get('label'),
        "source": data.get('source'),
        "updated": data.get('updated'),
        "dataSource": data['extension']['id'],
        "retrieved_at": datetime.now(timezone.utc).isoformat()
    }
    
    return metadata 

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

#-----------------------------------------------------------------------
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

#-----------------------------------------------------------------------

def get_source_code(data):
    """
    Get the source code from the Eurostat data.
    
    Parameters:
    data (dict): The JSON object containing Eurostat data.
    
    Returns:
    str: The indicator code.
    """
    return data['extension']['id']

#-----------------------------------------------------------------------

def get_source_label(data):
    """
    Get the source label from the Eurostat data.
    
    Parameters:
    data (dict): The JSON object containing Eurostat data.
    
    Returns:
    str: The source label.
    """
    return data['label']

#-----------------------------------------------------------------------

def create_output_directory(datasetCode, path = 'c:/repositaries/4.personal/EEA_interview/data/raw'):
    """
    Create the output directory if it does not exist.
    
    Parameters:
    output_dir (str): The path to the output directory.
    
    Returns:
    None
    """
    #create path to output directory
    output_dir = Path(path) / datasetCode

    if output_dir.exists():
        print(f"Output directory already exists: {output_dir}")
    else:
        print(f"Creating output directory: {output_dir}")
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    return output_dir

#-----------------------------------------------------------------------

def save_parquet(object, output_dir, file_name):
    """
    Save a DataFrame as a Parquet file in an indicator-specific directory.

    Args:
        data (pd.DataFrame):
            DataFrame to save.

        datasetCode (str):
            Eurostat dataset code used as the subdirectory name.

        file_name (str):
            Name of the Parquet file, without the .parquet extension.

        output_dir (str or Path, optional):
            Base output directory. Defaults to "output".
    """

    file_path = Path(output_dir) / f"{file_name}.parquet"

    object.to_parquet(file_path, index=False)

    print(f"Saved: {file_path}")

    #-----------------------------------------------------------------------

def save_json(obj, path):
    path = Path(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

#-----------------------------------------------------------------------

def save_raw_data(output_dir, df= None, lookups = None, meta = None ):
    folder = Path(output_dir)
    
    if df is not None:
        df.to_parquet(folder / "df.parquet", index=False)
    if lookups is not None:
        save_json(lookups, folder / "lookup.json")
    if meta is not None:
        save_json(meta, folder / "metadata.json")