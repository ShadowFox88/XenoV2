class Xeno(commands.AutoShardedBot):
	def __init__(self, *args, **kwargs):
		super().__init__(get_prefix, *args, **kwargs)
		self.user_prefix = {}
		self.__load_config()
		self.emoji_list = {
			"animated_green_tick": "<a:AnimatedGreenTick:789586504950874132>",
			"animated_red_cross": "<a:AnimatedRedCross:789586505974022164>"
		}

		
		
	async def get_prefix(self, message):
		return ["x-", "==", "<@737738422067658762>"]


	async def session(self):
		return aiohttp.ClientSession(loop=self.loop)


	async def setup_hook(self):
		self.db: asyncpg.Pool[Any] | Any = await asyncpg.create_pool(
			host=self.config["db_connection"]["host"],
			user=self.config["db_connection"]["username"],
			password=self.config["db_connection"]["password"],
			database=self.config["db_connection"]["database"]
		)

		if not self.db:
			raise RuntimeError("Couldn't connect to database!")


		async def cache(self):
			a = await self.db.fetch('SELECT * FROM users')
			for i in a:
				self.cache['userinfo'][i['userid']] = dict(i)

		
		await cache(self)


		initial_extensions = [
			"cogs.help",
			"jishaku",
			"cogs.ErrorHandler",
			"cogs.music",
			"cogs.LoggingMessages",
			"cogs.developer",
			"cogs.UserControl",
			"cogs.dnd"
		]

		self.initial_extensions = initial_extensions

		for cog in initial_extensions:
			await self.load_extension(cog)
		
		context_menu_commands.init(bot)
		# sync with priority guilds right away, instead of waiting for global sync
		for guild_id in self.config["guild_ids"]:
			try:
				guild = discord.Object(id=guild_id)
				self.tree.copy_global_to(guild=guild)
				await self.tree.sync(guild=guild)
			except:
				pass


	def __load_config(self, filename: str = None):
		"""
		Load config from a .JSON file. If not specified will default to `config.json`.
		"""

		if not filename:
			filename = "config.json"

		with open(filename) as file_object:
			config = json.load(file_object)

		if isinstance(config, dict):
			self.config = config


	def add_owner(self, member):
		self.owner_ids.append(member)


	def remove_owner(self, member):
		if member == 606648465065246750:
			return False
		self.owner_ids.remove(member)


	def format_print(self, text):
		format = str(datetime.now().strftime("%x | %X") + f" | {text}")
		return format


	def get_message_emojis(self, message: discord.Message):
		regex = re.findall("<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>", message.content)
		emojis: list = []
		for animated, name, id in emojis:
			emojis += discord.PartialEmoji(animated=bool(animated), name=name, id=id)
		return emojis


	async def close(self):
		await super().close()
		await self.db.close()


	async def get_context(self, message, *, cls=CustomContext):
		# when you override this method, you pass your new Context
		# subclass to the super() method, which tells the bot to
		# use the new MyContext class
		# use the new MyContext class
		return await super().get_context(message, cls=cls)