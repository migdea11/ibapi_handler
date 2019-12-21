from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ibapi import contract, wrapper

import handler.handler_config as config
from response.contract_response import ContractResponse
from response.error_response import ErrorResponse

if TYPE_CHECKING:
    from handler.request_handler import RequestHandler

LOG = logging.getLogger(__name__)
LOG.setLevel(config.CONFIG_LOG_LEVEL)


class IBWrapper(wrapper.EWrapper):
    def __init__(self, handler: RequestHandler):
        wrapper.EWrapper.__init__(self)
        self.request_handler = handler

    def nextValidId(self, orderId: int):
        LOG.info("setting nextValidOrderId: {}".format(orderId))
        self.nextValidOrderId = orderId

    def error(self, reqId, errorCode, errorString):
        output = "Error. Id: " + str(reqId) + " Code: " + str(errorCode) + " Msg: " + errorString
        if reqId == -1:
            LOG.info(output)
        else:
            LOG.error(output)
            self.request_handler.post_response(ErrorResponse(reqId, errorCode, errorString))

    """
    Wrapper callback overrides below
    """

    def contractDetails(self, reqId, contractDetails: contract.ContractDetails):
        contract: contract.Contract = contractDetails.contract
        self.request_handler.post_response(ContractResponse(reqId, contract.conId, contract.symbol, contractDetails.__dict__))
