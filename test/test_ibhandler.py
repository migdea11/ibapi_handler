import logging

from ibapi.contract import Contract

import common.contract_utils as contract_utils
import handler.handler_config as config
from handler.request_handler import RequestHandler

logging.basicConfig(format=config.CONFIG_LOG_FORMAT, level=config.CONFIG_LOG_LEVEL)
LOG = logging.getLogger(__name__)

contract = Contract()
contract.symbol = 'AAPL'
contract.currency = 'USD'
contract.secType = contract_utils.SecurityType.STOCK.value

LOG.info('Contract ' + contract.symbol)

handler = RequestHandler()
runner = handler.create_runner(exit_on_response=True)
new_id = runner.reqContractDetails(contract)
runner.execute()

print([result.__dict__ for result in handler.get_all_responses(runner)])
