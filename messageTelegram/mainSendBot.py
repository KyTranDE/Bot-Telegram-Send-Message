from telegram import Bot
from time import sleep
from message_template import message_template

def send_messages(bot_token, chat_id, data_list, delay=2):
    """
    Gửi các tin nhắn từ danh sách dữ liệu đến một nhóm chat trên Telegram.

    :param bot_token: Token API của bot Telegram.
    :param chat_id: ID của nhóm chat Telegram.
    :param data_list: Danh sách các từ điển chứa thông tin tin nhắn.
    :param delay: Thời gian chờ giữa các lần gửi tin nhắn (mặc định là 10 giây).
    """
    bot = Bot(token=bot_token)

    for data in data_list:
        message = message_template.format(
            name=data['name'], price=data['price'], location=data['location'], url=data['urlcar'])

        # Gửi tin nhắn
        bot.send_photo(
            chat_id=chat_id,
            photo='https://xe.chotot.com/_next/image?url=https%3A%2F%2Fcdn.chotot.com%2F2llj1W3J9Fvk8tgsqGfp_Gdpn7OEYFr8DsxuJhJT7co%2Fpreset%3Aview%2Fplain%2F33379762601844158f31203eab7ca97d-2866366097827255497.jpg&w=1920&q=100',
            caption=message,
            parse_mode='HTML'
        )
        # Thời gian chờ giữa các tin nhắn
        sleep(delay)

def main():
    # Thay 'YOUR_BOT_TOKEN' bằng token API của bạn
    bot_token = '7305659457:AAH7iMjozC4D5msQJGKLq3N9FU-Fc8njvds'

    # ID của nhóm chat. Bạn có thể lấy ID này bằng cách sử dụng @username_to_id_bot
    chat_id = '-4231092140'

    # Giả sử bạn có một danh sách các tin nhắn cần gửi từ tệp JSON hoặc một nguồn dữ liệu nào đó
    data_list = [
        {
            "name": "bug",
            "year": "2005",
            "price": " 97 Triệu ",
            "description": " *Xe nhập khẩu, màu đen, máy dầu 2.5 L, số tay, 6 chỗ ... Hyundai Starex 2005 máy dầu 6 chỗ 800kg xe đẹp máy êm ko khói đhoa cực mát xe cc miễn TG ",
            "urlcar": "https://bonbanh.com/xe-hyundai-starex-van-2.5-mt-2005-5571723",
            "location": "Phường Hố Nai, Thành phố Biên Hòa, Đồng Nai"
        },
        # Thêm các tin nhắn khác vào đây
    ]

    # Gọi hàm để gửi tin nhắn
    send_messages(bot_token, chat_id, data_list)

if __name__ == "__main__":
    main()
