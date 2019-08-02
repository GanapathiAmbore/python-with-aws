from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import re,random,json,sys,boto3
def handler(event, context):
    domain=event['domain']
    url=event['url']
    page = urlopen(url,timeout=60)
    page_soup=soup(page,'html.parser')
    pages=[link.get("href") for link in page_soup.find_all("a",attrs={'href': re.compile("^http://")})]
    for urls in pages:
        ps=urlopen(urls)
        ps1=soup(ps,'html.parser')
        ps2=[l.get("href") for l in ps1.find_all("a",attrs={'href':re.compile("^/")})]
        for script in ps1(["script","style","button","nav"]):
            script.decompose()
        text = ps1.text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        container = {"url": urls, "leaves": pages, "links": ps2, "content": text}
        x = 123456789101
        y = 987654321012
        f = open("Title_updated.json", 'r')
        name = domain+ "-" + str(random.randint(x, y)) + ".json"
        title =domain+'/'+name
        s3 = boto3.resource('s3', aws_access_key_id='', aws_secret_access_key='')
        s3.Object('Bucket_name', title).put(Key=title,Body=json.dumps(container,indent=4))

