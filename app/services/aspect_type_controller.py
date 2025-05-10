from utils import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def exists_aspect_type(dataplexProject_id, aspect_type_id, aspect_type_location):
  """Checks to see if an Entry Group already exists"""

  url = f"https://dataplex.googleapis.com/v1/projects/{dataplexProject_id}/locations/{aspect_type_location}/aspectTypes"

  json_result = rest_api_helper(url, "GET", None)
  logging.info(f"exists_aspect_type (GET) json_result: {json_result}")

  # Test to see if exists, if so return
  if "aspect_types" in json_result:
    for item in json_result["aspect_types"]:
      logging.info(f"Name: {item['name']}")
      if item["name"] == f"projects/{dataplexProject_id}/locations/{aspect_type_location}/aspectTypes/{aspect_type_id}":
        # print(f"Aspect Type {aspect_type_id} already exists")
        return True

  return False

def create_aspect_type(dataplexProject_id, aspect_type_id, aspect_type_location, aspect_type_name, aspect_type_description, metadata_template):
  """Creates an Aspect Type if it does not exist"""

  if exists_aspect_type(dataplexProject_id, aspect_type_id, aspect_type_location) == False:
    logging.info(f"Aspect Type {aspect_type_id} does not exist, creating")
    url = f"https://dataplex.googleapis.com/v1/projects/{dataplexProject_id}/locations/{aspect_type_location}/aspectTypes?aspectTypeId={aspect_type_id}"

    data = {
      "displayName": aspect_type_name,
      "description": aspect_type_description,
      "metadataTemplate": metadata_template
    }

    json_result = rest_api_helper(url, "POST", data)
    logging.info(f"create_aspect_type (POST) json_result: {json_result}")
  else:
    print(f"create_aspect_type (POST) Aspect Type {aspect_type_id} already exists")