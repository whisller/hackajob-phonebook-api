class AppException(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class DoesNotExistException(AppException):
    def __init__(self, message, status_code=404):
        self.message = message
        self.status_code = status_code


class GeneralException(AppException):
    def __init__(self, message='There was problem on the server.', status_code=500):
        self.message = message
        self.status_code = status_code
