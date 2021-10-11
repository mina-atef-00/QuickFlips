from mongoengine import connect
from os import environ
import ssl
from mongoengine.connection import ConnectionFailure
from mongoengine.document import Document
from mongoengine.fields import DateField, IntField, StringField
from datetime import datetime, timedelta
from mongoengine.errors import NotUniqueError
from pymongo.errors import ConfigurationError, AutoReconnect
import logging
from asyncio import run

from SETUP import quick_flips_bot

mongo_username = quick_flips_bot.mongo_username
mongo_password = quick_flips_bot.mongo_password
db_name = "Subscriptions"
cluster_name = "cluster0"


async def mongo_connect():
    try:
        connect(
            ssl=True,
            ssl_cert_reqs=ssl.CERT_NONE,
            host=f"mongodb+srv://{mongo_username}:{mongo_password}@{cluster_name}.xklrn.mongodb.net/{db_name}?retryWrites=true&w=majority",
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


############################## #! DEBUG
# run(mongo_connect())
# for (user_id, subscription_id, create_time, next_billing_time) in (
# (
#     12345678910111,
#     "I-BW452GLLEP1Ga",
#     "2019-04-09T10:26:04Z",
#     "2019-04-11T10:00:00Z",
# ),
# (
#     12345678910112,
#     "I-BW452GLLEP1Gb",
#     "2019-04-09T10:26:04Z",
#     "2019-04-12T10:00:00Z",
# ),
# (
#     12345678910113,
#     "I-BW452GLLEP1Gc",
#     "2019-04-09T10:26:04Z",
#     "2019-04-13T10:00:00Z",
# ),
# (
#     12345678910114,
#     "I-BW452GLLEP1Gd",
#     "2019-04-09T10:26:04Z",
#     "2019-04-14T10:00:00Z",
# ),


# ):
#     print(
#         create_subscription(
#             user_id=user_id,
#             subscription_id=subscription_id,
#             create_time=create_time,
#             next_billing_time=next_billing_time,
#         )
#     )

# print(del_subscription(user_id=123456789101169))
# print(del_subscription(user_id=1234567891011))
# for sub in subscribers.objects:
#     print(sub.user_id, sub.subscription_id, sub.create_time, sub.next_billing_time)
# print((subscribers.objects(user_id=1234567891011)).id)
