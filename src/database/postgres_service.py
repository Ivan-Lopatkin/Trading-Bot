from sqlalchemy import insert, select
from src.database.database import async_session_maker, engine
from src.models import User, Base, Transaction, Portfolio


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database initialized successully")
    except Exception as e:
        print(f"Exception: {e}")


class PostgresManager:
    async def add_user(self, telegram_id: int, username: str) -> None:
        async with async_session_maker() as session:
            stm = insert(User).values(
                telegram_id=telegram_id,
                username=username
            )
            await session.execute(stm)
            await session.commit()

    async def user_exists(self, telegram_id: int) -> bool:
        async with async_session_maker() as session:
            result = await session.execute(
                select(User).filter_by(telegram_id=telegram_id)
            )
            user = result.scalars().first()
            return user is not None

    async def get_user_by_telegram_id(self, telegram_id: int) -> User:
        async with async_session_maker() as session:
            result = session.query(User).filter(
                User.telegram_id == telegram_id).first()
            return result

    async def update_user_balance(self, telegram_id: int, new_balance: float):
        async with async_session_maker() as session:
            user = session.query(User).filter(telegram_id=telegram_id)
            if user:
                user.balance = new_balance
                session.commit()

    async def create_transaction(self, user_id: int, type: str, asset: str, amount: int, price: float, total: float):
        async with async_session_maker() as session:
            transaction = Transaction(
                user_id=user_id,
                type=type,
                asset=asset,
                amount=amount,
                price=price,
                total=total
            )
            session.add(transaction)
            session.commit()

    async def get_transactions_by_user_id(self, user_id: int):
        async with async_session_maker() as session:
            result = session.query(Transaction).filter(
                Transaction.user_id == user_id).all()

    async def upsert_portfolio(self, user_id: int, asset: str, quantity: int, value: float):
        async with async_session_maker() as session:
            portfolio = session.query(Portfolio).filter(
                Portfolio.user_id == user_id,
                Portfolio.asset == asset
            ).first()

            if portfolio:
                old_quantity = portfolio.quantity
                old_value = portfolio.value
                portfolio.quantity += + quantity

                if value != old_value:
                    new_value = ((old_value * old_quantity) +
                                 (value * quantity)) / (old_quantity + quantity)
                    portfolio.value = new_value
            else:
                portfolio = Portfolio(
                    user_id=user_id, asset=asset, quantity=quantity, value=value)
                session.add(portfolio)

            session.commit()
