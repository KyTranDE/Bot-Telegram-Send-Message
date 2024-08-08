import asyncio
from telegram import Bot, InputMediaPhoto
from messageTelegram.message_template import message_template


async def main():
    # Thay 'YOUR_BOT_TOKEN' bằng token API của bạn
    bot = Bot(token='7305659457:AAH7iMjozC4D5msQJGKLq3N9FU-Fc8njvds')

    # ID của nhóm chat. Bạn có thể lấy ID này bằng cách sử dụng @username_to_id_bot
    chat_id = '-4231092140'

    # Danh sách URL ảnh
    photo_urls = [
        # "https://s.bonbanh.com/uploads/users/685313/car/5571723/m_1713589044.840.jpg",
        "https://s.bonbanh.com/uploads/users/685313/car/5571723/m_1713589069.609.jpg",
        "https://s.bonbanh.com/uploads/users/685313/car/5571723/l_1713589068.368.jpg",
        "https://s.bonbanh.com/uploads/users/685313/car/5571723/l_1713589068.368.jpg",
        "https://xe.chotot.com/_next/image?url=https%3A%2F%2Fcdn.chotot.com%2FBk651EBm0z_p6hpWHpzTPLNdibga27rNYuGPoZouqCE%2Fpreset%3Aview%2Fplain%2Fe6e310f693feb76e2f701f1a34a01d4f-2885960859456250650.jpg&w=1920&q=100"
    ]

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

    # Tạo danh sách các InputMediaPhoto
    media = [InputMediaPhoto(media=url) for url in photo_urls]

    # Chỉ định chú thích cho bức ảnh đầu tiên
    media[0] = InputMediaPhoto(
        media=photo_urls[0], caption=message, parse_mode='HTML')

    # Gửi nhóm ảnh
    await bot.send_media_group(chat_id=chat_id, media=media)

if __name__ == "__main__":
    asyncio.run(main())
