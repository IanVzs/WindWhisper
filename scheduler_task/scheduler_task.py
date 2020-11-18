"""
requests:
    sqlalchemy
    apscheduler
定时任务
sqlalchemy 文档:  https://apscheduler.readthedocs.io/en/stable/index.html
"""
import time
import json
try:
    from pytz import utc, timezone
    china_tz = timezone('Asia/Shanghai')

    from apscheduler.schedulers.background import BackgroundScheduler
    # from apscheduler.jobstores.mongodb import MongoDBJobStore
    from apscheduler.jobstores.memory import MemoryJobStore
    from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
    from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
    from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
except:
    print("需安装下述包")
    print("pip3 install sqlalchemy", "pip3 install apscheduler")
    raise "Stop!"

import os
import sys
upath = os.path.dirname(os.path.abspath(__file__))
path = upath.split("/")[:-1]
path = '/'.join(path)
sys.path.append(path)
from loggers import scheLog
import weather

class AllScheduler():
    def __init__(self):
        pass

    def listener(self, event):
        """任务执行状态监听"""
        if event.exception:
            log_job = {
                "code": event.code,
                "jobid": event.job_id,
                "jobstore": event.jobstore,
            }
            scheLog.error(f'The job {event.job_id} crashed :( | {log_job}')
        else:
            scheLog.info(f'The job {event.job_id} worked :)')

    def run(self):
        jobstores = {
            # 'mongo': MongoDBJobStore(),
            # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
            "memory": MemoryJobStore(),
        }
        executors = {'default': ThreadPoolExecutor(5), 'processpool': ProcessPoolExecutor(2)}
        job_defaults = {'coalesce': False, 'max_instances': 3}
        scheduler = BackgroundScheduler(
            jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=china_tz)
        scheduler.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

        #scheduler.add_job(weather.weather_alarm, 'interval', seconds=10*60, id='sign_push_report')
        scheduler.add_job(weather.weather_alarm, 'interval', seconds=2, id='sign_weather_alarm')
        scheduler.start()
        return scheduler
        # scheLog.info(f"scheduler.get_jobs: {scheduler.get_jobs()}")
        # scheduler.remove_job('sign_push_report')
        # scheduler.shutdown(wait=True)


if __name__ == "__main__":
    jobs = AllScheduler().run()
    time.sleep(3)
    jobs.remove_job('sign_weather_alarm')
    jobs.shutdown(wait=True)
    while jobs:
        try:
            time.sleep(3)
        except:
            jobs.remove_job('sign_weather_alarm')
            jobs.shutdown(wait=True)
            print("Stop.")
