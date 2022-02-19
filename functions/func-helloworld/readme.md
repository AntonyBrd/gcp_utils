# Test function

## Test locally this function

See Official Google Documentation :
* [GCP Doc](https://cloud.google.com/functions/docs/running/function-frameworks#functions-local-ff-install-python)
* [Github](https://github.com/GoogleCloudPlatform/functions-framework-python)

Make sure you have a virtual env up and running:
```sh
python -m venv func
source func/Scripts/activate

pip install functions-framework
```

Start your function server
```sh
cd ./functions/func_helloworld
functions_framework --target=hello_http
```

Call your function
```sh
$ curl -X POST -H "Content-Type: application/cloudevents+json" -d "{\"name\": \"toto\"}" http://192.168.1.86:8080/
```

## Deploy this function

Login to GCP.
```sh
gcloud auth login
```

Select your account.
```sh
gcloud config set project antony-brd
```

Deploy the function.
```sh
gcloud functions deploy func_helloworld \
    --entry-point hello_http \
    --runtime python39 \
    --source func-helloworld \
    --trigger-http \
    --allow-unauthenticated \
    --region europe-west1 \
    --service-account github-actions@antony-brd.iam.gserviceaccount.com 
```

## To deploy on GCP

In order to make my CI CD pipeline working I had to give a specific right to my service account:

```sh
gcloud iam service-accounts \
   add-iam-policy-binding github-actions@antony-brd.iam.gserviceaccount.com  \
   --member='serviceAccount:github-actions@antony-brd.iam.gserviceaccount.com' \
   --role=roles/iam.serviceAccountUser
```



