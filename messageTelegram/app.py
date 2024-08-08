import asyncio
from telegram import Bot
from time import sleep
from messageTelegram.message_template import message_template
import json


async def main():
    # Thay 'YOUR_BOT_TOKEN' bằng token API của bạn
    bot = Bot(token='7305659457:AAH7iMjozC4D5msQJGKLq3N9FU-Fc8njvds')

    # ID của nhóm chat. Bạn có thể lấy ID này bằng cách sử dụng @username_to_id_bot
    chat_id = '-4231092140'

    # Tin nhắn mà bạn muốn gửi
    data = {
        "name": "Hyundai Starex Van 2.5 MT - 2005",
        "year": "2005",
        "price": " 97 Triệu ",
        "description": " *Xe nhập khẩu, màu đen, máy dầu 2.5 L, số tay, 6 chỗ ... Hyundai Starex 2005 máy dầu 6 chỗ 800kg xe đẹp máy êm ko khói đhoa cực mát xe cc miễn TG ",
        "urlcar": "https://bonbanh.com/xe-hyundai-starex-van-2.5-mt-2005-5571723",
        "location": "Phường Hố Nai, Thành phố Biên Hòa, Đồng Nai"
    }
    message = message_template.format(
        name=data['name'], price=data['price'], location=data['location'], url=data['urlcar'])

    # Gửi tin nhắn
    while True:
        await bot.send_photo(
            chat_id=chat_id,
            photo='https://xe.chotot.com/_next/image?url=https%3A%2F%2Fcdn.chotot.com%2FBk651EBm0z_p6hpWHpzTPLNdibga27rNYuGPoZouqCE%2Fpreset%3Aview%2Fplain%2Fe6e310f693feb76e2f701f1a34a01d4f-2885960859456250650.jpg&w=1920&q=100',
            caption=message,
            parse_mode='HTML'  # Chỉ định định dạng HTML
        )
        sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
