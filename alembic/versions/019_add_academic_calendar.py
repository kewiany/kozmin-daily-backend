"""Add academic_calendar table

Revision ID: 019
Revises: 018
Create Date: 2026-04-12

"""
from datetime import date
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "019"
down_revision: Union[str, None] = "018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

YEAR = "2025/2026"

def _d(s: str) -> date:
    """Parse 'YYYY-MM-DD' string to date object."""
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))


def upgrade() -> None:
    table = op.create_table(
        "academic_calendar",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("academic_year", sa.String(20), nullable=False),
        sa.Column("study_mode", sa.String(50), nullable=False),
        sa.Column("semester", sa.String(20), nullable=False),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("college", sa.String(20), nullable=True),
    )

    rows = []

    # ── STUDIA STACJONARNE ──────────────────────────────────────────────

    # Semestr zimowy
    rows.append(dict(academic_year=YEAR, study_mode="stacjonarne", semester="zimowy", category="zajecia",
                     title="Zajęcia dydaktyczne", start_date=_d("2025-09-29"), end_date=_d("2026-01-30"), college=None))
    rows.append(dict(academic_year=YEAR, study_mode="stacjonarne", semester="zimowy", category="sesja",
                     title="Sesja egzaminacyjna", start_date=_d("2026-02-02"), end_date=_d("2026-02-13"), college=None))
    rows.append(dict(academic_year=YEAR, study_mode="stacjonarne", semester="zimowy", category="przerwa",
                     title="Przerwa międzysemestralna", start_date=_d("2026-02-16"), end_date=_d("2026-02-20"), college=None))
    rows.append(dict(academic_year=YEAR, study_mode="stacjonarne", semester="zimowy", category="poprawki",
                     title="Sesja poprawkowa", start_date=_d("2026-03-02"), end_date=_d("2026-03-20"), college=None))

    # Semestr letni
    rows.append(dict(academic_year=YEAR, study_mode="stacjonarne", semester="letni", category="zajecia",
                     title="Zajęcia dydaktyczne", start_date=_d("2026-02-23"), end_date=_d("2026-06-16"), college=None))
    rows.append(dict(academic_year=YEAR, study_mode="stacjonarne", semester="letni", category="sesja",
                     title="Sesja egzaminacyjna (KZiFiE)", start_date=_d("2026-06-17"), end_date=_d("2026-06-30"), college="KZiFiE"))
    rows.append(dict(academic_year=YEAR, study_mode="stacjonarne", semester="letni", category="sesja",
                     title="Sesja egzaminacyjna (KIBS)", start_date=_d("2026-06-17"), end_date=_d("2026-06-30"), college="KIBS"))
    rows.append(dict(academic_year=YEAR, study_mode="stacjonarne", semester="letni", category="sesja",
                     title="Sesja egzaminacyjna (KP)", start_date=_d("2026-06-17"), end_date=_d("2026-06-30"), college="KP"))
    rows.append(dict(academic_year=YEAR, study_mode="stacjonarne", semester="letni", category="poprawki",
                     title="Sesja poprawkowa", start_date=_d("2026-09-01"), end_date=_d("2026-09-16"), college=None))

    # ── STUDIA NIESTACJONARNE — ZJAZDY ──────────────────────────────────

    # KZiFiE — semestr zimowy
    kzifie_zim = [
        ("2025-10-04", "2025-10-05"), ("2025-10-18", "2025-10-19"),
        ("2025-11-08", "2025-11-09"), ("2025-11-15", "2025-11-16"),
        ("2025-11-22", "2025-11-23"), ("2025-12-06", "2025-12-07"),
        ("2025-12-13", "2025-12-14"), ("2026-01-10", "2026-01-11"),
        ("2026-01-17", "2026-01-18"), ("2026-01-24", "2026-01-25"),
        ("2026-02-07", "2026-02-08"),
    ]
    for i, (s, e) in enumerate(kzifie_zim, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="zimowy", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KZiFiE"))

    # KZiFiE — semestr letni
    kzifie_let = [
        ("2026-02-28", "2026-03-01"), ("2026-03-14", "2026-03-15"),
        ("2026-03-28", "2026-03-29"), ("2026-04-18", "2026-04-19"),
        ("2026-04-25", "2026-04-26"), ("2026-05-09", "2026-05-10"),
        ("2026-05-16", "2026-05-17"), ("2026-05-23", "2026-05-24"),
        ("2026-05-30", "2026-05-31"), ("2026-06-13", "2026-06-14"),
        ("2026-06-20", "2026-06-21"),
    ]
    for i, (s, e) in enumerate(kzifie_let, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="letni", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KZiFiE"))

    # KIBS — semestr zimowy
    kibs_zim = [
        ("2025-10-04", "2025-10-05"), ("2025-10-18", "2025-10-19"),
        ("2025-11-08", "2025-11-09"), ("2025-11-22", "2025-11-23"),
        ("2025-12-06", "2025-12-07"), ("2025-12-13", "2025-12-14"),
        ("2026-01-10", "2026-01-11"), ("2026-01-17", "2026-01-18"),
        ("2026-01-24", "2026-01-25"), ("2026-02-07", "2026-02-08"),
    ]
    for i, (s, e) in enumerate(kibs_zim, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="zimowy", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KIBS"))

    # KIBS — semestr letni
    kibs_let = [
        ("2026-02-28", "2026-03-01"), ("2026-03-14", "2026-03-15"),
        ("2026-03-28", "2026-03-29"), ("2026-04-18", "2026-04-19"),
        ("2026-04-25", "2026-04-26"), ("2026-05-09", "2026-05-10"),
        ("2026-05-16", "2026-05-17"), ("2026-05-23", "2026-05-24"),
        ("2026-06-06", "2026-06-07"), ("2026-06-13", "2026-06-14"),
        ("2026-06-20", "2026-06-21"),
    ]
    for i, (s, e) in enumerate(kibs_let, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="letni", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KIBS"))

    # KP — semestr zimowy
    kp_zim = [
        ("2025-10-04", "2025-10-05"), ("2025-10-18", "2025-10-19"),
        ("2025-11-08", "2025-11-09"), ("2025-11-15", "2025-11-16"),
        ("2025-11-29", "2025-11-30"), ("2025-12-13", "2025-12-14"),
        ("2026-01-10", "2026-01-11"), ("2026-01-17", "2026-01-18"),
        ("2026-01-24", "2026-01-25"), ("2026-02-07", "2026-02-08"),
    ]
    for i, (s, e) in enumerate(kp_zim, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="zimowy", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KP"))

    # KP — semestr letni
    kp_let = [
        ("2026-02-28", "2026-03-01"), ("2026-03-14", "2026-03-15"),
        ("2026-03-28", "2026-03-29"), ("2026-04-18", "2026-04-19"),
        ("2026-04-25", "2026-04-26"), ("2026-05-09", "2026-05-10"),
        ("2026-05-16", "2026-05-17"), ("2026-05-30", "2026-05-31"),
        ("2026-06-06", "2026-06-07"), ("2026-06-13", "2026-06-14"),
        ("2026-06-20", "2026-06-21"),
    ]
    for i, (s, e) in enumerate(kp_let, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="letni", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KP"))

    # ── STUDIA NIESTACJONARNE ONLINE — ZJAZDY ──────────────────────────

    # KZiFiE online — semestr zimowy
    kzifie_online_zim = [
        ("2025-10-04", "2025-10-05"), ("2025-10-18", "2025-10-19"),
        ("2025-11-08", "2025-11-09"), ("2025-11-15", "2025-11-16"),
        ("2025-11-22", "2025-11-23"), ("2025-12-06", "2025-12-07"),
        ("2025-12-13", "2025-12-14"), ("2026-01-10", "2026-01-11"),
        ("2026-01-17", "2026-01-18"), ("2026-01-24", "2026-01-25"),
        ("2026-02-07", "2026-02-08"),
    ]
    for i, (s, e) in enumerate(kzifie_online_zim, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="zimowy", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KZiFiE"))

    # KZiFiE online — semestr letni
    kzifie_online_let = [
        ("2026-02-28", "2026-03-01"), ("2026-03-14", "2026-03-15"),
        ("2026-03-28", "2026-03-29"), ("2026-04-18", "2026-04-19"),
        ("2026-04-25", "2026-04-26"), ("2026-05-09", "2026-05-10"),
        ("2026-05-16", "2026-05-17"), ("2026-05-23", "2026-05-24"),
        ("2026-05-30", "2026-05-31"), ("2026-06-13", "2026-06-14"),
        ("2026-06-20", "2026-06-21"),
    ]
    for i, (s, e) in enumerate(kzifie_online_let, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="letni", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KZiFiE"))

    # KIBS online — semestr zimowy
    kibs_online_zim = [
        ("2025-10-04", "2025-10-05"), ("2025-10-18", "2025-10-19"),
        ("2025-11-08", "2025-11-09"), ("2025-11-22", "2025-11-23"),
        ("2025-12-06", "2025-12-07"), ("2025-12-13", "2025-12-14"),
        ("2026-01-10", "2026-01-11"), ("2026-01-17", "2026-01-18"),
        ("2026-01-24", "2026-01-25"), ("2026-02-07", "2026-02-08"),
    ]
    for i, (s, e) in enumerate(kibs_online_zim, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="zimowy", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KIBS"))

    # KIBS online — semestr letni
    kibs_online_let = [
        ("2026-02-28", "2026-03-01"), ("2026-03-14", "2026-03-15"),
        ("2026-03-28", "2026-03-29"), ("2026-04-18", "2026-04-19"),
        ("2026-04-25", "2026-04-26"), ("2026-05-09", "2026-05-10"),
        ("2026-05-16", "2026-05-17"), ("2026-05-23", "2026-05-24"),
        ("2026-06-06", "2026-06-07"), ("2026-06-13", "2026-06-14"),
        ("2026-06-20", "2026-06-21"),
    ]
    for i, (s, e) in enumerate(kibs_online_let, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="letni", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KIBS"))

    # KP online — semestr zimowy
    kp_online_zim = [
        ("2025-10-04", "2025-10-05"), ("2025-10-18", "2025-10-19"),
        ("2025-11-08", "2025-11-09"), ("2025-11-15", "2025-11-16"),
        ("2025-11-29", "2025-11-30"), ("2025-12-13", "2025-12-14"),
        ("2026-01-10", "2026-01-11"), ("2026-01-17", "2026-01-18"),
        ("2026-01-24", "2026-01-25"), ("2026-02-07", "2026-02-08"),
    ]
    for i, (s, e) in enumerate(kp_online_zim, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="zimowy", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KP"))

    # KP online — semestr letni
    kp_online_let = [
        ("2026-02-28", "2026-03-01"), ("2026-03-14", "2026-03-15"),
        ("2026-03-28", "2026-03-29"), ("2026-04-18", "2026-04-19"),
        ("2026-04-25", "2026-04-26"), ("2026-05-09", "2026-05-10"),
        ("2026-05-16", "2026-05-17"), ("2026-05-30", "2026-05-31"),
        ("2026-06-06", "2026-06-07"), ("2026-06-13", "2026-06-14"),
        ("2026-06-20", "2026-06-21"),
    ]
    for i, (s, e) in enumerate(kp_online_let, 1):
        rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="letni", category="zjazd",
                         title=f"Zjazd {i}", start_date=_d(s), end_date=_d(e), college="KP"))

    # ── Niestacjonarne — sesje i przerwy ────────────────────────────────

    # Semestr zimowy
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="zimowy", category="sesja",
                     title="Sesja egzaminacyjna", start_date=_d("2026-02-02"), end_date=_d("2026-02-13"), college=None))
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="zimowy", category="przerwa",
                     title="Przerwa międzysemestralna", start_date=_d("2026-02-16"), end_date=_d("2026-02-20"), college=None))
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="zimowy", category="poprawki",
                     title="Sesja poprawkowa", start_date=_d("2026-03-02"), end_date=_d("2026-03-20"), college=None))

    # Semestr letni
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="letni", category="sesja",
                     title="Sesja egzaminacyjna (KZiFiE)", start_date=_d("2026-06-17"), end_date=_d("2026-06-30"), college="KZiFiE"))
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="letni", category="sesja",
                     title="Sesja egzaminacyjna (KIBS)", start_date=_d("2026-06-17"), end_date=_d("2026-06-30"), college="KIBS"))
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="letni", category="sesja",
                     title="Sesja egzaminacyjna (KP)", start_date=_d("2026-06-17"), end_date=_d("2026-06-30"), college="KP"))
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne", semester="letni", category="poprawki",
                     title="Sesja poprawkowa", start_date=_d("2026-09-01"), end_date=_d("2026-09-16"), college=None))

    # ── Niestacjonarne online — sesje i przerwy ────────────────────────

    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="zimowy", category="sesja",
                     title="Sesja egzaminacyjna", start_date=_d("2026-02-02"), end_date=_d("2026-02-13"), college=None))
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="zimowy", category="przerwa",
                     title="Przerwa międzysemestralna", start_date=_d("2026-02-16"), end_date=_d("2026-02-20"), college=None))
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="zimowy", category="poprawki",
                     title="Sesja poprawkowa", start_date=_d("2026-03-02"), end_date=_d("2026-03-20"), college=None))

    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="letni", category="sesja",
                     title="Sesja egzaminacyjna (KZiFiE)", start_date=_d("2026-06-17"), end_date=_d("2026-06-30"), college="KZiFiE"))
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="letni", category="sesja",
                     title="Sesja egzaminacyjna (KIBS)", start_date=_d("2026-06-17"), end_date=_d("2026-06-30"), college="KIBS"))
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="letni", category="sesja",
                     title="Sesja egzaminacyjna (KP)", start_date=_d("2026-06-17"), end_date=_d("2026-06-30"), college="KP"))
    rows.append(dict(academic_year=YEAR, study_mode="niestacjonarne_online", semester="letni", category="poprawki",
                     title="Sesja poprawkowa", start_date=_d("2026-09-01"), end_date=_d("2026-09-16"), college=None))

    op.bulk_insert(table, rows)


def downgrade() -> None:
    op.drop_table("academic_calendar")
