from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Filter, Command, Text
import asyncio
import logging #импортируем библиотеку логирования
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apg import db
from pg import orders


#Блок инициализации#############################
TOKEN = '6052258880:AAEszm7mrAL74aIL76KnpLjihXng5f_vXSc'                      
ADMIN = '5774941154'                  
################################################

#Блок стартовых функций#########################
async def start_bot(bot: Bot): #функция срабатывает когда запускается сервер с ботом
    await bot.send_message(ADMIN, text='Бот запущен!')
async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<s>Бот остановлен</s>')
async def get_start(message: Message, bot: Bot): #Функция срабатывает когда юзер дает команду /start
    await message.answer('Давай начнем!')
###############################################

async def job_function(bot: Bot):

    extract = orders.get_orders()
    #Извлекаем не обработанные заявки
    if len(extract)> 0:
        for i in extract:
            #Проходимся по списку необработанных заявок в цикле
            order_id = str(i.get('id'))
     
            #Извлекаемданные из заявки в итерации
            datetime = i.get('date_time')
            order_date = datetime.strftime('%d.%m') if datetime else None
            order_time = datetime.strftime('%H:%M') if datetime else None
            location = i.get('location')
            address = i.get('address')
            order_phone = i.get('phone')
            full_price = i.get('full_price')
            product_price = i.get('product_price')
            delivery_price = i.get('delivery_price')
            loaders_price = i.get('load_price')
            
            #Формируем сообщение о наличии заявки
            order_info = f"<b>✅ Новый заказ с сайта ✅</b>\n\n\tЗаказ <b>№ {order_id}</b>, \n\t<b>от {order_date} в {order_time}</b>"
            
            #Извлекаем список товаров из заявки
            products = orders.get_products(order_id)
            order_products = f"----------------------------\n🛒<b> Товары по заказу № {order_id}</b>\n\n  "
            for prod in products:
                order_products += f"📦 <b>{prod.get('product_name')}</b> | {prod.get('coll')} шт. | {prod.get('price')} р. за шт. | Сумма: <b>{prod.get('total_price')} р. </b>\n\n"
                #Формируем сообщение со списком заявок
            order_products += f"\t\t<b>Итого за товар: {product_price} р.</b>"

            #Формируем сообщение доставки если есть доставка
            delivery_message = '----------------------------\n🚛 Доставка не нужна'
            if float(delivery_price) > 0:
                delivery_items = orders.get_delivery(order_id=order_id)[0]
                if delivery_items and len(delivery_items) > 0:
                    d_name = delivery_items.get('delivery_name')
                    p_weight = delivery_items.get('products_weight')
                    max_weight = delivery_items.get('max_weight')
                    need_ride = delivery_items.get('need_ride')
                    d_price = delivery_items.get('delivery_price')
                    total_price = delivery_items.get('total_price')

                    delivery_message =  f"----------------------------\n🚛 Доставка к заказу <b>№{order_id}</b> \n\n <b>{d_name}</b> \n " \
                                        f"По адресу: <b>{location}, {address}</b>\n\n"\
                                        f"Товар весит: <b>{int(p_weight) / 1000} т.</b>\n"\
                                        f"Грузоподъемность машины: <b>{int(max_weight) / 1000} т.</b>\n"\
                                        f"Нужно рейсов: <b>{need_ride}</b>\n"\
                                        f"Цена рейса: <b>{d_price} р.</b>\n\n"\
                                        f"\t\t<b>Итого за доставку: {total_price} р.</b>\n"\
            
            loaders_message = '----------------------------\n👷‍♂️ Грузчики не нужны '
            if float(loaders_price) > 0:
                loaders_items = orders.get_loaders(order_id=order_id)
                l_name = loaders_items[0].get('load_name')
                
                loaders_message = f"----------------------------\n👷‍♂️ Услуги грузчиков к заказу <b>№{order_id}</b> \n\n <b>{l_name}</b> \n\n"
                for load in loaders_items:
                    l_weight = load.get('load_weight')
                    l_coll = load.get('coll')
                    l_price = load.get('price')
                    l_tprice = load.get('total_price')
                    loaders_message += f'➕ Вес: <b>{l_weight} кг.</b> | {l_coll} шт. | Цена: {l_price} | Сумма: <b>{l_tprice}</b>\n\n'
                
                loaders_message += f"\t\t<b>Итого за разгрузку: {loaders_price} р.</b>\n"\

            #orders.order_status(order_id=order_id, status='in process')
            finally_message = f"{order_info} \n\n\n{order_products} \n\n\n{delivery_message} \n\n\n{loaders_message} \n\n\n<b>ОБЩАЯ СУММА: {full_price} </b>"

            await bot.send_message(ADMIN, text=str(finally_message))
            await bot.send_message(ADMIN, text=str(f"☎️ Телефон заказчика: ☎️\n\n "))
            await bot.send_message(ADMIN, text=f'{order_phone}')







#Тело бота#####################################
async def start():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(job_function, 'interval', seconds=10, args=(bot,))



    dp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start





    try:
        #Начало сессии
        scheduler.start()
        
        await dp.start_polling(bot)
    finally:
        #Закрываем сессию
        await bot.session.close()
###############################################


#Запускаем функцию Бота########################
if __name__ == "__main__":
    asyncio.run(start())