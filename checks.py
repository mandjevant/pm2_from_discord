from discord.ext import commands


def exc(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return False

    return wrapper


@exc
def admin_check(ctx):
    admins = [204184798200201216]

    return ctx.author.id in admins


@exc
def bot_squad_check(ctx):
    bot_squad_members = [189149892533288960,  # Elfah
                         278321214697504770,  # Jackson
                         590893206984720424,  # Batman
                         174622382361673728,  # Kelly
                         393801572858986496]  # Spaz

    return ctx.author.id in bot_squad_members


def is_admin():
    def wrapper(ctx):
        return admin_check(ctx)

    return commands.check(wrapper)


def is_bot_squad():
    def wrapper(ctx):
        return bot_squad_check(ctx) or admin_check(ctx)

    return commands.check(wrapper)
