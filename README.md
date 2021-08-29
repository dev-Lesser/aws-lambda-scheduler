## Create lambda function + s3 + EventBridge



### 1. Create Zip file
```bash
python create_zip_file.py --zipPath ./lambda_function --output output.zip
```
### 2. Create S3 bucket
```python
s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION,
    )
    
status = False
try:
    s3.create_bucket(
        ACL='private',
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={
            'LocationConstraint': REGION
        },
    )
    status = True
except Exception as ex:
    print(ex)
```

### 3. Create Event
```python
event_bridge = boto3.client(
    'events',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)
event_bridge.put_rule(
    Name='test_scheduler',
    ScheduleExpression='cron(0 9 * * ? *)', # make the your own rule 
    State='ENABLED',
    Description='test scheduler'
)
```
### 4. Create Lambda function
```python
lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

# ** You should have lambda-role in AWS IAM role **
res = lambda_client.create_function(
    Code={
        'S3Bucket': BUCKET_NAME,
        'S3Key': UPLOAD_FILENAME, 
    },
    Description='Scheduler',
    FunctionName=FUNCTION_NAME,
    Handler='lambda_function.lambda_handler',
    Publish=True,
    Timeout=600, # timeout 10 min 
    Role='arn:aws:iam::{user_id}:role/lambda-role'.format(user_id=USER_ID),
    Runtime='python3.8',
)
```

### .env
```
ACCESS_KEY=[YOUR KEY]
SECRET_KEY=[YOUR KEY]
REGION=ap-[YOUR REGION]

USER_ID=[YOUR USER ID]
```
