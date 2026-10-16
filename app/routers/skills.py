from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Skill
from ..schemas import SkillCreate, SkillOut, SkillUpdate
from ..utils import commit_or_409, get_or_404
from ..security import require_admin

router = APIRouter(prefix="/skills", tags=["Ko'nikmalar"], dependencies=[Depends(require_admin)],)


@router.get("", response_model=list[SkillOut])
def list_skills(
    q: str | None = None,
    category: str | None = None,
    skip: int = 0,
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
):
    stmt = select(Skill).order_by(Skill.name)
    if q:
        stmt = stmt.where(or_(Skill.name.ilike(f"%{q}%"), Skill.category.ilike(f"%{q}%")))
    if category:
        stmt = stmt.where(Skill.category == category)
    return db.scalars(stmt.offset(skip).limit(limit)).all()



@router.post(
    "",
    response_model=SkillOut,
    status_code=201,
    dependencies=[Depends(require_admin)],
)
def create_skill(data: SkillCreate, db: Session = Depends(get_db)):
    skill = Skill(**data.model_dump())
    db.add(skill)
    commit_or_409(db, "Bu nomli ko'nikma allaqachon mavjud")
    db.refresh(skill)
    return skill


@router.patch(
    "/{skill_id}",
    response_model=SkillOut,
    dependencies=[Depends(require_admin)],
)
def update_skill(
    skill_id: int,
    data: SkillUpdate,
    db: Session = Depends(get_db),
):
    skill = get_or_404(db, Skill, skill_id, "Ko'nikma")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(skill, key, value)
    commit_or_409(db, "Ma'lumot yaroqsiz yoki bu nom band")
    db.refresh(skill)
    return skill


@router.delete(
    "/{skill_id}",
    status_code=204,
    dependencies=[Depends(require_admin)],
)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = get_or_404(db, Skill, skill_id, "Ko'nikma")
    db.delete(skill)
    commit_or_409(db, "Bu ko'nikma almashuvlarda ishlatilgan, o'chirib bo'lmaydi")
