"""
Seed CLI for creating clubs and admins.

Usage:
    python -m app.seed add-club "Koło Naukowe AI" "ai_club" "password123"
    python -m app.seed add-admin "Admin Uczelni" "admin" "admin123"
"""

import asyncio
import sys

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import hash_password
from app.database import async_session, engine
from app.models import Club
from app.database import Base


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_club(name: str, login: str, password: str):
    await create_tables()
    async with async_session() as db:
        existing = await db.execute(select(Club).where(Club.login == login))
        if existing.scalar_one_or_none():
            print(f"Club with login '{login}' already exists.")
            return
        club = Club(
            name=name,
            login=login,
            password=hash_password(password),
            role="club",
        )
        db.add(club)
        await db.commit()
        print(f"Club '{name}' created (login: {login})")


async def add_admin(name: str, login: str, password: str):
    await create_tables()
    async with async_session() as db:
        existing = await db.execute(select(Club).where(Club.login == login))
        if existing.scalar_one_or_none():
            print(f"Admin with login '{login}' already exists.")
            return
        admin = Club(
            name=name,
            login=login,
            password=hash_password(password),
            role="admin",
        )
        db.add(admin)
        await db.commit()
        print(f"Admin '{name}' created (login: {login})")


def main():
    if len(sys.argv) < 5:
        print("Usage:")
        print('  python -m app.seed add-club "Name" "login" "password"')
        print('  python -m app.seed add-admin "Name" "login" "password"')
        sys.exit(1)

    command = sys.argv[1]
    name, login, password = sys.argv[2], sys.argv[3], sys.argv[4]

    if command == "add-club":
        asyncio.run(add_club(name, login, password))
    elif command == "add-admin":
        asyncio.run(add_admin(name, login, password))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
