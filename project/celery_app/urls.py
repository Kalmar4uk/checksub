import os
from dotenv import load_dotenv

load_dotenv()

headers_vk = {"Authorization": f"Bearer {os.getenv('VK_TOKEN')}"}
url_vk = (
    "https://api.vk.com/method/wall.get?"
    "domain={}&count=1&extended=1&fields=followers_count,domain&v=5.199"
)
