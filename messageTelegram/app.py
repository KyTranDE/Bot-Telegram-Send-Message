import asyncio
from telegram import Bot
from time import sleep
from message_template import message_template
import json


async def main():
    # Thay 'YOUR_BOT_TOKEN' bằng token API của bạn
    bot = Bot(token='7305659457:AAH7iMjozC4D5msQJGKLq3N9FU-Fc8njvds')

    # ID của nhóm chat. Bạn có thể lấy ID này bằng cách sử dụng @username_to_id_bot
    chat_id = '-4231092140'

    # Tin nhắn mà bạn muốn gửi
    data = {
        "name": "bug",
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
            photo="https://xe.chotot.com/_next/image?url=https%3A%2F%2Fcdn.chotot.com%2FGD1xKePUmFLYC17DrLOpCBUB52ph2S87V6VCr3cuMPo%2Fpreset%3Aview%2Fplain%2F1a51308bb7886b82f7bc8bcc200d442c-2866366100190608516.jpg&w=640&q=100 640w, /_next/image?url=https%3A%2F%2Fcdn.chotot.com%2FGD1xKePUmFLYC17DrLOpCBUB52ph2S87V6VCr3cuMPo%2Fpreset%3Aview%2Fplain%2F1a51308bb7886b82f7bc8bcc200d442c-2866366100190608516.jpg&w=750&q=100 750w, /_next/image?url=https%3A%2F%2Fcdn.chotot.com%2FGD1xKePUmFLYC17DrLOpCBUB52ph2S87V6VCr3cuMPo%2Fpreset%3Aview%2Fplain%2F1a51308bb7886b82f7bc8bcc200d442c-2866366100190608516.jpg&w=828&q=100 828w, /_next/image?url=https%3A%2F%2Fcdn.chotot.com%2FGD1xKePUmFLYC17DrLOpCBUB52ph2S87V6VCr3cuMPo%2Fpreset%3Aview%2Fplain%2F1a51308bb7886b82f7bc8bcc200d442c-2866366100190608516.jpg&w=1080&q=100 1080w, /_next/image?url=https%3A%2F%2Fcdn.chotot.com%2FGD1xKePUmFLYC17DrLOpCBUB52ph2S87V6VCr3cuMPo%2Fpreset%3Aview%2Fplain%2F1a51308bb7886b82f7bc8bcc200d442c-2866366100190608516.jpg&w=1200&q=100 1200w, /_next/image?url=https%3A%2F%2Fcdn.chotot.com%2FGD1xKePUmFLYC17DrLOpCBUB52ph2S87V6VCr3cuMPo%2Fpreset%3Aview%2Fplain%2F1a51308bb7886b82f7bc8bcc200d442c-2866366100190608516.jpg&w=1920&q=100 1920w, /_next/image?url=https%3A%2F%2Fcdn.chotot.com%2FGD1xKePUmFLYC17DrLOpCBUB52ph2S87V6VCr3cuMPo%2Fpreset%3Aview%2Fplain%2F1a51308bb7886b82f7bc8bcc200d442c-2866366100190608516.jpg&w=2048&q=100 2048w, /_next/image?url=https%3A%2F%2Fcdn.chotot.com%2FGD1xKePUmFLYC17DrLOpCBUB52ph2S87V6VCr3cuMPo%2Fpreset%3Aview%2Fplain%2F1a51308bb7886b82f7bc8bcc200d442c-2866366100190608516.jpg&w=3840&q=100 3840w",
            caption=message,
            parse_mode='HTML'  # Chỉ định định dạng HTML
        )
        sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
