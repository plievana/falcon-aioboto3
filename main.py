import falcon
import falcon.asgi
import uvicorn

from middleware import S3Middleware
from resources.s3 import S3Resource
from resources.sleep import SleepResource
from resources.root import RootResource
import logging


class FileSinkAdapter(object):
    def __init__(self, resource):
        self.resource = resource

    async def __call__(self, req: falcon.Request, resp: falcon.Response, path: str, **kwargs):
        responder_method = 'on_' + req.method.lower()
        method = getattr(self.resource, responder_method)
        try:
            await method(req, resp, path, **kwargs)

        except Exception as exc:
            resp.media = {'msg': str(exc)}
            resp.status = falcon.HTTP_500
            logging.error(str(exc), exc_info=True)


def create_app():
    root = RootResource()
    sl = SleepResource()
    s3_resource = S3Resource()
    s3middleware = S3Middleware([s3_resource])
    s3 = FileSinkAdapter(s3_resource)

    app = falcon.asgi.App(middleware=(s3middleware,))
    app.add_sink(s3, r'/s3(?P<path>/.*)\Z')

    app.add_route('/', root)
    app.add_route('/sleep/{seconds}', sl)

    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
