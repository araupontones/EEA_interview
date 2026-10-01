#Functions to download data from Eurostat API

#Filters are optional and can be any dimension present in the data. Filters start with a question mark ("?") and are separated by an ampersand (&) if there are several filters.
#For time: "utnilTilePeriod", "sinceTimePeriod", and "lastTimePeriod".

import requests
from pyjstat import pyjstat

def download_eurostat(datasetCode, host_Url =  "https://ec.europa.eu/eurostat/api/dissemination/",
                      service = "statistics",
                      version = "1.0",
                      response_type = "data",
                      format = "JSON",
                      lang= "EN",
                      geoLevel = "country",
                      sinceTimePeriod =  "2010",
                      untilTimePeriod = '2026'                      
                      ):
    """
    Download a dataset from the Eurstat Statistics API and return the data as a JSON object.

    Sends a GET request to the Eurostat API and returns the response as a JSON object.

    Args:
        datasetCode (str): The code of the dataset to download.
        host_Url (str): The base URL of the Eurostat API. Default is "https://ec.europa.eu/eurostat/api/dissemination/".
        service (str): The service to use. Default is "statistics".
        version (str): The version of the API to use. Default is "1.0".
        response_type (str): The type of response to request. Default is "data".
        format (str): The format of the response. Default is "JSON".
        lang (str): The language of the response. Default is "EN".  
        geoLevel (str): The level of geographical detail. Default is "country".
        sinceTimePeriod (str): The start time period for the data. Default is "2010".
        untilTimePeriod (str): The end time period for the data. Default is "2026".
    
    Returns:
        dict: The data returned by the Eurostat API as a JSON object.
    
    
    Raises:
        requests.exceptions.RequestException: If the request to the Eurostat API fails.
    
    References:
        Eurostat API documentation: https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/api-statistics
    """
    #define url
    url = f"{host_Url}{service}/{version}/{response_type}/{datasetCode}"

    params = {
        "format" : format,
        "lang" : lang,
        "geoLevel" : geoLevel,
    }

    #add these parameters only if they user has provided them
    if sinceTimePeriod:
        params["sinceTimePeriod"] = sinceTimePeriod
    if untilTimePeriod:
        params["untilTimePeriod"] = untilTimePeriod

    #execute the request
    response = requests.get(url, params=params)

    response.raise_for_status()

    data = response.json()

    return data
