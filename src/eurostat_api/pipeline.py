import logging
from eurostat_api.download_eurostat import download_eurostat
from eurostat_api import transform_response as tr

log = logging.getLogger(__name__)

def process(datasetCode: str) -> None:
    data = download_eurostat(datasetCode)
    df = tr.response_to_dataframe(data)
    if df.empty:
        raise ValueError(f"{datasetCode}: downloaded dataframe is empty")

    lookups = tr.create_lookup_tables(data)
    missing = set(lookups) - set(df.columns)
    if missing:
        raise ValueError(f"{datasetCode}: dimensions in lookups but not in dataframe: {missing}")

    output_dir = tr.create_output_directory(datasetCode)
    tr.save_raw_data(output_dir, df=df, lookups=lookups, meta=tr.get_metadata(data))
    log.info("%s: saved %d rows to %s", datasetCode, len(df), output_dir)

