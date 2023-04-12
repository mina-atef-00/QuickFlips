from mongoengine import connect
import ssl
from mongoengine.connection import ConnectionFailure
from mongoengine.document import Document
from mongoengine.fields import DateField, IntField, StringField
from datetime import datetime
from mongoengine.errors import NotUniqueError
from pymongo.errors import ConfigurationError, AutoReconnect
import logging

from SETUP import quick_flips_bot


async def mongo_connect():
    try:
        connect(
            ssl=True,
            ssl_cert_reqs=ssl.CERT_NONE,
            host="mongodb+srv://{mongo_username}:{mongo_password}@{mongo_hostname}.mongodb.net/{mongo_clustername}?retryWrites=true&w=majority".format(
                mongo_username=quick_flips_bot.mongo_username,
                mongo_password=quick_flips_bot.mongo_password,
                mongo_hostname=quick_flips_bot.mongo_hostname,
                mongo_clustername=quick_flips_bot.mongo_clustername,
            ),
            alias="default",
        )
        print("        + mongo db loaded")
        # print(get_time_left(user_id=12345678910111))  #!DEBUG

    except ConfigurationError or AutoReconnect or ConnectionFailure:
        raise  #!UNCOMMENT FOR DEBUG
        logging.error("DNS Timeout")


class subscribers(Document):
    user_id = IntField(unique=True)
    subscription_id = StringField()
    create_time = DateField()
    next_billing_time = DateField()


def create_subscription(
    user_id: int,
    subscription_id: str,
    create_time: datetime,
    next_billing_time: datetime,
) -> bool:
    try:
        subscription = subscribers(
            user_id=user_id,
            subscription_id=subscription_id,
            create_time=datetime.strptime(create_time, r"%Y-%m-%dT%H:%M:%SZ"),
            next_billing_time=datetime.strptime(
                next_billing_time, r"%Y-%m-%dT%H:%M:%SZ"
            ),
        ).save()
        return bool(subscription)

    except NotUniqueError:
        return "not_unique"
    except:
        # raise  #!UNCOMMENT TO DEBUG
        return None


def del_subscription(user_id: int):
    if not subscribers.objects(user_id=user_id):
        return False
    else:
        for subscriber in subscribers.objects(user_id=user_id):
            subscribers.delete(subscriber)
            return True


def get_time_left(user_id: int) -> str:
    return "".join(
        [
            str(subscriber.next_billing_time - subscriber.create_time)
            for subscriber in subscribers.objects(user_id=user_id)
        ]
    )


def get_subs() -> list:
    return [subscriber.user_id for subscriber in subscribers.objects]
