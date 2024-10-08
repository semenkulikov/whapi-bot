import threading
import time
import schedule
import datetime
from loader import bot, app_logger
from config_data.config import ALLOWED_USERS
from database.models import clear_status


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def background_job():
    today = datetime.datetime.now().day
    if today in (1, 15):
        clear_status()
        app_logger.info("Очистка статусов пользователей завершена")
        for user_id in ALLOWED_USERS:
            bot.send_message(user_id, "Очистка статусов пользователей завершена успешно!")


def run_clear():
    schedule.every().day.at("12:00").do(background_job)

    # Start the background thread
    stop_run_continuously = run_continuously()

    # Do some other things...
    time.sleep(10)

    # Stop the background thread
    stop_run_continuously.set()
