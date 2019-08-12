import settings
from clockify import get_users, get_running_clock_user
from shabby_telegram import shabby_telegram_send

users = get_users()
for user_name, user_id in users.items():
    if user_name in settings.telegram_users:
        msg = get_running_clock_user(user_id)
        if msg:
            shabby_telegram_send(msg, settings.telegram_users[user_name])
