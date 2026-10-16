# SkillSwap Backend (FastAPI + SQLite)

## Ishga tushirish
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux
pip install -r requirements.txt
python seed.py                 # namuna ma'lumotlar (ixtiyoriy)
uvicorn app.main:app --reload
```
Brauzerda oching: http://127.0.0.1:8000/docs (barcha endpointlarni shu yerda sinab ko'rasiz)

## Endpointlar
| Resurs | Yaratish | Ro'yxat | Bittasi | Yangilash | O'chirish |
|---|---|---|---|---|---|
| Foydalanuvchilar | POST /users | GET /users | GET /users/{id} | PATCH /users/{id} | DELETE /users/{id} |
| Ko'nikmalar | POST /skills | GET /skills | GET /skills/{id} | PATCH /skills/{id} | DELETE /skills/{id} |
| Almashuvlar | POST /swaps | GET /swaps | GET /swaps/{id} | PATCH /swaps/{id} | DELETE /swaps/{id} |

Qo'shimcha: `GET /stats` (dashboard uchun), `GET /users?q=aziza&status=faol`, `GET /swaps?status=kutilmoqda`.

## Struktura
```
app/
  database.py   baza ulanishi
  models.py     jadvallar
  schemas.py    kiruvchi/chiquvchi ma'lumot qoidalari
  utils.py      umumiy yordamchi funksiyalar
  routers/      users.py, skills.py, swaps.py, stats.py
  main.py       ilova va CORS
seed.py         namuna ma'lumotlar
```
