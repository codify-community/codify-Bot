from discord.ext import commands
from discord.ext.commands import Context


class MessageCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx: Context):
        if ctx.content.startswith(self.client.user.mention):
            await ctx.channel.send(f"{ctx.author.mention} | Meu prefixo é `..`!")


async def setup(client):
    await client.add_cog(MessageCog(client))
