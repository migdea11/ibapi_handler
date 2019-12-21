from response.generic_response import GenericResponse
from typing import Dict


class ContractResponse(GenericResponse):
    CONTRACT_TYPE = 'contract'

    def __init__(self, req_id: str, contract_id: str, symbol: str, properties: Dict[str, str]):
        GenericResponse.__init__(self, req_id=req_id, properties=properties)
        self.response_type = self.CONTRACT_TYPE
        self.contract_id = contract_id
        self.symbol = symbol
