from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase,relationship,mapped_column,Mapped,Session
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from config import MYSQL_URL

engine = create_async_engine(MYSQL_URL,echo=True)

async_session = async_sessionmaker(engine)

class Base(DeclarativeBase,AsyncAttrs):
    pass


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(100))
    recipes = relationship('Recipe', back_populates='category')

class   Recipe(Base):
    __tablename__ = 'recipe'

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    food_name: Mapped[str] = mapped_column(String(100))
    number_of_servings: Mapped[int] = mapped_column(Integer)
    cooking_time: Mapped[str] = mapped_column(String(50))
    image: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(500))
    ingredients: Mapped[str] = mapped_column(String(300))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category = relationship('Category',back_populates='recipes')  

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
