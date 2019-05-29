#python programm to print all the buckets from s3
import boto3
s3 = boto3.resource('s3')
for buckets in s3.buckets.all():
    print(buckets.name)


#Python programm to get all the files from s3
import boto3
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('bucket_name')
for file in my_bucket.objects.all():
    print (file.key)
