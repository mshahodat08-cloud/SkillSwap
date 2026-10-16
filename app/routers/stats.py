from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from ..security import require_admin

from ..database import get_db
from ..models import Skill, Swap, User

router = APIRouter(prefix="/stats", tags=["Statistika"], dependencies=[Depends(require_admin)])


@router.get("")
def dashboard_stats(db: Session = Depends(get_db)):
    total_users = db.scalar(select(func.count(User.id)))
    by_status = dict(db.execute(select(Swap.status, func.count()).group_by(Swap.status)).all())
    top = db.execute(
        select(Skill.name, func.count(Swap.id).label("total"))
        .join(Swap, Swap.offered_skill_id == Skill.id)
        .group_by(Skill.id, Skill.name)
        .order_by(func.count(Swap.id).desc())
        .limit(5)
    ).all()
    return {
        "total_users": total_users,
        "swaps": {
            "kutilmoqda": by_status.get("kutilmoqda", 0),
            "tasdiqlangan": by_status.get("tasdiqlangan", 0),
            "rad": by_status.get("rad", 0),
        },
        "top_skills": [{"name": n, "count": c} for n, c in top],
    }
