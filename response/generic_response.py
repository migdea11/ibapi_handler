from typing import Dict


class GenericResponse():
    GENERIC_TYPE = 'generic'

    def __init__(self, req_id: str, properties: Dict[str, str]):
        self.response_type = self.GENERIC_TYPE
        self.req_id = req_id
        self.properties = properties
