import logging
import sys
import threading
import time
from typing import Dict, List

from ibapi.client import EClient

import handler.handler_config as config
from handler.ib_wrapper import IBWrapper
from response.generic_response import GenericResponse
from runner.runner import Runner

LOG = logging.getLogger(__name__)
LOG.setLevel(config.CONFIG_LOG_LEVEL)


class RequestHandler():
    _requests: Dict[str, Runner] = {}
    _responses: Dict[str, GenericResponse] = {}
    _new_id_counter = 0

    _request_lock: threading.Lock = threading.Lock()
    _response_lock: threading.Lock = threading.Lock()
    _counter_lock: threading.Lock = threading.Lock()

    def __init__(self):
        LOG.debug('Creating new Handler')
        self.wrapper = IBWrapper(self)

    @classmethod
    def _get_new_id(klass) -> int:
        valid = False
        new_id = None
        with klass._counter_lock:
            new_id = klass._new_id_counter

        with klass._request_lock:
            while(not valid):
                new_id = new_id + 1 % sys.maxsize
                if new_id not in klass._requests:
                    valid = True

        return new_id

    def create_runner(self, exit_on_response: bool):
        return Runner(self, EClient(self.wrapper), exit_on_response)

    @classmethod
    def register_request(klass, runner: Runner) -> int:
        new_id = klass._get_new_id()

        with klass._request_lock:
            LOG.debug('Registering request: ' + str(new_id))
            klass._requests[new_id] = runner

        return new_id

    @classmethod
    def _clean_requests(klass, req_id: str):
        LOG.debug('Purging inactive requests')
        with klass._request_lock:
            klass._requests = {req_id: runner for req_id, runner in klass._requests.items() if runner.active}

    def get_response(self, req_id: str) -> GenericResponse:
        print('getting response')
        with self._response_lock:
            ret_val = self._responses.get(req_id)

            if ret_val is None:
                LOG.debug('No response found')
                print('No response found')
                return None

            del self._responses[req_id]

        with self._request_lock:
            runner = self._requests.get(req_id)
            runner.close_request(req_id)

        self._clean_requests(req_id)  # TODO this should be done periodically instead
        return ret_val

    def get_all_responses(self, runner: Runner, polling_interval: int = 1) -> List[GenericResponse]:
        if not runner.exit_on_response:
            LOG.error('Cannot get all when runner isn\'t set to exit on completion')
            return None

        results = []
        while runner.active is True:
            for req_id in runner.get_active_requests():
                result = self.get_response(req_id)
                if result:
                    results.append(result)

            if runner.active is True:
                time.sleep(polling_interval)

        return results

    def post_response(self, response: GenericResponse):
        LOG.debug('Recorded response for ' + str(response.req_id))
        with self._response_lock:
            self._responses[response.req_id] = response
