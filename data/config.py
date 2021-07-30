import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
PROVIDER_TOKEN = str(os.getenv("PROVIDER_TOKEN"))

admins = [
    409524113,
    979399757
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

# база как для пользователей, так и для зпдпний
absolute_path_to_Users_database = '/home/ser4/PycharmProjects/megalike6/data/Users.db'