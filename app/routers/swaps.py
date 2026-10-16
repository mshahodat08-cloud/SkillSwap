from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Swap, User
from ..schemas import SwapCreate, SwapOut, SwapStatus, SwapUpdate
from ..utils import commit_or_409, ensure_skills, get_or_404
from ..security import require_admin

router = APIRouter(prefix="/swaps", tags=["Almashuvlar"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[SwapOut])
def list_swaps(
    status: SwapStatus | None = None,
    user_id: int | None = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Swap).order_by(Swap.id.desc())
    if status:
        stmt = stmt.where(Swap.status == status)
    if user_id:
        stmt = stmt.where((Swap.requester_id == user_id) | (Swap.partner_id == user_id))
    return db.scalars(stmt.offset(skip).limit(limit)).all()


@router.post("", response_model=SwapOut, status_code=201)
def create_swap(data: SwapCreate, db: Session = Depends(get_db)):
    if data.requester_id == data.partner_id:
        raise HTTPException(400, "Foydalanuvchi o'zi bilan almasha olmaydi")
    for uid in (data.requester_id, data.partner_id):
        user = get_or_404(db, User, uid, "Foydalanuvchi")
        if user.status == "bloklangan":
            raise HTTPException(400, f"{user.full_name} bloklangan")
    ensure_skills(db, data.offered_skill_id, data.wanted_skill_id)
    swap = Swap(**data.model_dump())
    db.add(swap)
    commit_or_409(db, "Almashuvni saqlab bo'lmadi")
    db.refresh(swap)
    return swap


@router.get("/{swap_id}", response_model=SwapOut)
def get_swap(swap_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Swap, swap_id, "Almashuv")


@router.patch("/{swap_id}", response_model=SwapOut)
def update_swap(swap_id: int, data: SwapUpdate, db: Session = Depends(get_db)):
    swap = get_or_404(db, Swap, swap_id, "Almashuv")
    changes = data.model_dump(exclude_unset=True)
    ensure_skills(db, changes.get("offered_skill_id"), changes.get("wanted_skill_id"))
    for key, value in changes.items():
        setattr(swap, key, value)
    commit_or_409(db, "Ma'lumot yaroqsiz")
    db.refresh(swap)
    return swap


@router.delete("/{swap_id}", status_code=204)
def delete_swap(swap_id: int, db: Session = Depends(get_db)):
    swap = get_or_404(db, Swap, swap_id, "Almashuv")
    db.delete(swap)
    db.commit()
