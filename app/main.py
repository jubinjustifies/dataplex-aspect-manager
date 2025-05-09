from services.operations_handler import *
from utils import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

product_id = "odp_dp_1"
myAspectTypeId = "data-owner-aspect"
aspect_data = '{"owner": "Compliance", "email": "compliance@google.com", "data_product_type": "ODP"}'

logging.info(f"Starting Job")
create_or_update_aspect(product_id, myAspectTypeId, aspect_data)