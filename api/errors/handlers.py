from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import BaseAPIException


async def api_exeption_handler(request: Request, exc: BaseAPIException):
   return JSONResponse(status_code=exc.error_code, content={"message": exc.message})