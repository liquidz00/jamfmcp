from pydantic import BaseModel


class V1Site(BaseModel):
    id: str | None = None
    name: str | None = None
