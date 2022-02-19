# Test function

Login to GCP.
```sh
gcloud auth login
```

Select your account
```sh
gcloud config set project antony-brd
```

Deploy the function
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

```sh

```




