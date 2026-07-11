import aiosqlite

DB_NAME = "database.db"


async def create_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT UNIQUE,
            channel_name TEXT
        )
        """)
        await db.commit()


async def add_channel(channel_id, channel_name):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO channels (channel_id, channel_name) VALUES (?, ?)",
            (channel_id, channel_name)
        )
        await db.commit()


async def remove_channel(channel_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "DELETE FROM channels WHERE channel_id = ?",
            (channel_id,)
        )
        await db.commit()


async def get_channels():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT channel_id, channel_name FROM channels"
        )
        return await cursor.fetchall()
