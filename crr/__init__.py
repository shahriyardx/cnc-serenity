import os
from nextcord import Intents, Member
from nextcord.ext import commands
from databases import Database
from nextcord.message import Message

class Serenity(commands.AutoShardedBot):
    """Custom reaction roles bot"""

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.reaction_roles = dict()

    async def on_ready(self):
        await self._init_database()

        self.load_extension("crr.commands")
        self.load_extension("crr.events")

        print(f"{self.user} is ready")

    async def on_message(self, message: Message) -> None:
        if message.author.bot or not message.guild:
            return


        if "@everyone" in message.content or "@here" in message.content:
            muted_role = message.guild.get_role(897197795457531924)
            ignored_roles = {851508657363484713, 893009978460348439, 880273785595506709, 893552694093053993, 850470727425458186}

            if not isinstance(message.author, Member) or not muted_role:
                return

            user_roles = { role.id for role in message.author.roles }

            if not user_roles.intersection(ignored_roles):
                try:
                    await message.author.add_roles(muted_role)
                    await message.reply("This server mutes anyone who tags **everyone** and **here**. You have been muted because of this. Please message **greatscottie** to be unmuted.")
                    return
                except Exception as e:
                    print(e)

        await self.process_commands(message)

    async def _init_database(self):
        self.datatabase = Database(str(os.getenv("DSN")))
        await self.datatabase.connect()

        await self.datatabase.execute(
            """
            CREATE TABLE IF NOT EXISTS reactions(
                id BIGSERIAL NOT NULL PRIMARY KEY,
                guild_id BIGINT NOT NULL,
                message_id BIGINT NOT NULL,
                emoji_id BIGINT NOT NULL,
                add_roles BIGINT[] NOT NULL,
                remove_roles BIGINT[] NOT NULL
            )
        """
        )

default = Intents.default()
default.message_content = True

bot = Serenity(command_prefix="?", intents=default)
