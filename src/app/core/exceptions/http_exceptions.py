# ruff: noqa
from fastcrud.exceptions.http_exceptions import (
    CustomException,
    BadRequestException,
    NotFoundException,
    ForbiddenException,
    UnauthorizedException,
    UnprocessableEntityException,
    DuplicateValueException,
    RateLimitException
)
from fastapi import HTTPException
class ServerErrorException(HTTPException):
    def __init__(self, value: str):
        self.value = value
        super().__init__(status_code=500, detail="The server is having an error!")