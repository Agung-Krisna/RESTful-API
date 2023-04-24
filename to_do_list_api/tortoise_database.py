from tortoise import Tortoise

async def dbInit():
    await Tortoise.init(db_url="sqlite://./todo.db", modules={"models": ["tortoise_models"]})