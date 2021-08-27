import boto3
from dotenv import load_dotenv
import os
import argparse

if __name__ == '__main__':
    load_dotenv(verbose=True)
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    REGION = os.getenv('REGION')
    USER_ID = os.getenv('USER_ID')


    parser = argparse.ArgumentParser(description='Process Create ECR repo & push docker image')
    parser.add_argument('--bucket', required=True, help="S3 bucket name")
    parser.add_argument('--zipPath', required=True, default="output.zip", help="upload zip file path")
    parser.add_argument('--fileName', required=True, help="upload zip file name")
    parser.add_argument('--funcName', required=True, help="lambda function name")

    args = parser.parse_args()


    BUCKET_NAME = args.bucket
    UPLOAD_PATH = args.zipPath
    UPLOAD_FILENAME = args.fileName
    FUNCTION_NAME = args.funcName
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
    assert status, "Please change your bucket name OR %s" % ex

    s3.upload_file(
        UPLOAD_PATH, 
        BUCKET_NAME, 
         UPLOAD_FILENAME
    )

    # create schedule event
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
    print(res)