from typing import Optional

from pydantic import BaseModel


class ScenarioBase(BaseModel):
    name: str
    level_min: str
    level_max: str
    description: Optional[str] = None
    situation: Optional[str] = None
    dialogue_script: Optional[dict] = None


class ScenarioCreate(ScenarioBase):
    pass


class ScenarioUpdate(BaseModel):
    name: Optional[str] = None
    level_min: Optional[str] = None
    level_max: Optional[str] = None
    description: Optional[str] = None
    situation: Optional[str] = None
    dialogue_script: Optional[dict] = None


class ScenarioOut(ScenarioBase):
    id: int
