import aiohttp


class Webhook:
    def __init__(self, url):
        self.url = url

    async def execute(self, username=None, avatar=None, content=None, embeds=None):
        payload = {}
        headers = {
            "Content-Type": "application/json"
        }

        if content:
            payload["content"] = content

        if embeds:
            payload["embeds"] = embeds

        if username:
            payload["username"] = username
        
        if avatar:
            payload["avatar_url"] = avatar

        async with aiohttp.ClientSession() as s:
            async with s.post(self.url, json=payload, headers=headers) as r:
                print(r)