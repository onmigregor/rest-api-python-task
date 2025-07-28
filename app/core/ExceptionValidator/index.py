from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if exc.errors():
        err = exc.errors()[0]
        if err['type'] == 'missing' or err['msg'] == 'Field required':
            # El campo suele estar en la última posición de loc
            loc = err.get('loc', [])
            field = None
            if len(loc) > 1 and loc[0] == 'body':
                field = loc[1]
            elif len(loc) > 0:
                field = loc[-1]
            else:
                field = '<unknown>'
            msg = f"Field '{field}' is required"
        else:
            msg = err['msg']
    else:
        msg = "Validation error"
    return JSONResponse(
        status_code=422,
        content={"message": msg, "status": 422}
    )

async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    msg = exc.errors()[0]['msg'] if exc.errors() else "Validation error"
    return JSONResponse(
        status_code=422,
        content={"message": msg, "status": 422}
    )
