import asyncio

import falcon


class SleepResource:
    async def on_get(self, req, resp, seconds: int):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = f"Return response after sleep {seconds} s."
        await asyncio.sleep(int(seconds))