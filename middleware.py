import contextlib
import aioboto3
import config


session = aioboto3.Session()


class S3Middleware:
    __slots__ = ("_s3_resource", "_context_stack", "_resources")

    def __init__(self, resources):
        self._context_stack = contextlib.AsyncExitStack()
        self._s3_resource = None
        self._resources = resources

    async def process_startup(self, scope, event):
        self._s3_resource = await self._context_stack.enter_async_context(
            session.client('s3',
                           aws_access_key_id=config.AWS_KEY,
                           aws_secret_access_key=config.AWS_SECRET)
        )
        for r in self._resources:
            r.s3 = self._s3_resource
            # r.bucket = await self._s3_resource.Bucket(S3_BUCKET)

        print("Hello Middleware")

    async def process_shutdown(self, scope, event):
        await self._context_stack.aclose()
        print("Bye Middleware")
