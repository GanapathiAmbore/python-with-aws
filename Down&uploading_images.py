from urllib.request import urlopen
from bs4 import BeautifulSoup
import re,boto3,sys,os
url=sys.argv[1]
domain=url.split('//')[1].split('.')[0]
s3=boto3.resource("s3")
html = urlopen(url)
bs = BeautifulSoup(html, 'html.parser')
for links in bs.find_all("a",attrs={'href':re.compile("^http://")}):
    pages=links.get("href")
    html=urlopen(pages)
    bs = BeautifulSoup(html, 'html.parser')
    JPEG = bs.find_all('img', {'src':re.compile('.jpg')})
    PNG=bs.find_all('img',{'src':re.compile('.png')})
    all_images=JPEG+PNG
    for image in all_images:
        url=image['src']+'\n'
        filename = url.split('/')[-1]
        with open(filename,'wb') as file:
            file.write(urlopen(url).read())
            s3.Bucket('imagedatas3').put_object(Key=domain+"/"+filename, Body=urlopen(url).read())







