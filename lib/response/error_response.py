from lib.response.generic_response import GenericResponse


class ErrorResponse(GenericResponse):
    ERROR_TYPE = 'error'

    def __init__(self, req_id: int, code: int, error: str):
        GenericResponse.__init__(self, req_id=req_id, properties={})
        self.response_type = self.ERROR_TYPE
        self.error_code = code
        self.error_message = error
