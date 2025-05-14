from .aspect_controller import *
from .aspect_type_controller import *
from models.data_product_model import DataProduct
from models.aspect_type_asset_mapping_model import AspectTypeAssetMapping
from models.aspect_type_env_mapping_model import AspectTypeEnvMapping
from models.constant import *
import logging


aspect_type_env_mapping: AspectTypeEnvMapping = load_aspect_type_env_mapping(ASPECT_TYPE_ENV_MAPPING_FILE)
aspect_type_asset_mapping: AspectTypeAssetMapping = load_aspect_type_asset_mapping(ASPECT_TYPE_ASSET_MAPPING_FILE)
data_product: DataProduct = load_product_entry_mapping(PRODUCT_ENTRY_MAPPING_FILE)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_or_update_aspect_type(project_id,
                       aspect_type_id,
                       aspect_type_location,
                       aspect_type_name,
                       aspect_type_description,
                       metadata_template):
    return create_aspect_type(project_id,
                     aspect_type_id,
                     aspect_type_location,
                     aspect_type_name,
                     aspect_type_description,
                     metadata_template)

def create_or_update_aspect(data_product_id,
                           aspect_type_id,
                           aspect_data):
    try:
        logging.info(f"Starting create_or_update_aspect for data_product_id: {data_product_id}, aspect_type_id: {aspect_type_id}")

        env_dict: dict = get_dataplex_project_id_and_region_from_mapping(aspect_type_env_mapping, aspect_type_id)
        if not env_dict:
            logging.warning(f"No environment mapping found for aspect_type_id: {aspect_type_id}")
            return None

        dataplex_project_id = env_dict["dataplex_project_id"]
        dataplex_region = env_dict["dataplex_region"]

        gcp_asset_list: list = get_gcp_asset_list_from_mapping(aspect_type_asset_mapping, aspect_type_id)

        logging.info(f"Running bulk aspect creation/updation job for data_product_id: {data_product_id}")
        api_responses = []
        for product in data_product:
            if product.product_id == data_product_id:
                for project in product.gcp_projects:
                    logging.info(f"Processing project: {project.project_id}")
                    for location in project.locations:
                        for asset_type in location.asset_types:
                            if asset_type.asset_type_id in gcp_asset_list:
                                logging.info(f"Processing Asset Type: {asset_type.asset_type_id}")

                                # Creating/Updating Aspects under bq_dataset
                                if asset_type.asset_type_id == "bq_dataset" and hasattr(asset_type, 'assets'):
                                    for asset in asset_type.assets:
                                        logging.info(f"      Asset Name: {asset.asset_name}, Flag: {asset.flag}")

                                        bigquery_project_id = project.project_id
                                        bigquery_region = location.location_id
                                        bigquery_dataset = asset.asset_name.split(".")[0]

                                        aspects = json_to_aspect_generator(dataplex_project_id, dataplex_region, aspect_type_id, aspect_data)

                                        api_response = update_system_entry_bq_dataset(dataplex_project_id,
                                                                                    dataplex_region,
                                                                                    bigquery_project_id,
                                                                                    bigquery_region,
                                                                                    bigquery_dataset,
                                                                                    aspects)
                                        api_responses.append(api_response)
                                        logging.info(f"Updated aspect for bq_dataset: {bigquery_dataset}")

                                # Creating/Updating Aspects under bq_table
                                elif asset_type.asset_type_id == "bq_table" and hasattr(asset_type, 'assets'):
                                    for asset in asset_type.assets:
                                        logging.info(f"      Asset Name: {asset.asset_name}, Flag: {asset.flag}")

                                        bigquery_project_id = project.project_id
                                        bigquery_region = location.location_id
                                        bigquery_dataset = asset.asset_name.split(".")[0]
                                        bigquery_table = asset.asset_name.split(".")[1]

                                        aspects = json_to_aspect_generator(dataplex_project_id, dataplex_region, aspect_type_id, aspect_data)

                                        api_response = update_system_entry_bq_table(dataplex_project_id,
                                                                                    dataplex_region,
                                                                                    bigquery_project_id,
                                                                                    bigquery_region,
                                                                                    bigquery_dataset,
                                                                                    bigquery_table,
                                                                                    aspects)
                                        api_responses.append(api_response)
                                        logging.info(f"Updated aspect for bq_table: {bigquery_dataset}.{bigquery_table}")

                                # Creating/Updating Aspects under spn_schema
                                elif asset_type.asset_type_id == "spn_schema" and hasattr(asset_type, 'assets'):
                                    for asset in asset_type.assets:
                                        logging.info(f"      Asset Name: {asset.asset_name}, Flag: {asset.flag}")

                                        spanner_project_id = project.project_id
                                        spanner_region = location.location_id
                                        spanner_schema = asset.asset_name.split(".")[0]

                                        aspects = json_to_aspect_generator(dataplex_project_id, dataplex_region, aspect_type_id, aspect_data)

                                        api_response = update_system_entry_spn_schema(dataplex_project_id,
                                                                                        dataplex_region,
                                                                                        spanner_project_id,
                                                                                        spanner_region,
                                                                                        spanner_schema,
                                                                                        aspects)
                                        api_responses.append(api_response)
                                        logging.info(f"Updated aspect for spn_schema: {spanner_schema}")

                                # Creating/Updating Aspects under spn_table
                                elif asset_type.asset_type_id == "spn_table" and hasattr(asset_type, 'assets'):
                                    for asset in asset_type.assets:
                                        logging.info(f"      Asset Name: {asset.asset_name}, Flag: {asset.flag}")

                                        spanner_project_id = project.project_id
                                        spanner_region = location.location_id
                                        spanner_schema = asset.asset_name.split(".")[0]
                                        spanner_table = asset.asset_name.split(".")[1]

                                        aspects = json_to_aspect_generator(dataplex_project_id, dataplex_region, aspect_type_id, aspect_data)

                                        api_response = update_system_entry_spn_table(dataplex_project_id,
                                                                                    dataplex_region,
                                                                                    spanner_project_id,
                                                                                    spanner_region,
                                                                                    spanner_schema,
                                                                                    spanner_table,
                                                                                    aspects)
                                        api_responses.append(api_response)
                                        logging.info(f"Updated aspect for spn_table: {spanner_schema}.{spanner_table}")

                                # Creating/Updating Aspects under gcs_bucket
                                elif asset_type.asset_type_id == "gcs_bucket" and hasattr(asset_type, 'assets'):
                                    for asset in asset_type.assets:
                                        logging.info(f"      Asset Name: {asset.asset_name}, Flag: {asset.flag}")

                                        gcs_project_id = project.project_id
                                        gcs_region = location.location_id
                                        gcs_bucket = asset.asset_name.split(".")[0]

                                        aspects = json_to_aspect_generator(dataplex_project_id, dataplex_region, aspect_type_id, aspect_data)

                                        api_response = update_system_entry_gcs_bucket(dataplex_project_id,
                                                                                        dataplex_region,
                                                                                        gcs_project_id,
                                                                                        gcs_region,
                                                                                        gcs_bucket,
                                                                                        aspects)
                                        api_responses.append(api_response)
                                        logging.info(f"Updated aspect for gcs_bucket: {gcs_bucket}")
        logging.info(f"Completed create_or_update_aspect for data_product_id: {data_product_id}, aspect_type_id: {aspect_type_id}")
        return {"response": api_responses}
    except Exception as e:
        logging.error(f"Error in create_or_update_aspect for data_product_id: {data_product_id}, aspect_type_id: {aspect_type_id}. Error: {str(e)}")
        return {"response": None, "error": str(e)}