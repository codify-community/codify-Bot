from discord.ext import commands
from discord import app_commands, Member, Interaction, Client
from discord.ext.commands import Context

from use_cases.moderation.mute import MuteUseCase, UnmuteUseCase


class MuteCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="mutar", aliases=["mute"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx: Context, membro: Member) -> None:
        mute_use_case = MuteUseCase(send=ctx.send, author=ctx.author)
        await mute_use_case.execute(membro, ctx.guild.me, ctx.guild)

    @app_commands.command(
        name="mutar",
        description="Muta um membro.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def mute_slash(self, interaction: Interaction, membro: Member) -> None:
        mute_use_case = MuteUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await mute_use_case.execute(membro, interaction.guild.me, interaction.guild)

    @commands.command(name="desmutar", aliases=["unmute"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx: Context, membro: Member) -> None:
        unmute_use_case = UnmuteUseCase(send=ctx.send, author=ctx.author)
        await unmute_use_case.execute(membro, ctx.guild.me, ctx.guild)

    @app_commands.command(
        name="desmutar",
        description="Retira o mute de um membro.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def unmute_slash(self, interaction: Interaction, membro: Member) -> None:
        unmute_use_case = UnmuteUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await unmute_use_case.execute(membro, interaction.guild.me, interaction.guild)


async def setup(client):
    await client.add_cog(MuteCog(client))
