import discord
import requests

from bot import token


async def no_permission(message):
    embed = discord.Embed(title="Keine Rechte", description="Dazu hast du keine Rechte!", color=discord.Color(0xff0000))
    await message.reply(embed=embed)


class HTTPCodeErrors:
    class NoPermission(Exception):
        pass

    class ServerError(Exception):
        pass

    class NotFound(Exception):
        pass

    class Other(Exception):
        def __init__(self, code):
            self.code = code


def handle_code(responsecode):
    if responsecode < 300:
        return
    elif responsecode == 403:
        raise HTTPCodeErrors.NoPermission()
    elif responsecode == 500:
        raise HTTPCodeErrors.ServerError()
    elif responsecode == 404:
        raise HTTPCodeErrors.NotFound()
    else:
        raise HTTPCodeErrors.Other(responsecode)


def discord_get(url, params=None, session=None):
    request_headers = {"Authorization", f"Bot {token}"}
    session = requests.Session() if session is None else session

    response = session.get(f"https://discord.com/api/v9/{url}", params=params, headers=request_headers)
    handle_code(response.status_code)
    return response.json()


def discord_post(url, params=None, session=None):
    request_headers = {"Authorization", f"Bot {token}"}
    session = requests.Session() if session is None else session

    response = session.post(f"https://discord.com/api/v9/{url}", params=params, headers=request_headers)
    handle_code(response.status_code)
    return response.json()
