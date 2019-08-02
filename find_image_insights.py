import json,boto3,sys
client=boto3.client('rekognition')
s3=boto3.resource('s3')
bucket=s3.Bucket('imagedatas3')
for filename in bucket.objects.all():
    name=filename.key
    response = client.detect_labels(
        Image={

            'S3Object': {
                'Bucket': 'imagedatas3',
                'Name': name,

            }
        },
        MaxLabels=100,

    )
    f=open('response.json','w')
    f.write(json.dumps(response,indent=4))
