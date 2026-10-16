from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Skill


def get_or_404(db: Session, model, obj_id: int, label: str = "Obyekt"):
    obj = db.get(model, obj_id)
    if obj is None:
        raise HTTPException(404, f"{label} topilmadi")
    return obj


def ensure_skills(db: Session, *skill_ids: int | None) -> None:
    for sid in skill_ids:
        if sid is not None:
            get_or_404(db, Skill, sid, "Ko'nikma")


def commit_or_409(db: Session, message: str) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, message)
