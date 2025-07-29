from flask import g
from src.app.helpers.constant import *


class APIError(Exception):
    def __init__(self, status_code: int, response: dict = None):
        self.message = ERROR_MESSAGES.get(status_code, UNEXPECTED_ERROR)
        self.status_code = status_code
        self.response = [response] if response else []

    def to_json(self):
        return {
            REQUEST_ID: getattr(g, "request_id", "unknown-request-id"),
            STATUS_KEY: FAILED,
            MESSAGE_KEY: self.message,
            CODE_KEY: self.status_code,
            RESPONSE_KEY: self.response
        }


class APISuccess:
    def __init__(self, status_code: int = 200, payload: dict = None):
        self.message = SUCCESS_MESSAGES.get(status_code)
        self.status_code = status_code
        self.payload = payload if payload else {}

    def to_json(self):
        return {
            REQUEST_ID: getattr(g, "request_id", "unknown-request-id"),
            STATUS_KEY: SUCCESS,
            MESSAGE_KEY: self.message,
            CODE_KEY: self.status_code,
            PAYLOAD_KEY: self.payload
        }