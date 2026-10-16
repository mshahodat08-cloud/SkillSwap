"""Bazani namuna ma'lumotlar bilan to'ldiradi: python seed.py"""
from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Skill, Swap, User

SKILLS = [
    ("Python", "Dasturlash"), ("JavaScript", "Dasturlash"),
    ("Ingliz tili", "Tillar"), ("Rus tili", "Tillar"),
    ("Dizayn", "Dizayn"), ("Rasm chizish", "Dizayn"),
    ("Gitara", "Musiqa"), ("Fotografiya", "Fotografiya"), ("Shaxmat", "Shaxmat"),
]
# (ism, email, o'rgatadi, o'rganadi, holat)
USERS = [
    ("Aziza Karimova", "aziza@mail.uz", "Ingliz tili", "Python", "faol"),
    ("Jasur Toshmatov", "jasur@mail.uz", "Python", "Gitara", "faol"),
    ("Malika Yusupova", "malika@mail.uz", "Rasm chizish", "Ingliz tili", "faol"),
    ("Bobur Rahimov", "bobur@mail.uz", "Gitara", "Dizayn", "bloklangan"),
    ("Nodira Aliyeva", "nodira@mail.uz", "Dizayn", "JavaScript", "faol"),
    ("Sardor Qodirov", "sardor@mail.uz", "JavaScript", "Fotografiya", "faol"),
    ("Dilnoza Ergasheva", "dilnoza@mail.uz", "Fotografiya", "Rus tili", "faol"),
    ("Otabek Mirzayev", "otabek@mail.uz", "Rus tili", "Shaxmat", "bloklangan"),
]
# (so'rovchi email, sherik email, taklif qilingan, kerakli, holat)
SWAPS = [
    ("aziza@mail.uz", "jasur@mail.uz", "Ingliz tili", "Python", "kutilmoqda"),
    ("malika@mail.uz", "nodira@mail.uz", "Rasm chizish", "Dizayn", "kutilmoqda"),
    ("sardor@mail.uz", "dilnoza@mail.uz", "JavaScript", "Fotografiya", "kutilmoqda"),
    ("jasur@mail.uz", "bobur@mail.uz", "Python", "Gitara", "tasdiqlangan"),
    ("otabek@mail.uz", "aziza@mail.uz", "Rus tili", "Ingliz tili", "rad"),
]

Base.metadata.create_all(engine)
with SessionLocal() as db:
    if db.scalar(select(Skill)):
        raise SystemExit("Baza bo'sh emas, seed o'tkazib yuborildi.")
    skills = {n: Skill(name=n, category=c) for n, c in SKILLS}
    db.add_all(skills.values())
    users = {
        e: User(full_name=n, email=e, status=s, teach_skill=skills[t], learn_skill=skills[l])
        for n, e, t, l, s in USERS
    }
    db.add_all(users.values())
    db.flush()
    for r, p, o, w, s in SWAPS:
        db.add(Swap(requester=users[r], partner=users[p],
                    offered_skill=skills[o], wanted_skill=skills[w], status=s))
    db.commit()
print("Tayyor: namuna ma'lumotlar qo'shildi.")
