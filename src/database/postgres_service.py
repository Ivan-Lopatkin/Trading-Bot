from sqlalchemy import insert, delete
from src.database.database import async_session_maker
from src.database.models import User, Transaction


class PostgresManager:
    async def add_user(self, telegram_id: int, username: str, bio: str) -> None:
        async with async_session_maker() as session:
            stm = insert(User).values(
                telegram_id=telegram_id,
                username=username,
                bio=bio
            )
            await session.execute(stm)
            await session.commit()
