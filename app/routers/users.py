from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserOut, UserStatus, UserUpdate
from ..utils import commit_or_409, ensure_skills, get_or_404
from ..security import require_admin

router = APIRouter(
    prefix="/users",
    tags=["Foydalanuvchilar"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=list[UserOut])
def list_users(
    q: str | None = None,
    status: UserStatus | None = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(User).order_by(User.id.desc())
    if q:
        stmt = stmt.where(or_(User.full_name.ilike(f"%{q}%"), User.email.ilike(f"%{q}%")))
    if status:
        stmt = stmt.where(User.status == status)
    return db.scalars(stmt.offset(skip).limit(limit)).all()


@router.post("", response_model=UserOut, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    ensure_skills(db, data.teach_skill_id, data.learn_skill_id)
    user = User(**data.model_dump())
    db.add(user)
    commit_or_409(db, "Bu email allaqachon ro'yxatdan o'tgan")
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, User, user_id, "Foydalanuvchi")


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = get_or_404(db, User, user_id, "Foydalanuvchi")
    changes = data.model_dump(exclude_unset=True)
    ensure_skills(db, changes.get("teach_skill_id"), changes.get("learn_skill_id"))
    for key, value in changes.items():
        setattr(user, key, value)
    commit_or_409(db, "Ma'lumot yaroqsiz yoki email band")
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_or_404(db, User, user_id, "Foydalanuvchi")
    db.delete(user)  # uning almashuvlari ham avtomatik o'chadi (CASCADE)
    db.commit()
