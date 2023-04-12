from typing import Union
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiohttp import request
from asyncio import run
from discord import Member, Role
from discord.utils import get
from src.db.mongo import create_subscription, del_subscription
from src.db.mongo import subscribers

# from src.cogs.customers import Customers
from quick_flips_main import Bot
from SETUP import quick_flips_bot


async def check_subscription_payment(
    user_id: int, subscription_id: str, live: bool = False
) -> Union[bool, str]:
    endpoint = (
        r"https://api-m.sandbox.paypal.com//v1/billing/subscriptions"
        if not live
        else r"https://api-m.paypal.com//v1/billing/subscriptions"
    )
    try:
        async with request(
            method="GET",
            url=f"{endpoint}/{subscription_id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {quick_flips_bot.paypal_token}",
            },
        ) as response_json:
            # return response_json  #!DEBUG
            if not response_json:
                return False

            try:
                if response_json["status"] == "ACTIVE":
                    create_subscription(
                        user_id=user_id,
                        subscription_id=response_json["id"],
                        create_time=response_json["create_time"],
                        next_billing_time=response_json["billing_info"][
                            "next_billing_time"
                        ],
                    )
                    return True
                else:
                    return "not_active"

            except:
                return False
    except:
        return False


async def remove_inactive_subs():
    for subscriber in subscribers.objects:
        if (
            check_subscription_payment(
                user_id=subscriber.user_id,
                subscription_id=subscriber.subscription_id,
            )
            == "not_active"
        ):
            try:
                ex_customer: Member = get(
                    (Bot.get_guild(quick_flips_bot.server_id)).members,
                    id=subscriber.user_id,
                )
                customer_role: Role == get(
                    (Bot.get_guild(quick_flips_bot.server_id)).roles,
                    name=quick_flips_bot.customer_role_name,
                )
                await ex_customer.remove_roles(customer_role)
            except:
                continue
            del_subscription(user_id=subscriber.user_id)


async def cron_check_subs(sched: AsyncIOScheduler):
    sched.add_job(remove_inactive_subs, CronTrigger(day=1))


#!FOR DEBUG
# print(run(check_subscription_payment("")))
