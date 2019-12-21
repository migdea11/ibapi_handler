from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING, Set, List

from ibapi.client import EClient
from ibapi.common import TagValueList
from ibapi.contract import Contract

import handler.handler_config as config

if TYPE_CHECKING:
    from handler.request_handler import RequestHandler

LOG = logging.getLogger(__name__)
LOG.setLevel(config.CONFIG_LOG_LEVEL)


class Runner():
    _client_pool = 0
    _client_pool_lock = threading.Lock()

    def __init__(self, handler: RequestHandler, client: EClient, exit_on_response: bool = True):
        LOG.debug('Creating new Runner')
        self._handler = handler
        self._client = client

        self._req_id_lock = threading.Lock()
        self._req_id_set: Set[int] = set()
        self._thread: threading.Thread = None

        self.exit_on_response = exit_on_response
        self.active = True

        with self._client_pool_lock:
            self._client_pool += 1
            if self._client_pool >= config.CONFIG_CONNECT_MAX_CONNECTION_POOL:
                self._client_pool -= 1
                return None

            LOG.info('Establishing connection as client: ' + str(self._client_pool))
            self._client.connect(config.CONFIG_CONNECT_HOST, config.CONFIG_CONNECT_PORT, clientId=self._client_pool)

    def _get_req_id(self) -> int:
        new_id = self._handler.register_request(self)
        print('TESTING adding req_id ' + str(new_id))
        self._req_id_set.add(new_id)
        return new_id

    def _runner_execution(self):
        LOG.info('Runner thread started')
        print('TESTING')
        print(self._req_id_set)
        self._client.run()

    def execute(self):
        LOG.debug('Runner starting child thread')
        self._thread = threading.Thread(target=self._runner_execution)
        self._thread.start()

    def get_active_requests(self) -> List[int]:
        with self._req_id_lock:
            return list(self._req_id_set)

    def close_request(self, req_id):
        if self.exit_on_response:
            print('TESTING set')
            print(self._req_id_set)
            self._req_id_set.remove(req_id)

            if not self._req_id_set:
                LOG.info('Closing connection with client')
                self._client.disconnect()
                self.active = False

                with self._client_pool_lock:
                    self._client_pool += 1

    """
    Client request overrides below
    """

    def reqSmartComponents(self, bboExchange: str) -> int:
        ret_val = self._get_req_id()
        self._client.reqSmartComponents(ret_val, bboExchange)
        return ret_val

    def reqAccountSummary(self, groupName: str, tags: str) -> int:
        ret_val = self._get_req_id()
        self._client.reqAccountSummary(ret_val, groupName, tags)
        return ret_val

    def cancelAccountSummary(self) -> int:
        ret_val = self._get_req_id()
        self._client.cancelAccountSummary(ret_val)
        return ret_val

    def reqContractDetails(self, contract: Contract) -> int:
        ret_val = self._get_req_id()
        self._client.reqContractDetails(ret_val, contract)
        return ret_val

    def reqMktData(self, contract: Contract, genericTickList: str, snapshot: bool, regulatorySnapshot: bool, mktDataOptions: TagValueList) -> int:
        ret_val = self._get_req_id()
        self._client.reqMktData(ret_val, contract, genericTickList, snapshot, regulatorySnapshot, mktDataOptions)
        return ret_val

    def cancelMktData(self) -> int:
        ret_val = self._get_req_id()
        self._client.cancelMktData(ret_val)
        return ret_val

    def reqTickByTickData(self, contract: Contract, tickType: str, numberOfTicks: int, ignoreSize: bool) -> int:
        ret_val = self._get_req_id()
        self._client.reqTickByTickData(ret_val, contract, tickType, numberOfTicks, ignoreSize)
        return ret_val

    def cancelTickByTickData(self) -> int:
        ret_val = self._get_req_id()
        self._client.cancelTickByTickData(ret_val)
        return ret_val

    def calculateImpliedVolatility(self, contract: Contract, optionPrice: float, underPrice: float, implVolOptions: TagValueList) -> int:
        ret_val = self._get_req_id()
        self._client.calculateImpliedVolatility(ret_val, contract, optionPrice, underPrice, implVolOptions)
        return ret_val

    def cancelCalculateImpliedVolatility(self) -> int:
        ret_val = self._get_req_id()
        self._client.cancelCalculateImpliedVolatility(ret_val)
        return ret_val

    def cancelCalculateOptionPrice(self) -> int:
        ret_val = self._get_req_id()
        self._client.cancelCalculateImpliedVolatility(ret_val)
        return ret_val
