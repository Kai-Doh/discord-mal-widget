from dotenv import load_dotenv
import requests
from os import getenv
from bs4 import BeautifulSoup

load_dotenv()

REQUEST_HEADERS = {
    'Content-Type': "application/json",
    'Authorization': "Bot {}".format(getenv("BOT_TOKEN")),
    'User-Agent': "DiscordBot (https://github.com/discord/discord-api-docs, 1.0.0)"
}

MAL_HEADERS = {
    'User-Agent': "Mozilla/5.0 (compatible; discord-mal-widget/1.0)"
}

username = getenv("MAL_USERNAME")


def parse_int(text):
    return int(text.replace(",", "").strip())


def get_status_count(container, status_class):
    link = container.select_one("a.{}".format(status_class))
    if not link:
        return 0
    span = link.find_next_sibling("span")
    return parse_int(span.get_text(strip=True))


profile_response = requests.get(
    "https://myanimelist.net/profile/{}".format(username), headers=MAL_HEADERS
)
profile_response.raise_for_status()
soup = BeautifulSoup(profile_response.text, "html.parser")

avatar_img = soup.select_one("div.user-image img")
avatarurl = avatar_img["data-src"]

joined = None
for li in soup.select("ul.user-status.border-top.pb8.mb4 li"):
    title = li.select_one(".user-status-title")
    if title and title.get_text(strip=True) == "Joined":
        joined = li.select_one(".user-status-data").get_text(strip=True)
        break

anime_stats = soup.select_one("div.stats.anime")

days_div = anime_stats.select_one(".stat-score > div")
dayswatched = days_div.contents[-1].strip()

watching_anime_list = get_status_count(anime_stats, "watching")
completed_anime_list = get_status_count(anime_stats, "completed")
onhold_anime_list = get_status_count(anime_stats, "on_hold")
dropped_anime_list = get_status_count(anime_stats, "dropped")
plantowatch_anime_list = get_status_count(anime_stats, "plan_to_watch")

totalanime_anime_list = None
for li in anime_stats.select("ul.stats-data li"):
    spans = li.find_all("span")
    if spans and spans[0].get_text(strip=True) == "Total Entries":
        totalanime_anime_list = parse_int(spans[1].get_text(strip=True))
        break

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
