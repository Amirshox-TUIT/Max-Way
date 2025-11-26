from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from django.utils.translation import gettext as _, activate

from bot.keyboards.builder import db_keyboard
from bot.keyboards.contact_us import contact_us_keyboard
from bot.keyboards.delivery_type import delivery_keyboard
from bot.keyboards.join_us import join_us_inline_keyboard
from bot.keyboards.language import get_language_keyboard
from bot.keyboards.location import location_keyboard
from bot.keyboards.menu import menu_keyboard
from bot.keyboards.settings import settings_keyboard
from bot.states.menu import MenuState
from bot.states.to_order import OrderState
from bot.sync_to_async.orders import *
from bot.sync_to_async.translation import get_or_create_user, set_user_language, get_user_language

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    """Start command handler"""
    user = message.from_user

    # Create or update user in database (await async function)
    user, created = await get_or_create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    if created:
        welcome_text = """
Assalomu alaykum! Les Ailes yetkazib berish xizmatiga xush kelibsiz.

Здравствуйте! Добро пожаловать в службу доставки Les Ailes.

Hello! Welcome to Les Ailes delivery service.
"""
        await message.answer(
            welcome_text,
            reply_markup=await get_language_keyboard()
        )
    else:
        await state.set_state(MenuState.region)
        language_code = await get_user_language(user_id=user.id)
        activate(language_code)
        regions = await get_all_regions()
        text = _("Bosh menyuga xush kelibsiz 😊")
        await message.answer(
            text,
            reply_markup=db_keyboard(regions, language_code)
        )

@router.callback_query(F.data.startswith("lang_"))
async def change_language(callback: CallbackQuery, state: FSMContext):
    """Handle language change"""
    language_code = callback.data.split("_")[1]  # Extract language code
    user_id = callback.from_user.id

    # Update user's language (await async function)
    await set_user_language(user_id, language_code)

    # Activate new language for response
    from django.utils.translation import activate
    activate(language_code)
    regions = await get_all_regions()
    await state.set_state(MenuState.region)
    await callback.message.answer(text=_("Assalomu alaykum! Les Ailes yetkazib berish xizmatiga xush kelibsiz.\n"
                                "Qaysi shaharda yashaysiz?\n Iltimos, shaharni tanlang:"),
                         reply_markup=db_keyboard(regions, language_code))


@router.message(MenuState.region)
async def region(message: Message, state: FSMContext):
    await state.set_state(MenuState.menu)
    await message.answer(text=_("Bosh menyu"), reply_markup=menu_keyboard())


@router.message(MenuState.menu)
async def menu(message: Message, state: FSMContext):
    match message.text:
        case "🛍 Buyurtma berish" | "🛒 Make an order":
            await state.set_state(MenuState.to_order)
            await message.answer(text=_("Buyurtmani o'zingiz 🙋‍♂️ olib keting yoki Yetkazib berishni 🚙 tanlang"),
                                 reply_markup=delivery_keyboard())

        case "📖 Buyurtmalar tarixi" | "📖 Order history":
            await message.answer(text=_("Sizning buyurtmalaringiz yo'q"))
            return

        case "⚙️Sozlash ℹ️ Ma'lumotlar" | "⚙️ Settings ℹ️ Information":
            await state.set_state(MenuState.settings)
            await message.answer(text=_("Harakatni tanlang:"), reply_markup=settings_keyboard())

        case "🔥 Aksiya" | "🔥 Promotions":
            await state.set_state(MenuState.sales)
            await message.answer(text=_("Shahringizda hali aksiyalar mavjud emas"))

        case "🙋🏻‍♂️ Jamoamizga qo'shiling" | "🙋‍♂️ Join our team":
            await state.set_state(MenuState.join_us)
            await message.answer(
                text=_("Ahil jamoamizda ishlashga taklif qilamiz! Telegramdan chiqmay, "
                       "shu yerning o'zida anketani to'ldirish uchun quyidagi tugmani bosing."),
                reply_markup=join_us_inline_keyboard)

        case "🙋☎️ Les Ailes bilan aloqa" | "📞 Contact Les Ailes":
            await state.set_state(MenuState.contact_us)
            await message.answer(
                text=_("Agar siz bizga yozsangiz yoki sharh qoldirmoqchi bo'lsangiz, xursand bo'lamiz."),
                reply_markup=contact_us_keyboard)

        case _:
            await state.set_state(MenuState.menu)


@router.message(MenuState.to_order)
async def to_order(message: Message, state: FSMContext):
    if message.text == "⬅️ Ortga":
        await state.set_state(MenuState.menu)
        await message.answer(text=_("Bosh menyu"), reply_markup=menu_keyboard())
        return

    if message.text == "🏃 Olib ketish" or message.text == "🏃 Pickup":
        await state.set_state(OrderState.delivery_type)
        await message.answer(text=_("Qayerdasiz 👀? Agar lokatsiyangizni📍 yuborsangiz, "
                                    "sizga eng yaqin filialni aniqlaymiz"),
                             reply_markup=location_keyboard()
                             )


@router.message(OrderState.delivery_type)
async def delivery_type(message: Message, state: FSMContext):
    if message.text == "⬅️ Ortga":
        await state.set_state(MenuState.to_order)
        await message.answer(text=_("Buyurtmani o'zingiz 🙋‍♂️ olib keting yoki Yetkazib berishni 🚙 tanlang"),
                             reply_markup=delivery_keyboard())
        return

    if "Filialni tanlang" in message.text or "Select a branch" in message.text:
        language_code = get_user_language(message.from_user.id)
        branches = await get_all_branches()
        await state.set_state(OrderState.branches)
        await message.answer(text=_("Qaysi filialdan olib ketishni tanlang"),
                             reply_markup=db_keyboard(branches, language_code))


@router.message(OrderState.branches)
async def branches(message: Message, state: FSMContext):
    if message.text == "⬅️ Ortga":
        await state.set_state(OrderState.delivery_type)
        await message.answer(text=_("Qayerdasiz 👀? Agar lokatsiyangizni📍 yuborsangiz, "
                                    "sizga eng yaqin filialni aniqlaymiz"),
                             reply_markup=location_keyboard()
                             )
        return

    await state.set_state(OrderState.categories)
    branch = await get_branch_by_title(message.text)
    if not branch:
        await message.answer(_("Filial topilmadi. Iltimos, qaytadan tanlang."))
        return

    language_code = get_user_language(message.from_user.id)
    categories = await get_all_categories()
    location = _("Manzil")
    target = _("Mo'ljal")
    working_hours = _("Ish vaqti")
    await message.answer(text=f"{branch.title}\n"
                              f"{location}: {branch.location} \n"
                              f"{target}: {branch.target} \n"
                              f"{working_hours}: {branch.working_hours}\n",
                         )
    await message.answer(text=_("Nimadan boshlaymiz?"), reply_markup=db_keyboard(categories, language_code))


@router.message(OrderState.categories)
async def categories(message: Message, state: FSMContext):
    language_code = get_user_language(message.from_user.id)
    if message.text == "⬅️ Ortga":
        await state.set_state(OrderState.branches)
        await message.answer(text=_("Qaysi filialdan olib ketishni tanlang"),
                             reply_markup=db_keyboard(branches, language_code))
        return

    await state.set_state(OrderState.products)
    products = await get_products_by_category(message.text)
    if not products:
        await message.answer(_("Bu kategoriyada mahsulotlar topilmadi"))
        return
    await message.answer(text=_("Nimadan boshlaymiz?"),
                         reply_markup=db_keyboard(products, language_code))

@router.message(OrderState.products)
async def products(message: Message, state: FSMContext):
    language_code = get_user_language(message.from_user.id)
    if message.text == "⬅️ Ortga":
        await state.set_state(OrderState.categories)
        categories = await get_all_categories()
        await message.answer(text=_("Nimadan boshlaymiz?"),
                             reply_markup=db_keyboard(categories, language_code))
        return

    product = await sync_to_async(Product.objects.filter(title=message.text).first)()
    if not product:
        await message.answer(_("Mahsulot topilmadi"))
        return

    price = _("💰 Narxi")
    try:
        if product.image:
            photo = FSInputFile(product.image.path)
            await message.answer_photo(
                photo=photo,
                caption=f"📦 {product.title}\n\n"
                        f"{product.description}\n\n"
                        f"{price}: {product.price:,} so'm"
            )
        else:
            await message.answer(
                text=f"📦 {product.title}\n\n"
                     f"{product.description}\n\n"
                     f"{price}: {product.price:,} so'm"
            )
    except Exception as e:
        await message.answer(
            text=f"📦 {product.title}\n\n"
                 f"{product.description}\n\n"
                 f"{price}: {product.price:,} so'm"
        )
