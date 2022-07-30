from typing import Any
from pydantic import BaseModel


class ResponseResultEvents(BaseModel):
    metadata: Any
    snapshot: Any
    state: Any | None


class ResponseResult(BaseModel):
    type: str = "init"
    events: list[ResponseResultEvents]
