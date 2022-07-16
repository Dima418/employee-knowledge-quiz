import random
import string


async def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


async def random_email() -> str:
    return f"{await random_lower_string()}@{await random_lower_string()}.com"
