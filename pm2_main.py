from configparser import ConfigParser
import discord
from discord.ext import commands
from scripts import *
import sentry_sdk
import asyncio
import sys
import os
import re


event_loop = asyncio.get_event_loop()


class Bot(commands.Bot):
    def __init__(self, conf):
        super().__init__(command_prefix='$', description='dankmemes pm2 from discord', loop=event_loop)
        self.conf = conf
        self.shell = None

        self.load_extension('cogs.admin')
        self.load_extension('cogs.squad')

    @staticmethod
    async def on_ready():
        sentry_sdk.capture_message("Logged in!")

    async def on_message(self, message):
        if message.author.id not in [204184798200201216, 706810315647483985]:
            for user_id, regex in on_message_users.items():
                if re.match(regex, str(message.content).lower()):
                    await self.send_notification(message, user_id)

        await Bot.process_commands(self, message=message)

    async def send_notification(self, message, user_discord_id):
        message_url = f'https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}'
        embed = discord.Embed(title=f'{message.author} said')

        embed.add_field(name='Server:', value=message.guild.name, inline=True)
        embed.add_field(name='Channel:', value=message.channel.mention, inline=True)
        embed.add_field(name='Author:', value=message.author, inline=True)
        embed.add_field(name='Time (UTC):', value=message.created_at.strftime('%B %d, %Y at %I:%M:%S %p %Z'), inline=True)
        embed.add_field(name='Message Link:', value=message_url)
        embed.add_field(name='Message:', value=message.clean_content, inline=False)

        await Bot.get_user(self, id=user_discord_id).send(embed=embed)

    def run(self):
        super().run(self.conf.get('global', 'discord_id'))


class Config:
    conf = None

    @staticmethod
    def initiate_config():
        try:
            Config.conf = ConfigParser()
            os.chdir(sys.path[0])
            if os.path.exists('conf.ini'):
                Config.conf.read('conf.ini')
            else:
                sentry_sdk.capture_message('Config file, conf.ini, was not found.')
                return False

            return True

        except Exception as e:
            sentry_sdk.capture_message("Could not initiate conf.")
            sentry_sdk.capture_exception(e)
            return False


def main():
    if Config.initiate_config():
        sentry_sdk.init(Config.conf.get('global', 'sentry_init'))
        bot = Bot(Config.conf)
        bot.run()
    else:
        sys.exit()


if __name__ == '__main__':
    main()
