from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from bot.keyboards.builder import db_keyboard
from bot.keyboards.contact_us import contact_us_keyboard
from bot.keyboards.delivery_type import delivery_keyboard
from bot.keyboards.join_us import join_us_inline_keyboard
from bot.keyboards.location import location_keyboard
from bot.keyboards.menu import menu_keyboard
from bot.keyboards.regions import REGIONS, regions_keyboard
from bot.keyboards.settings import settings_keyboard
from bot.states.menu import MenuState
from bot.states.to_order import OrderState
from bot.sync_to_async.orders import *

router = Router()

@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
    await state.set_state(MenuState.region)
    await message.answer(text="Assalomu alaykum! Les Ailes yetkazib berish xizmatiga xush kelibsiz.\n"
                              "Qaysi shaharda yashaysiz?\n Iltimos, shaharni tanlang:",
                         reply_markup=regions_keyboard())

@router.message(lambda message: message.text in REGIONS, MenuState.region)
async def region(message: Message, state: FSMContext):
    await state.set_state(MenuState.menu)
    await message.answer(text="Bosh menyu", reply_markup=menu_keyboard())

@router.message(MenuState.menu)
async def menu(message: Message, state: FSMContext):
    match message.text:
        case "🛍 Buyurtma berish":
            await state.set_state(MenuState.to_order)
            await message.answer(text="Buyurtmani o'zingiz 🙋‍♂️ olib keting yoki Yetkazib berishni 🚙 tanlang",
                                 reply_markup=delivery_keyboard())

        case "📖 Buyurtmalar tarixi":
            await message.answer(text="Sizning buyurtmalaringiz yo'q")
            return

        case "⚙️Sozlash ℹ️ Ma'lumotlar":
            await state.set_state(MenuState.settings)
            await message.answer(text="Harakatni tanlang:", reply_markup=settings_keyboard())

        case "🔥 Aksiya":
            await state.set_state(MenuState.sales)
            await message.answer(text="Shahringizda hali aksiyalar mavjud emas")

        case "🙋🏻‍♂️ Jamoamizga qo'shiling":
            await state.set_state(MenuState.join_us)
            await message.answer(
                text="Ahil jamoamizda ishlashga taklif qilamiz! Telegramdan chiqmay, shu yerning o'zida anketani to'ldirish uchun quyidagi tugmani bosing.",
                reply_markup=join_us_inline_keyboard)

        case "🙋☎️ Les Ailes bilan aloqa":
            await state.set_state(MenuState.contact_us)
            await message.answer(text="Agar siz bizga yozsangiz yoki sharh qoldirmoqchi bo'lsangiz, xursand bo'lamiz.",
                                 reply_markup=contact_us_keyboard)

        case _:
            await state.set_state(MenuState.menu)

@router.message(MenuState.to_order)
async def to_order(message: Message, state: FSMContext):
    if message.text == "⬅️ Ortga":
        await state.set_state(MenuState.menu)
        await message.answer(text="Bosh menyu", reply_markup=menu_keyboard())
        return

    if message.text == "🏃 Olib ketish":
        await state.set_state(OrderState.delivery_type)
        await message.answer(text="Qayerdasiz 👀? Agar lokatsiyangizni📍 yuborsangiz, "
                                  "sizga eng yaqin filialni aniqlaymiz",
                             reply_markup=location_keyboard()
                             )

@router.message(OrderState.delivery_type)
async def delivery_type(message: Message, state: FSMContext):
    if message.text == "⬅️ Ortga":
        await state.set_state(MenuState.to_order)
        await message.answer(text="Buyurtmani o'zingiz 🙋‍♂️ olib keting yoki Yetkazib berishni 🚙 tanlang",
                             reply_markup=delivery_keyboard())
        return

    if "Filialni tanlang" in message.text:
        branches = await get_all_branches()
        await state.set_state(OrderState.branches)
        await message.answer(text="Qaysi filialdan olib ketishni tanlang",
                             reply_markup=db_keyboard(branches))

@router.message(OrderState.branches)
async def branches(message: Message, state: FSMContext):
    if message.text == "⬅️ Ortga":
        await state.set_state(OrderState.delivery_type)
        await message.answer(text="Qayerdasiz 👀? Agar lokatsiyangizni📍 yuborsangiz, "
                                  "sizga eng yaqin filialni aniqlaymiz",
                             reply_markup=location_keyboard()
                             )
        return

    await state.set_state(OrderState.categories)
    branch = await get_branch_by_title(message.text)
    if not branch:
        await message.answer("Filial topilmadi. Iltimos, qaytadan tanlang.")
        return

    categories = await get_all_categories()
    await message.answer(text=f"{branch.title}\n"
                              f"Manzil: {branch.location} \n"
                              f"Mo'ljal: {branch.target} \n"
                              f"Ish vaqti: {branch.working_hours}\n",
                         )
    await message.answer(text="Nimadan boshlaymiz?", reply_markup=db_keyboard(categories))

@router.message(OrderState.categories)
async def categories(message: Message, state: FSMContext):
    if message.text == "⬅️ Ortga":
        await state.set_state(OrderState.branches)
        await message.answer(text="Qaysi filialdan olib ketishni tanlang",
                             reply_markup=db_keyboard(branches))
        return

    await state.set_state(OrderState.products)
    products = await get_products_by_category(message.text)
    if not products:
        await message.answer("Bu kategoriyada mahsulotlar topilmadi")
        return

    await message.answer(text="Nimadan boshlaymiz?", reply_markup=db_keyboard(products))

@router.message(OrderState.products)
async def products(message: Message, state: FSMContext):
    if message.text == "⬅️ Ortga":
        await state.set_state(OrderState.categories)
        categories = await get_all_categories()
        await message.answer(text="Nimadan boshlaymiz?", reply_markup=db_keyboard(categories))
        return

    product = await sync_to_async(Product.objects.filter(title=message.text).first)()
    if not product:
        await message.answer("Mahsulot topilmadi")
        return

    try:
        if product.image:
            photo = FSInputFile(product.image.path)
            await message.answer_photo(
                photo=photo,
                caption=f"📦 {product.title}\n\n"
                        f"{product.description}\n\n"
                        f"💰 Narxi: {product.price:,} so'm"
            )
        else:
            await message.answer(
                text=f"📦 {product.title}\n\n"
                     f"{product.description}\n\n"
                     f"💰 Narxi: {product.price:,} so'm"
            )
    except Exception as e:
        await message.answer(
            text=f"📦 {product.title}\n\n"
                 f"{product.description}\n\n"
                 f"💰 Narxi: {product.price:,} so'm"
        )
