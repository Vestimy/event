import os
import io
import boto3
import mimetypes

s3_client = boto3.client(
    's3',
    # endpoint_url='https//ams3.digitaloceanspaces.com',
    aws_access_key_id=os.environ.get('DO_SPACE_ACCESS'),
    aws_secret_access_key=os.environ.get('DO_SPACE_SECRET'),
    region_name='ams3'
)

def upload_video(local_path, path, bucket_name='video-space', acl='public-re'):
    with open(local_path, 'rb') as f:
        file = io.BytesIO(f.read())

    try:
        mimetype = mimetypes.guess_type(local_path)[0]
    except:
        raise Exception('Invalid file format')

    s3_client.upload_fileobj(
        file,
        bucket_name,
        path,
        ExtaArgs={
            'ACL': acl,
            'ContentType': 'video/mp4'
        }
    )
