from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

UserStatus = Literal["faol", "bloklangan"]
SwapStatus = Literal["kutilmoqda", "tasdiqlangan", "rad"]


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- Skill ----------
class SkillCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    category: str = Field(min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=300)


class SkillUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    category: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=300)


class SkillOut(ORM):
    id: int
    name: str
    category: str
    description: str | None


# ---------- User ----------
class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    status: UserStatus = "faol"
    teach_skill_id: int | None = None
    learn_skill_id: int | None = None


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None
    status: UserStatus | None = None
    teach_skill_id: int | None = None
    learn_skill_id: int | None = None


class UserShort(ORM):
    id: int
    full_name: str


class UserOut(ORM):
    id: int
    full_name: str
    email: str
    status: UserStatus
    created_at: datetime
    teach_skill: SkillOut | None
    learn_skill: SkillOut | None


# ---------- Swap ----------
class SwapCreate(BaseModel):
    requester_id: int
    partner_id: int
    offered_skill_id: int
    wanted_skill_id: int


class SwapUpdate(BaseModel):
    status: SwapStatus | None = None
    offered_skill_id: int | None = None
    wanted_skill_id: int | None = None


class SwapOut(ORM):
    id: int
    status: SwapStatus
    created_at: datetime
    requester: UserShort
    partner: UserShort
    offered_skill: SkillOut
    wanted_skill: SkillOut
