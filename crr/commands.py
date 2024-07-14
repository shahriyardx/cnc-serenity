import re
import asyncio
import nextcord
from nextcord.ext import commands


class Setup(commands.Cog):
    """Setup commands"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx: commands.Context):
        """Setup reaction roles."""
        question = await ctx.send(
            "**Welcome to the setup wizard!** \n"
            "> Paste the message id which you want to use for reaction roles!"
        )

        while True:
            answer: nextcord.Message = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )
            
            try:
                message_id = int(answer.content)
            except:
                
                await question.edit(
                    content="Message id should be a integer. Please paste a valid message id"
                )
                continue

            reaction_message = None
            try:
                reaction_message = await ctx.channel.fetch_message(message_id)
            except:
                pass
            
            await asyncio.sleep(1)
            await answer.delete()
            

            if not reaction_message:
                await question.edit(
                    content="Sorry the message id you provided was not a valid message id, Try pasting again..."
                )
                continue
            else:
                break

        await question.edit(content="Type the emoji you want to add...")

        while True:
            emoji_regex = re.compile(
                r"<(?P<animated>a)?:(?P<name>[0-9a-zA-Z_]{2,32}):(?P<id>[0-9]{15,21})>"
            )

            answer: nextcord.Message = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )

            emoji = emoji_regex.match(answer.content)

            await asyncio.sleep(1)
            await answer.delete()
            if not emoji:
                await question.edit(
                    content="Unable to find an emoji in your message. Please type again"
                )
            else:
                emoji_id = int(emoji.groups()[2])
                the_emoji = nextcord.utils.get(ctx.guild.emojis, id=emoji_id)

                if the_emoji:
                    await reaction_message.add_reaction(the_emoji)
                    break
                else:
                    await question.edit(
                        content="Emoji not in this server. Please user a server emoji."
                    )
                    continue

        await question.edit(
            content=f"Mention the role you want to `add` when reacted to the emoji {the_emoji}."
        )

        while True:
            answer: nextcord.Message = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )

            role_mentions = answer.role_mentions

            await asyncio.sleep(1)
            await answer.delete()
            if not role_mentions:
                await question.edit(
                    content="Sorry no role mention was found on this message. Please try again..."
                )
                continue
            else:
                role_ids_add = [role.id for role in role_mentions]
                break

        await question.edit(
            content=f"Mention the role you want to `remove` when reacted to the emoji {the_emoji}."
        )

        while True:
            answer: nextcord.Message = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )

            role_mentions = answer.role_mentions

            await asyncio.sleep(1)
            await answer.delete()
            if not role_mentions:
                await question.edit(
                    content="Sorry no role mention was found on this message. Please try again..."
                )
                continue
            else:
                role_ids_remove = [role.id for role in role_mentions]
                break
        
        await question.edit(content="Setup completed. :tada: ")
        await self.bot.datatabase.execute(
            """
            INSERT INTO reactions
                (guild_id, message_id, emoji_id, add_roles, remove_roles)
            VALUES
                (:guild_id, :message_id, :emoji_id, :add_roles, :remove_roles)
            """,
            {
                "guild_id": ctx.guild.id,
                "message_id": message_id,
                "emoji_id": emoji_id,
                "add_roles": role_ids_add,
                "remove_roles": role_ids_remove,
            },
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

def setup(bot):
    bot.add_cog(Setup(bot))
