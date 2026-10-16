from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    category: Mapped[str] = mapped_column(String(80))
    description: Mapped[str | None] = mapped_column(String(300))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="faol")
    teach_skill_id: Mapped[int | None] = mapped_column(ForeignKey("skills.id", ondelete="SET NULL"))
    learn_skill_id: Mapped[int | None] = mapped_column(ForeignKey("skills.id", ondelete="SET NULL"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    teach_skill = relationship("Skill", foreign_keys=[teach_skill_id])
    learn_skill = relationship("Skill", foreign_keys=[learn_skill_id])


class Swap(Base):
    __tablename__ = "swaps"

    id: Mapped[int] = mapped_column(primary_key=True)
    requester_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    partner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    offered_skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    wanted_skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    status: Mapped[str] = mapped_column(String(20), default="kutilmoqda")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    requester = relationship("User", foreign_keys=[requester_id])
    partner = relationship("User", foreign_keys=[partner_id])
    offered_skill = relationship("Skill", foreign_keys=[offered_skill_id])
    wanted_skill = relationship("Skill", foreign_keys=[wanted_skill_id])
