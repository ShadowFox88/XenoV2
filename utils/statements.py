class PreparedStatements():
    def __init__(self, db):
        self.db = db
    
    async def setup(self):
        self.error_insertion = await self.db.prepare("""INSERT INTO errors (command, user_id, guild_id, traceback) VALUES ($1, $2, $3, $4)""")
        self.get_last_error_id = await self.db.prepare("""SELECT id FROM errors ORDER BY id DESC LIMIT 1""")
        self.get_error_by_id = await self.db.prepare("""SELECT * FROM errors WHERE id = $1""")