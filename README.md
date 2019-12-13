# Load Balancer

Load Balancer redirects http requests to random backend from predefined list. It is implemented as Google Cloud Function and the list of target backends should be placed on Google Storage.

## Setup:

1. Create text file with name of YOUR\_FUNCTION (e.g. lb) contained target backends, one backend per line like this:

```
http://backend-1.oz/base1/path1
http://backend-2.oz/base2/path2
http://backend-3.oz/base2/path3
```

The suffix /base/path is optional and could be anything whatever your need or nothing. In any way full path of request including query string would be appended to randomly choosen backend.

2. Create your bucket:

```
gsutil mb -l YOUR_REGION -p YOUR_PROJECT gs://YOUR_REGION-YOUR_PROJECT-cloudfunctions
```
where YOUR\_REGION is region where you place your function, e.g. us-east1 and YOUR\_PROJECT is project id witch all this stuff belongs to, e.g. project-1.

3. Upload backends list to the bucket:

```
cp YOUR_FUNCTION gs://YOUR_REGION-YOUR_PROJECT-cloudfunctions
```

4. Download source of the function and deploy it to the cloud:

```
git clone https://github.com/vstavrinov/lb.git
cd lb
gcloud functions deploy     \
    --project=YOUR_PROJECT  \
    --memory=128MB          \
    --runtime=python37      \
    --entry-point=lb        \
    --trigger-http          \
    --allow-unauthenticated \
    --region=YOUR_REGION    \
    YOUR_FUNCTION
```

That's all. From now all requests like this:

```
https://YOUR_REGION-YOUR_PROJECT.cloudfunctions.net/YOUR_FUNCTION/some_base/some_path?key1=value1&key2=value2
```

will be redirected to:

```
http://backend-1.oz/base1/path1/some_base/some_path?key1=value1&key2=value2
```

or

```
http://backend-2.oz/base2/path2/some_base/some_path?key1=value1&key2=value2
```

or

```
http://backend-3.oz/base3/path3/some_base/some_path?key1=value1&key2=value2
```

and so on.

## Caveat

There are no neither health check nor backend auto disable.

## Tools
gsutil and gcloud are parts of google-cloud-sdk. See:

```
https://cloud.google.com/sdk/docs/
```
