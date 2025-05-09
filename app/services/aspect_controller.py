from utils import *


# UPDATE SYSTEM ENTRIES - ASPECTS
def update_system_entry_bq_table(dataplexProject_id, entryGroupLocation, bigqueryProjectId, bigqueryRegion, 
                                            bigqueryDataset, bigqueryTable, aspects):
    """Associates an Entry Type and Aspect Type to a BigQuery (Dataplex System Entry Group)"""

    print(f'inside update_system_entry_bq_table')
    url = f"https://dataplex.googleapis.com/v1/projects/{dataplexProject_id}/locations/{entryGroupLocation}/entryGroups/" + \
            f"@bigquery/entries/bigquery.googleapis.com/projects/{bigqueryProjectId}/datasets/{bigqueryDataset}/tables/{bigqueryTable}?update_mask=aspects"

    data = {
        "aspects": aspects
    }

    json_result = rest_api_helper(url, "PATCH", data)
    print(f"updateDataplexSystemEntry_BigQueryTable (PATCH) json_result: {json_result}")

def update_system_entry_bq_dataset(dataplexProject_id, entryGroupLocation, bigqueryProjectId,
                                              bigqueryRegion, bigqueryDataset, aspects):
    """Updates aspects for a BigQuery Dataset (Dataplex System Entry Group)"""

    print(f'inside update_system_entry_bq_dataset')
    url = f"https://dataplex.googleapis.com/v1/projects/{dataplexProject_id}/locations/{entryGroupLocation}/entryGroups/" + \
            f"@bigquery/entries/bigquery.googleapis.com/projects/{bigqueryProjectId}/datasets/{bigqueryDataset}?update_mask=aspects"

    data = {
        "aspects": aspects
    }

    json_result = rest_api_helper(url, "PATCH", data)
    print(f"updateDataplexSystemEntry_BigQueryDataset (PATCH) json_result: {json_result}")

def update_system_entry_spn_schema(dataplexProject_id, entryGroupLocation, spannerProjectId, spannerRegion,
                                            spannerInstance, spannerDatabase, aspects):
    """Updates aspects for a Spanner Schema"""

    url = f"https://dataplex.googleapis.com/v1/projects/{dataplexProject_id}/locations/{entryGroupLocation}/entryGroups/" + \
          f"@spanner/entries/spanner.googleapis.com/projects/{spannerProjectId}/instances/{spannerInstance}/databases/{spannerDatabase}?update_mask=aspects"

    data = {
        "aspects": aspects
    }

    json_result = rest_api_helper(url, "PATCH", data)
    print(f"updateDataplexSystemEntry_SpannerSchema (PATCH) json_result: {json_result}")

def update_system_entry_spn_table(dataplexProject_id, entryGroupLocation, spannerProjectId, spannerRegion,
                                           spannerInstance, spannerDatabase, spannerTable, aspects):
    """Updates aspects for a Spanner Table"""

    url = f"https://dataplex.googleapis.com/v1/projects/{dataplexProject_id}/locations/{entryGroupLocation}/entryGroups/" + \
          f"@spanner/entries/spanner.googleapis.com/projects/{spannerProjectId}/instances/{spannerInstance}/databases/{spannerDatabase}/tables/{spannerTable}?update_mask=aspects"

    data = {
        "aspects": aspects
    }

    json_result = rest_api_helper(url, "PATCH", data)
    print(f"updateDataplexSystemEntry_SpannerTable (PATCH) json_result: {json_result}")

def update_system_entry_gcs_bucket(dataplexProject_id,
                                           entryGroupLocation,
                                           gcsProjectId,
                                           gcsRegion,
                                           gcsBucket,
                                           aspects):
    """Updates aspects for a GCS Bucket"""

    url = f"https://dataplex.googleapis.com/v1/projects/{dataplexProject_id}/locations/{entryGroupLocation}/entryGroups/" + \
          f"@storage/entries/storage.googleapis.com/{gcsBucket}?update_mask=aspects"

    data = {
        "aspects": aspects
    }

    json_result = rest_api_helper(url, "PATCH", data)
    print(f"updateDataplexSystemEntry_GCSBucket (PATCH) json_result: {json_result}")