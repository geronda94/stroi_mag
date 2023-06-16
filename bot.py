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
            full_price = i.get('full_price')
            product_price = i.get('product_price')
            delivery_price = i.get('delivery_price')
            loaders_price = i.get('loaders_price')
            
            #Формируем сообщение о наличии заявки
            order_info = f"<b>Новый заказ с сайта</b>\n\n\t Заказ <b>№ {order_id}</b>, \n\tот {order_date} в {order_time} \n\tна сумму: <b>{full_price} р.</b>"
            
            #Извлекаем список товаров из заявки
            products = orders.get_products(order_id)
            order_products = f"<b>Товары по заказу № {order_id}</b>\n\n"
            for prod in products:
                order_products += f"<b>{prod.get('product_name')}</b> | {prod.get('coll')} шт. | {prod.get('price')} р. за шт. | Сумма: <b>{prod.get('total_price')} р. </b>\n\n"
                #Формируем сообщение со списком заявок
            order_products += f"\t\t<b>Итого за товар: {product_price} р.</b>"

            #Формируем сообщение доставки если есть доставка
            delivery_message = 'Доставка не нужна'
            if delivery_price > 0 or not None:
                delivery_items = orders.get_delivery(order_id=order_id)[0]
                if delivery_items and len(delivery_items) > 0:
                    d_name = delivery_items.get('delivery_name')
                    p_weight = delivery_items.get('products_weight')
                    max_weight = delivery_items.get('max_weight')
                    need_ride = delivery_items.get('need_ride')
                    d_price = delivery_items.get('delivery_price')
                    total_price = delivery_items.get('total_price')

                    delivery_message =  f"Заказана доставка: <b>{d_name}</b>\n" \
                                        f"По адресу: <b>{location}, {address}</b>\n"\
                                        f"Товар весит: <b>{int(p_weight) / 1000} т.</b>\n"\
                                        f"Грузоподъемность машины: <b>{int(max_weight) / 1000} т.</b>\n"\
                                        f"Нужно рейсов: <b>{need_ride}</b>\n"\
                                        f"Цена рейса: <b>{d_price} р.</b>\n"\
                                        f"\t\t<b>Итого за доставку: {total_price} р.</b>\n"\
            
            loaders_message = 'Грузчики не нужны'
            if loaders_price > 0:
                True


            # orders.in_process(order_id=order_id)
            await bot.send_message(ADMIN, text=str(order_info))
            await bot.send_message(ADMIN, text=str(order_products))
            await bot.send_message(ADMIN, text=str(delivery_message))
    else:
        await bot.send_message(ADMIN, text='Нет новых заявок\n 123\n123\n 077553291')






#Тело бота#####################################
async def start():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(job_function, 'interval', seconds=1, args=(bot,))



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