import falcon

import config


class S3Resource:
    async def file_reader(self, s3_obj):
        chunk_size = 4096
        async with s3_obj["Body"] as stream:
            file_data = await stream.read(chunk_size)
            while file_data:
                yield file_data
                file_data = await stream.read(chunk_size)

    async def on_get(self, req, resp, path):
        resp.status = falcon.HTTP_200
        path = path[1:] if path.startswith('/') else path
        s3_obj = await self.s3.get_object(Bucket=config.S3_BUCKET, Key=path)

        ob_info = s3_obj["ResponseMetadata"]["HTTPHeaders"]
        resp.content_type = ob_info["content-type"]
        resp.content_length = ob_info["content-length"]
        resp.stream = self.file_reader(s3_obj)