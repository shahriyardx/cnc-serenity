from operator import add
import nextcord
from nextcord.ext import commands


class CrrEvents(commands.Cog):
    """Handles all the events"""

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        data = await self.bot.datatabase.fetch_one("SELECT * FROM reactions WHERE emoji_id=:emoji_id AND message_id=:message_id",
        {
            'emoji_id': payload.emoji.id,
            'message_id': payload.message_id
        }
        )

        if data:
            add_roles = [payload.member.guild.get_role(role) for role in data['add_roles']]
            remove_roles = [payload.member.guild.get_role(role) for role in data['remove_roles']]
            
            for role in add_roles:
                try:
                    await payload.member.add_roles(role)
                except:
                    pass
            
            for role in remove_roles:
                try:
                    await payload.member.remove_roles(role)
                except:
                    pass


def setup(bot):
    bot.add_cog(CrrEvents(bot))
