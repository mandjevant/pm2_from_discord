from scripts import *
from checks import *
import sentry_sdk
import re


class BotSquadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = bot.conf
        self.shell = bot.shell

    @commands.command()
    @is_bot_squad()
    async def ssh(self, ctx, user: str):
        self.shell = create_conn(hostname=self.conf.get(user + "_creds", 'cred_hostname'),
                                 username=self.conf.get(user + "_creds", 'cred_username'),
                                 private_key_file=self.conf.get(user + "_creds", 'cred_pkk_file'))

        await ctx.send("Shell connected")

    @ssh.error
    async def ssh_error(self, ctx, err):
        if isinstance(err, commands.CheckFailure):
            await ctx.send("Sorry, you do not have permission to use this command.")
        elif isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"User is a required argument that is missing.\nExisting users are:\n{av_users}")
        elif isinstance(err, commands.BadArgument):
            await ctx.send(f"Login for user not found. Please input an existing user.\nExisting users are:\n{av_users}")
        else:
            await ctx.send(f"Unknown error occurred.\n{str(err)}")
            sentry_sdk.capture_message(str(err))

    @commands.command()
    @is_bot_squad()
    async def run(self, ctx, *, arg: str):
        word_list = re.sub("[^\\w]", " ", arg).split()

        result = self.shell.run(word_list)

        if arg[:8] == "pm2 list":
            result = result.output.decode('utf8')
            result = BotSquadCog.replace(result)

            description = result.split("\n")

        else:
            if isinstance(result.output, bytes):
                res = result.output.decode('utf8')
            else:
                res = result.output

            description = res.split("\n")

        text = ""

        for value in description:
            text += value + "\n"

            if len(text) > 1800:
                try:
                    await ctx.send(f"```Java\n{text}\n````")
                    text = ""
                except Exception as e:
                    sentry_sdk.capture_exception(e)

        try:
            await ctx.send(f"```Java\n{text}\n```")
        except Exception as e:
            sentry_sdk.capture_exception(e)

    @run.error
    async def run_error(self, ctx, err):
        if isinstance(err, commands.CheckFailure):
            await ctx.send("Sorry, you do not have permission to use this command.")
        elif isinstance(err, commands.BadArgument):
            await ctx.send("It is required to input a command you want to execute.")
        else:
            await ctx.send(f"Unknown error occurred.\n{str(err)}")
            sentry_sdk.capture_message(str(err))

    @staticmethod
    def replace(text):
        bad_chars = {'┼': '', '┌': '', '┬': '', '└': '', '┘': '', '─': '',
                     '┐': '', '┤': '', '┴': '', '├': '', ']': '', '[': ''}

        for original, replacement in bad_chars.items():
            text = text.replace(original, replacement)

        return text


def setup(bot):
    bot.add_cog(BotSquadCog(bot))
