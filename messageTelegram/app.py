import asyncio
from telegram import Bot
from time import sleep
import json


async def sendBot(data):
    message_template = """
    🚗 <b>{name}</b>
    
    💰 <b>Giá:</b> {price}
    📍 <b>Địa chỉ:</b> {location}
        
    👉 <a href="{url}">Xem chi tiết</a>
    """
    bot = Bot(token='7305659457:AAH7iMjozC4D5msQJGKLq3N9FU-Fc8njvds')

    # đọc file json lấy ra danh sách GroupID
    with open('groupid.json', 'r') as f:
        data = json.load(f)
    
    # sử lí những GroupID trùng nhau
    chat_ids = []
    for i in data:
        chat_ids.append(i['group_id'])

    # Tin nhắn mà bạn muốn gửi
    message = message_template.format(
        name=data['name'], price=data['price'], location=data['location'], url=data['urlcar'])

    for chat_id in chat_ids:
        # Gửi tin nhắn
        await bot.send_photo(
            chat_id=chat_id,
            photo=data['image'],
            caption=message,
            parse_mode='HTML'
        )
        sleep(1)

#___________________________________________________________________________________________________________________________________________________________________________
# def mainSendBot(data):                                                                                                                                                    |
#     asyncio.run(sendBot(data))                                                                                                                                            |
#                                                                                                                                                                           |
# data = {                                                                                                                                                                  |
#     "name": "admin handsome",                                                                                                                                             |
#     "year": "0000",                                                                                                                                                       |
#     "price": " 911117 Triệu ",                                                                                                                                            |
#     "description": " *Xe nhập khẩu, màu đen, máy dầu 2.5 L, số tay, 6 chỗ ... Hyundai Starex 2005 máy dầu 6 chỗ 800kg xe đẹp máy êm ko khói đhoa cực mát xe cc miễn TG ", |
#     "urlcar": "https://bonbanh.com/xe-hyundai-starex-van-2.5-mt-2005-5571723",                                                                                            |
#     "location": "Phường Hố Nai, Thành phố Biên Hòa, Đồng Nai"                                                                                                             |
# }                                                                                                                                                                         |
# main(data)                                                                                                                                                                |
#___________________________________________________________________________________________________________________________________________________________________________|