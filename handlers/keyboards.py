from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
from database.requests import *
import emoji

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f'{emoji.emojize(":magnifying_glass_tilted_right:")} Поиск')],
    [KeyboardButton(text=f'{emoji.emojize(":closed_book:")} Категории')],
    [KeyboardButton(text=f'{emoji.emojize(":game_die:")} Рандомный рецепт')],
    [KeyboardButton(text=f'{emoji.emojize(":plus:")} Добавить рецепт')]
],resize_keyboard=True,input_field_placeholder='Выберите кнопку',
one_time_keyboard=True)

async def categories():
    category_kb = InlineKeyboardBuilder()
    categories = await get_category()
    for category in categories:
        category_kb.add(InlineKeyboardButton(
            text=category.category_name.capitalize(),
            callback_data=f'category_{category.id}'
        ))
    return category_kb.adjust(2).as_markup()

async def categories_add_recipe():
    category_kb = InlineKeyboardBuilder()
    categories = await get_category()
    for category in categories:
        category_kb.add(InlineKeyboardButton(
            text=category.category_name,
            callback_data=f'categoriesaddrecipe_{category.id}'
        ))
    return category_kb.adjust(2).as_markup()

PAGE_SIZE = 6
async def recipes(category_id, page):
    offset = (page - 1) * PAGE_SIZE
    recipes_kb = InlineKeyboardBuilder()
    all_recipes = await get_category_recipe(category_id=category_id, offset=offset, limit=PAGE_SIZE)
    
    for recipe in all_recipes:
        recipes_kb.add(InlineKeyboardButton(
            text=recipe.food_name,
            callback_data=f'recipe_{recipe.id}'
        ))
    
    if page == 1:
        recipes_kb.add(InlineKeyboardButton(
            text=f'{emoji.emojize(":left_arrow:")}',
            callback_data=f'back_to_categories'
        ))

    if page > 1:
        recipes_kb.add(InlineKeyboardButton(
            text=f'{emoji.emojize(":left_arrow:")}',
            callback_data=f'page_{category_id}_{page-1}'
        ))
    if len(all_recipes) == PAGE_SIZE:
            recipes_kb.add(InlineKeyboardButton(
            text=f'{emoji.emojize(":right_arrow:")}',
            callback_data=f'page_{category_id}_{page+1}'
        ))
    return recipes_kb.adjust(2).as_markup()

async def back():
    back_kb = InlineKeyboardBuilder()
    back_kb.add(InlineKeyboardButton(
        text='Назад',
        callback_data='back_to_categories'))
    return back_kb.as_markup()

async def back_delete(recipe_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data=f'back_to_categories')],
        [InlineKeyboardButton(text='Удалить', callback_data=f'delete_{recipe_id}')]
    ])
    return kb

async def delete_to_search(recipe_id):
    delete_kb = InlineKeyboardBuilder()
    delete_kb.add(InlineKeyboardButton(
        text='Удалить',
        callback_data=f'deletesearch_{recipe_id}'))
    return delete_kb.as_markup()

async def category_delete():
    category_kb = InlineKeyboardBuilder()
    categories = await get_category()
    for category in categories:
        category_kb.add(InlineKeyboardButton(
            text=category.category_name,
            callback_data=f'categorydelete_{category.id}'
        ))
    return category_kb.adjust(2).as_markup()