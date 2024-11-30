from dotenv import load_dotenv
from sqlalchemy import Column, Integer, BigInteger, String, Numeric, TIMESTAMP
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine, class_=AsyncSession)
