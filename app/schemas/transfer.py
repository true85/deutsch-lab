from typing import Any, Optional

from pydantic import BaseModel


class TransferPayload(BaseModel):
    user_id: int
    data: dict[str, list[dict[str, Any]]]
    mode: Optional[str] = "upsert"
