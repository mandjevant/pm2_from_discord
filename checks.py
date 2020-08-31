from configparser import ConfigParser
from discord.ext import commands
import json


def exc(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return False

    return wrapper


@exc
def admin_check(ctx):
    conf = ConfigParser()
    conf.read('conf.ini')

    return ctx.author.id in json.loads(conf.get('global', 'admins'))


@exc
def bot_squad_check(ctx):
    conf = ConfigParser()
    conf.read('conf.ini')

    return ctx.author.id in json.loads(conf.get('global', 'bot_squad_members'))


def is_admin():
    def wrapper(ctx):
        return admin_check(ctx)

    return commands.check(wrapper)


def is_bot_squad():
    def wrapper(ctx):
        return bot_squad_check(ctx) or admin_check(ctx)

    return commands.check(wrapper)
