import schedule
import time
import threading
import json

from classes.tg_bot import TG_bot
from classes.balance import Balance
from classes.mediator import Mediator

with open('conf.json', 'r') as file:
    config = json.load(file)
check_interval_hours = config['check_interval_hours']

balance = Balance()
mediator = Mediator(None, balance)
tg_bot = TG_bot(mediator)

mediator.bot = tg_bot


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every(check_interval_hours).hours.do(
    lambda: mediator.check_balance_validity())

schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.daemon = True
schedule_thread.start()

tg_bot.run_bot()
