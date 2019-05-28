import json
tf=open("today.json.gz_out").read()
yf=open("yesterday.json.gz_out").read()
today_file=json.dumps(tf,sort_keys=True)
yesterday_file=json.dumps(yf,sort_keys=True)
print(today_file==yesterday_file)
