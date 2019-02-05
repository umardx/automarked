from . import celery
from time import sleep


@celery.task
def reverse(msg):
    sleep(10)
    return msg[::-1]


@celery.task
def wait_sec(second):
   sleep(second)
   return True
