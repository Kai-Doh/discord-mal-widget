from dotenv import load_dotenv
import requests
from os import getenv
import datetime

load_dotenv()

REQUEST_HEADERS = {
    'Content-Type': "application/json",
    'Authorization': "Bot {}".format(getenv("BOT_TOKEN")),
    'User-Agent': "DiscordBot (https://github.com/discord/discord-api-docs, 1.0.0)"
}

username = getenv("MAL_USERNAME")

jikan_response = requests.get("https://api.jikan.moe/v4/users/{}/full".format(username))
jikan_response.raise_for_status()
user = jikan_response.json()

avatarurl = user['data']['images']['jpg']['image_url']
anime_list = user['data']['statistics']['anime']
joined = datetime.datetime.strptime(user['data']['joined'], "%Y-%m-%dT%H:%M:%S%z").strftime("%b %d, %Y")
dayswatched = anime_list['days_watched']
watching_anime_list = anime_list['watching']
plantowatch_anime_list = anime_list['plan_to_watch']
completed_anime_list = anime_list['completed']
dropped_anime_list = anime_list['dropped']
onhold_anime_list = anime_list['on_hold']
totalanime_anime_list = anime_list['total_entries']

REQUEST_DATA = {
    "data":
    {
        "dynamic":
        [
            {
                "type": 3,
                "name": "avatar",
                "value":
                {
                    "url": avatarurl
                }
            },
            {
                "type": 1,
                "name": "joindate",
                "value": "Joined: {}".format(joined)
            },
            {
                "type":2,
                "name":"watching",
                "value":watching_anime_list
            },
            {
                "type":2,
                "name":"completed",
                "value":completed_anime_list
            },
            {
                "type":2,
                "name":"plantowatch",
                "value":plantowatch_anime_list
            },
            {
                "type":2,
                "name":"dropped",
                "value":dropped_anime_list
            },
            {
                "type": 1,
                "name": "dayswatched",
                "value": "Days Watched: {}".format(dayswatched)
            },
            {
                "type":2,
                "name":"onhold",
                "value":onhold_anime_list
            },
            {
                "type":2,
                "name":"totalanime",
                "value":totalanime_anime_list
            }
        ]
    },
    "username": username
}

try:
    response = requests.patch(url = "https://discord.com/api/v9/applications/{}/users/{}/identities/0/profile".format(getenv("APP_ID"), getenv("USER_ID")),
                              json = REQUEST_DATA,
                              headers = REQUEST_HEADERS)
    response.raise_for_status()
    print("Update successful!")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
