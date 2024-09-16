import json
import httpx
from typing import Dict
from urllib.parse import quote
import array

INSTAGRAM_APP_ID = "936619743392459"  # this is the public app id for instagram.com

# scrape metadata around a user account
client = httpx.Client(
    headers={
        # this is internal ID of an instagram backend app. It doesn't change often.
        "x-ig-app-id": "936619743392459",
        # use browser-like features
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)

# single user support
def scrape_user(username: str):
    """Scrape Instagram user's data"""
    result = client.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
    )
    data = json.loads(result.content)
    return data["data"]["user"]

# multi user support
def scrape_users(usernames):
    userdata = []
    print(usernames)
    for username in usernames:
        result = client.get(
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
        )
        data = json.loads(result.content)
        userdata.append(data["data"]["user"])
    return userdata

# print(scrape_user("travisscott"))

'''
userinfo = scrape_user("yeat")

with open("yeat.json", "w",encoding="utf-8") as f:
    json.dump(userinfo, f, indent=2, ensure_ascii=False)'''

count = 2
for user in scrape_users(["yeat", "kencarson"]):
    filename = f"user{count}.json"
    with open(filename, "w",encoding="utf-8") as f:
        json.dump(user, f, indent=2, ensure_ascii=False)
    count += 1