from checks import *
import sentry_sdk
import typing
import sys
import os


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = bot.conf

    @commands.command()
    @is_admin()
    async def reloadcogs(self, ctx):
        self.bot.reload_extension('cogs.admin')
        self.bot.reload_extension('cogs.squad')

        await ctx.send(f"{ctx.author.mention}, all cogs have been reloaded.")

    @reloadcogs.error
    async def reloadcogs_error(self, ctx, err):
        if isinstance(err, commands.CheckFailure):
            await ctx.send("Sorry, you do not have permission to use this command.")
        else:
            await ctx.send(f"Unknown error occurred.\n{str(err)}")
            sentry_sdk.capture_message(str(err))

    @commands.command()
    @is_admin()
    async def loadcog(self, ctx, cog):
        self.bot.load_extension(cog)
        await ctx.send(f"{ctx.author.mention}, `{cog}` has been loaded.")

    @loadcog.error
    async def loadcog_error(self, ctx, err):
        if isinstance(err, commands.CheckFailure):
            await ctx.send("Sorry, you do not have permission to use this command.")
        else:
            await ctx.send(f"Unknown error occurred.\n{str(err)}")
            sentry_sdk.capture_message(str(err))

    @commands.command()
    @is_admin()
    async def unloadcog(self, ctx, cog):
        self.bot.unload_extension(cog)
        await ctx.send(f"{ctx.author.mention}, `{cog}` has been unloaded.")

    @unloadcog.error
    async def unloadcog_error(self, ctx, err):
        if isinstance(err, commands.CheckFailure):
            await ctx.send("Sorry, you do not have permission to use this command.")
        else:
            await ctx.send(f"Unknown error occurred.\n{str(err)}")
            sentry_sdk.capture_message(str(err))

    @commands.command()
    @is_admin()
    async def purge(self, ctx, n: typing.Optional[int] = 100):
        deleted = await ctx.channel.purge(limit=n)
        await ctx.send(f"Deleted {len(deleted)} message(s).")

    @purge.error
    async def purge_error(self, ctx, err):
        if isinstance(err, commands.CheckFailure):
            await ctx.send("Sorry, you do not have permission to use this command.")
        elif isinstance(err, commands.BadArgument):
            await ctx.send("Please input an integer.")
        else:
            await ctx.send(f"Unknown error occurred.\n{str(err)}")
            sentry_sdk.capture_message(str(err))

    @commands.command()
    @is_bot_squad()
    async def restart(self, ctx):
        os.execl(sys.executable, sys.executable, *sys.argv)

    @restart.error
    async def restart_error(self, ctx, err):
        if isinstance(err, commands.CheckFailure):
            await ctx.send("Sorry, you do not have permission to use this command.")
        else:
            await ctx.send(f"Unknown error occurred.\n{str(err)}")
            sentry_sdk.capture_message(str(err))


def setup(bot):
    bot.add_cog(AdminCog(bot))
