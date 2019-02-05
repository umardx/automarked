from . import celery
from time import sleep


@celery.task
def reverse(msg):
    return msg[::-1]


@celery.task
def wait_sec(second):
   sleep(second)
   return True
