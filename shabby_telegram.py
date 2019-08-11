import requests
from urllib.parse import quote
import settings


def shabby_telegram_send(msg, chatid):
    api_telegram = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
    url = api_telegram.format(settings.TELEGRAM_TOKEN, chatid, quote(msg))
    # print(url)
    response = requests.get(url)
    if response.status_code is not 200:
        print("ERROR sending telegram")


def print_users_ids():
    url = "https://api.telegram.org/bot{}/getUpdates".format(settings.TELEGRAM_TOKEN)
    # print(url)
    response = requests.get(url)
    if response.status_code is not 200:
        return
    # print(response.text)
    response.encoding = 'utf-8'
    rj = response.json()
    if not rj['ok']:
        return
    ids = {}
    for result in rj['result']:
        id = result['message']['from']['id']
        username = result['message']['from']['username']
        first_name = result['message']['from']['first_name']
        ids[id] = (username, first_name)
    for id, names in ids.items():
        print("id: {}\tusername: @{}\tfirst_name: {}".format(id, names[0], names[1]))


if __name__ == "__main__":
    print_users_ids()
