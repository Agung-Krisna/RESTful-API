from tortoise_database import dbInit
from tortoise import run_async, Tortoise


async def main():
    await dbInit()
    await Tortoise.generate_schemas()

if __name__ == "__main__":
    run_async(main())