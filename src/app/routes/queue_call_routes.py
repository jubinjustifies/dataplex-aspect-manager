from flask import Blueprint, request, jsonify, g
from src.app.helpers.utils import *
from threading import Thread
from src.app.models.job_queue import JobQueue
import asyncio
from logging import basicConfig, INFO
from src.app.services.aspect_manager import create_update_bulk_aspects_with_yaml

basicConfig(level=INFO, format=LOGGING_FORMAT)

queue_call_bp = Blueprint('queue_call_bp', __name__, url_prefix='/dataplex-management-service/api/v1')


job_queue = JobQueue()
event_loop = asyncio.new_event_loop()


async def job_worker():
    while True:
        job = job_queue.dequeue()
        if job is not None:
            try:
                info(f"Processing job: {job['request_id']}")
                data = job['data']
                await create_update_bulk_aspects_with_yaml(data[ASPECT_CREATION_REQUIRED_FIELDS[0]],
                                                           data[ASPECT_CREATION_REQUIRED_FIELDS[1]],
                                                           data[ASPECT_CREATION_REQUIRED_FIELDS[2]])
            except Exception as e:
                error(f"Error processing job {job['request_id']}: {str(e)}")
        await asyncio.sleep(1)


def start_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(job_worker())


Thread(target=start_event_loop, args=(event_loop,), daemon=True).start()


@queue_call_bp.route('/dummy', methods=[POST])
def dummy_route_with_queue_implementation():
    try:
        validate_is_json(request)
        request_id = g.request_id
        data = request.get_json()
        validate_required_fields(data, ASPECT_CREATION_REQUIRED_FIELDS)
        validate_values_are_not_empty(data)
        # validate_values_do_not_have_special_characters(data)
        validate_values_length_do_not_exceed(data)
        job = {
            'request_id': request_id,
            'data': data
        }
        event_loop.call_soon_threadsafe(job_queue.enqueue, job)
        return jsonify({'message': 'Job added to queue', 'request_id': request_id}), 202
    except APIError as e:
        return jsonify(e.to_json()), e.status_code
    except Exception as e:
        return jsonify(APIError(501, {ERROR_KEY: str(e),
                                      REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()), 501
