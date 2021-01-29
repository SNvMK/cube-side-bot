import aiohttp


class Webhook:
    def __init__(self, url):
        self.url = url

    async def execute(self, content, embeds):
        payload = {}

        if content:
            payload["content"] = content

        if embeds:
            payload["embeds"] = embeds

        async with aiohttp.ClientSession() as s:
            async with s.post(self.url, json=payload) as r:
                return r.response