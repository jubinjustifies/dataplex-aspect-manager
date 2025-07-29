import requests, json, yaml
from typing import List
from models.data_product_model import DataProduct
from models.aspect_type_asset_mapping_model import AspectTypeAssetMapping
from models.aspect_type_env_mapping_model import AspectTypeEnvMapping
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rest_api_helper(url: str, http_verb: str, request_body: str) -> str:
  """Calls the Google Cloud REST API passing in the current users credentials"""

  headers = {
    "Content-Type" : "application/json",
    "Authorization" : "Bearer "
  }
  logging.info(f"Requesting Dataplex for the change")
  logging.info(f"http_verb: {http_verb}, url: {url}, request_body: {request_body}")

  if http_verb == "GET":
    response = requests.get(url, headers=headers)
  elif http_verb == "POST":
    response = requests.post(url, json=request_body, headers=headers)
  elif http_verb == "PUT":
    response = requests.put(url, json=request_body, headers=headers)
  elif http_verb == "PATCH":
    response = requests.patch(url, json=request_body, headers=headers)
  elif http_verb == "DELETE":
    response = requests.delete(url, headers=headers)
  else:
    raise RuntimeError(f"Unknown HTTP verb: {http_verb}")

  if response.status_code == 200:
    return json.loads(response.content)
    #image_data = json.loads(response.content)["predictions"][0]["bytesBase64Encoded"]
  else:
    error = f"Error rest_api_helper -> ' Status: '{response.status_code}' Text: '{response.text}'"
    raise RuntimeError(error)

def json_to_aspect_generator(aspect_type_project_id: str, aspect_type_location: str, aspect_type_id: str, aspect_data: str) -> str:
  aspects = {
    f"{aspect_type_project_id}.{aspect_type_location}.{aspect_type_id}": {
        # "data": json.loads(aspect_data)
        "data": aspect_data
    }
  }
  # logging.info(f"Converting json to aspects: {aspects}") 
  return aspects

def yaml_parser(yaml_file_path: str) -> dict:
  with open(yaml_file_path, 'r') as file:
      data = yaml.safe_load(file)
  # logging.info(f"Parsing YAML to JSON object: {data}")
  return data

def load_aspect_type_asset_mapping(file_path: str) -> AspectTypeAssetMapping:
  data = yaml_parser(file_path)

  if "aspect_types" in data:
      aspect_types_data = data["aspect_types"]
  else:
      raise ValueError("Invalid YAML structure: Missing 'aspect_types' key.")

  aspect_type_asset_mapping = AspectTypeAssetMapping(aspect_types=aspect_types_data)
  # logging.info(f"Loaded aspect_type_asset_mapping: {aspect_type_asset_mapping}")
  return aspect_type_asset_mapping

def load_aspect_type_env_mapping(file_path: str) -> AspectTypeEnvMapping:
  data = yaml_parser(file_path)

  if "aspect_types" in data:
      aspect_types_data = data["aspect_types"]
  else:
      raise ValueError("Invalid YAML structure: Missing 'aspect_types' key.")

  # Create an instance of the AspectTypeEnvMapping model
  aspect_type_env_mapping = AspectTypeEnvMapping(aspect_types=aspect_types_data)
  # logging.info(f"Loaded aspect_type_env_mapping: {aspect_type_env_mapping}")
  return aspect_type_env_mapping

def load_product_entry_mapping(file_path: str) -> List[DataProduct]:
  data = yaml_parser(file_path)
  
  # Handle both "data_products" and "data_product" keys
  if "data_products" in data:
      product_list = data["data_products"]
  elif "data_product" in data:
      product_list = data["data_product"]
  else:
      raise ValueError("Invalid YAML structure: Missing 'data_products' or 'data_product' key.")

  data_products = []
  for product_data in product_list:
    data_products.append(DataProduct(**product_data))

  # logging.info(f"Loaded data_products: {data_products}")
  return data_products

def get_dataplex_project_id_and_region_from_mapping(aspect_type_env_mapping: AspectTypeEnvMapping, aspect_type_id: str) -> dict:
  for aspect_type in aspect_type_env_mapping.aspect_types:
    if aspect_type.aspect_type_id == aspect_type_id:
      # logging.info(f"Getting dataplex env specs -> gcp_project_id: {aspect_type.gcp_project_id}, location_id: {aspect_type.location_id}")
      return dict(dataplex_project_id=aspect_type.gcp_project_id, 
                    dataplex_region=aspect_type.location_id)

def get_gcp_asset_list_from_mapping(aspect_type_asset_mapping: AspectTypeAssetMapping, aspect_type_id: str) -> list:
  for aspect_type in aspect_type_asset_mapping.aspect_types:
    if aspect_type.aspect_type_id == aspect_type_id:
        # logging.info(f"Getting gcp assets list: {aspect_type.gcp_assets}")
        return list(aspect_type.gcp_assets)

