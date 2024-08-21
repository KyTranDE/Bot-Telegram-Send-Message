import asyncio
from telegram import Bot
from time import sleep
import json
from Utils import postgres_tool
import yaml


with open('./config/config.yml', 'r') as f:
    config = yaml.safe_load(f)

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
        group_data = json.load(f)
    
    # Xử lý những GroupID trùng nhau
    chat_ids = list(set(item['group_id'] for item in group_data))

    

    # Tin nhắn mà bạn muốn gửi
    message = message_template.format(
        name=data['name'], price=data['price'], location=data['location'], url=data['urlcar'])

    for chat_id in chat_ids:
        dataimage = data["image"]
        try:
            await bot.send_photo(
                chat_id=chat_id,
                photo=dataimage,
                caption=message,
                parse_mode='HTML'
            )
            print(f"Message sent to {chat_id} successfully.")
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")
        
        # Tạm dừng 3 giây giữa các lần gửi tin nhắn
        await asyncio.sleep(3)

    # Cập nhật trạng thái sau khi gửi thành công
    try:
        database = config["database"]
        conn = postgres_tool.PostgresTool(**database)
        conn.query(f"UPDATE car SET sent = TRUE WHERE urlcar = '{data['urlcar']}';", False)
    except Exception as e:
        print(f"Failed to update database: {e}")
    finally:
        conn.close()

# get data từ database rồi send message
def main():
    # try:
    #     database = config["database"]
    #     conn = postgres_tool.PostgresTool(**database)
    #     data =  conn.query("SELECT * FROM car WHERE sent = FALSE",False)
    #     for item in data:
    #         # ('https://bonbanh.com/xe-audi-q7-3.0-at-2014-5747161', ' 739 Triệu ', ' Liên hệ: Auto Hồng Phúc C5/15B, Bình Hưng, Bình Chánh TP HCM ĐT: 0907 222 222 - 0977 775 882 ', 'Audi Q7 3.0 AT - 2014', 'https://s.bonbanh.com/uploads/users/49587/car/5747161/s_1722334908.441.jpg', False)
    #         # item dictionary
    #         datasend = {
    #             "name": item[3],
    #             "price": item[1],
    #             "location": item[2],
    #             "urlcar": item[0],
    #             "image": item[4]
    #         }
    #         asyncio.run(sendBot(datasend))
    #         conn.query(f"UPDATE car SET sent = TRUE WHERE urlcar = '{datasend['urlcar']}';",False)
    # except :
    #     pass
    datasend = {
        "name": "admin handsome",
        "price":
        " 911117 Triều ",
        "location":
        "Phường Hố Nai, Thành phố Biên Hòa, Đồng Nai",
        "urlcar":
        "https://bonbanh.com/xe-hyundai-starex-van-2.5-mt-2005-5571723",
        "image":
        "https://s.bonbanh.com/uploads/users/49587/car/5747161/s_1722334908.441.jpg"
    }
    asyncio.run(sendBot(datasend))

if __name__ == "__main__":
    while True:
        main()
        sleep(10)


#___________________________________________________________________________________________________________________________________________________________________________
#                                                                                                                                                                           |
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