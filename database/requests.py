from database.models import Category,Recipe,async_session


from sqlalchemy import select, delete


async def get_category():
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result
    
async def get_recipes():
    async with async_session() as session:
        result_recipe = await session.scalars(select(Recipe))
        return result_recipe
    
async def get_category_recipe(category_id, offset, limit):
    async with async_session() as session:
        result_recipe_cat = await session.scalars(
            select(Recipe).where(Recipe.category_id == category_id).offset(offset).limit(limit)
        )
        return result_recipe_cat.all()
    
async def get_recipe_i(recipe_id):
    async with async_session() as session:
        result_recipe_id = await session.scalar(
            select(Recipe).where(Recipe.id == recipe_id))
        return result_recipe_id

async def search_recipes(query: str):
    async with async_session() as session: 
        search_request = select(Recipe).where(Recipe.food_name.ilike(f'%{query}%'))
        result_search = await session.execute(search_request)
        return result_search.scalars().all()
    
async def add_recipe_db(recipe):
    async with async_session() as session:
        session.add(recipe)
        await session.commit()
        await session.refresh(recipe)
        return recipe
    
async def add_category_db(category):
    async with async_session() as session:
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category
    
async def delete_recipe(recipe_id):
    async with async_session() as session:
        await session.execute(
            delete(Recipe).where(Recipe.id == recipe_id))
        await session.commit()

async def delete_category_db(category_id):
    async with async_session() as session:
        await session.execute(
            delete(Category).where(Category.id == category_id))
        await session.commit()