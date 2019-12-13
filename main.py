def lb(request):
    from random import choice
    from os import environ
    from flask import Response
    from google.cloud import storage

    path = request.full_path
    if path[1] == '?':
        path = path.strip('/')
    bucket_name = environ['FUNCTION_REGION'] + '-' + environ['GCP_PROJECT'] + '-cloudfunctions'
    blob_name = environ['FUNCTION_NAME']
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = storage.Blob(blob_name, bucket)
    blob_content = blob.download_as_string()
    host = choice(blob_content.decode().splitlines())
    url = host + path
    response = Response('', content_type='text/plain')
    response.headers['Location'] = url
    response.status_code = 302
    return response
