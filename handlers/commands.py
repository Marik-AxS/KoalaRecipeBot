from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from .keyboards import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types
import emoji
router = Router()

admin_id = 1265349385

@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer(
        f"""Привет, {message.from_user.id}
у меня есть много рецептов, что хочешь приготовить?""",
        reply_markup=kb,
    )

@router.message(F.text == f'{emoji.emojize(":closed_book:")} Категории')
async def category_command(message: Message):
    await message.answer("Выберите категорию", reply_markup=await categories())

@router.callback_query(F.data.startswith('category_'))
async def select_category(callback: CallbackQuery):
    await callback.message.delete()
    category_id = int(callback.data.split('_')[1])
    await callback.message.answer(
        text='Рецепты по этой категории',
        reply_markup=await recipes(category_id=category_id, page=1),
    )

@router.callback_query(F.data.startswith('page_'))
async def paginate(callback: CallbackQuery):
    data = callback.data.split('_')
    category_id = int(data[1])
    page = int(data[2])
    await callback.message.edit_reply_markup(
        reply_markup=await recipes(category_id=category_id, page=page)
    )

@router.callback_query(F.data == 'back_to_categories')
async def back_to_categories(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text='Выберите категорию',
        reply_markup=await categories(),
    )

from random import randint

@router.message(F.text == f'{emoji.emojize(":game_die:")} Рандомный рецепт')
async def random_recipe(message: Message):
    recipe_id = randint(1, 16)
    recipe = await get_recipe_i(recipe_id)
    ingredients_before = recipe.ingredients.split(',')
    formatted_ingredients = '\n       '.join(ingredients_after.strip() for ingredients_after in ingredients_before)
    ingredients = formatted_ingredients
    if recipe.image.startswith('http') or recipe.image.startswith('AgAC'):
        photo = recipe.image
    else:
        photo = FSInputFile(recipe.image)
    await message.answer_photo(
        photo=photo,
        caption=f'{emoji.emojize(":curry_rice:")} Название: {recipe.food_name}\n{emoji.emojize(":hourglass_done:")} Время приготовления: {recipe.cooking_time}\n{emoji.emojize(":fork_and_knife_with_plate:")} Количество порций: {recipe.number_of_servings}\n{emoji.emojize(":scroll:")} Ингредиенты:\n       {ingredients}\n{emoji.emojize(":shallow_pan_of_food:")} Шаги приготовления: {recipe.description}'
    )


@router.callback_query(F.data.startswith('recipe_'))
async def select_recipe(callback: CallbackQuery):
    await callback.message.delete()
    recipe_id = int(callback.data.split('_')[1])
    recipe = await get_recipe_i(recipe_id)
    ingredients_before = recipe.ingredients.split(',')
    formatted_ingredients = '\n       '.join(ingredients_after.strip() for ingredients_after in ingredients_before)
    ingredients = formatted_ingredients
    user_id = callback.from_user.id
    if recipe.image.startswith('http') or recipe.image.startswith('AgAC'):
        photo = recipe.image
    else:
        photo = FSInputFile(recipe.image)
    if user_id == admin_id :
        reply_markup = await back_delete(recipe_id)
    else:
        reply_markup = await back()
    await callback.message.answer_photo(
        photo=photo,
        caption=f'{emoji.emojize(":curry_rice:")} Название: {recipe.food_name}\n{emoji.emojize(":hourglass_done:")} Время приготовления: {recipe.cooking_time}\n{emoji.emojize(":fork_and_knife_with_plate:")} Количество порций: {recipe.number_of_servings}\n{emoji.emojize(":scroll:")} Ингредиенты:\n       {ingredients}\n{emoji.emojize(":shallow_pan_of_food:")} Шаги приготовления: {recipe.description}',
        reply_markup=reply_markup
    )

class SearchRecipe(StatesGroup):
    search = State()

@router.message(F.text == f'{emoji.emojize(":magnifying_glass_tilted_right:")} Поиск')
async def search_command(message: Message, state: FSMContext):
    await message.answer("Напишите название рецепта или ключевое слово:")
    await state.set_state(SearchRecipe.search)

@router.message(SearchRecipe.search)
async def results_after_search(message: Message, state: FSMContext):
    search_query = message.text
    results = await search_recipes(search_query)
    user_id = message.from_user.id
    count = len(results)
    
    if count > 0:
        for recipe in results:
            if recipe.image.startswith('http') or recipe.image.startswith('AgAC'):
                photo = recipe.image
            else:
                photo = FSInputFile(recipe.image)
            ingredients_before = recipe.ingredients.split(',')
            formatted_ingredients = '\n       '.join(ingredients_after.strip() for ingredients_after in ingredients_before)
            ingredients = formatted_ingredients
            recipe_id = recipe.id
            if user_id == admin_id :
                reply_markup = await delete_to_search(recipe_id)
            else:
                reply_markup = None
            await message.answer_photo(
                photo=photo,
                caption=f'{emoji.emojize(":curry_rice:")} Название: {recipe.food_name}\n{emoji.emojize(":hourglass_done:")} Время приготовления: {recipe.cooking_time}\n{emoji.emojize(":fork_and_knife_with_plate:")} Количество порций: {recipe.number_of_servings}\n{emoji.emojize(":scroll:")} Ингредиенты:\n       {ingredients}\n{emoji.emojize(":shallow_pan_of_food:")} Шаги приготовления: {recipe.description}',
                reply_markup= reply_markup
    )
        await message.answer(f'{emoji.emojize(":magnifying_glass_tilted_right:")} Найдено рецептов по вашему запросу: {count}')
    else:
        await message.answer("Рецепты не найдены.")
    
    await state.clear()

@router.callback_query(F.data.startswith('delete_'))
async def recipe_delete(callback: CallbackQuery):
    recipe_id = int(callback.data.split('_')[1])
    await delete_recipe(recipe_id)
    await callback.answer('Рецепт успешно удален',
                          reply_markup= await categories())
    await callback.message.delete()

@router.callback_query(F.data.startswith('deletesearch_'))
async def delete_recipe_search(callback: CallbackQuery):
    recipe_id = int(callback.data.split('_')[1])
    await delete_recipe(recipe_id)
    await callback.answer('Рецепт успешно удален',
                          reply_markup=await categories())
    await callback.message.delete()

class AddRecipe(StatesGroup):
    food_name = State()
    ingredients = State()
    number_of_servings = State()
    cooking_time = State()
    description = State()
    image = State()
    category_id = State()

@router.message(F.text == f'{emoji.emojize(":plus:")} Добавить рецепт')
async def add_recipe(message: Message, state: FSMContext):
    await message.answer('Введите название блюда')
    await state.set_state(AddRecipe.food_name)

@router.message(AddRecipe.food_name, StateFilter(AddRecipe))
async def enter_food_name(message: Message, state: FSMContext):
    await state.update_data(food_name=message.text)
    await message.answer('Введите ингредиенты, каждую после запятой')
    await state.set_state(AddRecipe.ingredients)

@router.message(AddRecipe.ingredients, StateFilter(AddRecipe))
async def enter_ingredients(message: Message, state: FSMContext):
    await state.update_data(ingredients=message.text)
    await message.answer('Введите количество порций')
    await state.set_state(AddRecipe.number_of_servings)

@router.message(AddRecipe.number_of_servings, StateFilter(AddRecipe))
async def enter_number_of_servings(message: Message, state: FSMContext):
    await state.update_data(number_of_servings=message.text)
    await message.answer('Введите время приготовления')
    await state.set_state(AddRecipe.cooking_time)

@router.message(AddRecipe.cooking_time, StateFilter(AddRecipe))
async def enter_cooking_time(message: Message, state: FSMContext):
    await state.update_data(cooking_time=message.text)
    await message.answer('Введите шаги приготовления')
    await state.set_state(AddRecipe.description)

@router.message(AddRecipe.description, StateFilter(AddRecipe))
async def enter_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Отправьте фотографию блюда')
    await state.set_state(AddRecipe.image)

@router.message(AddRecipe.image, StateFilter(AddRecipe))
async def enter_food_image(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[0].file_id)
    await message.answer('Выберите категорию блюда', reply_markup=await categories_add_recipe())
    await state.set_state(AddRecipe.category_id)

@router.callback_query(AddRecipe.category_id, StateFilter(AddRecipe))
async def enter_game_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split('_')[1])
    data = await state.get_data()
    recipe = Recipe(
        food_name=data['food_name'],
        ingredients=data['ingredients'],
        number_of_servings=data['number_of_servings'],
        cooking_time=data['cooking_time'],
        description=data['description'],
        image=data['image'],
        category_id=category_id,
    )
    await add_recipe_db(recipe)
    await callback.message.answer('Рецепт успешно добавлен')
    await state.clear()

class AddCategory(StatesGroup):
    category_name = State()

@router.message(Command('add_category'))
async def add_category(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id == admin_id:
        await message.answer('Введите название категории')
        await state.set_state(AddCategory.category_name)
    else:
        None

@router.message(AddCategory.category_name)
async def down_category_name(message: Message, state: FSMContext):
    category_name = message.text
    await state.update_data(category_name=category_name)
    data = await state.get_data()
    category = Category(category_name=data['category_name'])
    await add_category_db(category)
    await message.answer('Категория успешно добавлена')
    await state.clear()

class DeleteCategory(StatesGroup):
    category = State()

@router.message(Command('delete_category'))
async def delete_category(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id == admin_id:
        await message.answer('Выберите категорию', reply_markup=await category_delete())
        await state.set_state(DeleteCategory.category)
    else: 
        None

@router.callback_query(DeleteCategory.category)
async def finish_delete(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split('_')[1])
    category_id = category_id
    await delete_category_db(category_id)
    await callback.message.answer('Категория успешно удалена')
    await state.clear()

@router.message(Command('admin_help'))
async def admin_help(message: Message):
    user_id = message.from_user.id
    if user_id == admin_id:
        await message.answer("""Доступные команды:\n
/add_category - Добавить категорию\n
/delete_category - Удалить категорию\n
/admin_help - Список команд""")
    else:
        None