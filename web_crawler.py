from bs4 import BeautifulSoup as soup
from urllib.request import urlopen,urljoin
import json,boto3,sys,re,random,time,datetime
s3 = boto3.resource('s3')
bucket = s3.Bucket('crewler-data')
domain=sys.argv[1]
url=sys.argv[2]
start_time =str(datetime.datetime.now())
print("start_Time_is",start_time)
s3files={}
for file in bucket.objects.filter(Prefix=domain):
    title=file.key
    time=file.last_modified
    body = file.get()['Body'].read()
    data=json.loads(body)
    for key,value in data.items():
        if "url" in key:
            s3files[value]=[str(time),title]
timestamp=[time[1][0] for time in s3files.items()]
All_URLS=set()#Empty set to add all the urls of given domain
page = urlopen(url)
page_soup=soup(page,'html.parser')
Absolute_urls={links["href"] for links in page_soup.find_all("a",attrs={'href':re.compile('^http://')})}
Relative_urls={url+links["href"] for links in page_soup.find_all("a",attrs={'href':re.compile('^/')})}
all_links=Absolute_urls.union(Relative_urls)
for urls in all_links:
    All_URLS.add(urls)
    page = urlopen(urls)
    page_soup=soup(page,'html.parser')
    Absolute_urls={links.get("href") for links in page_soup.find_all("a",attrs={'href':re.compile('^http://')})}
    Relative_urls={url+links["href"] for links in page_soup.find_all("a",attrs={'href':re.compile('^/')})}
    All_links=Absolute_urls.union(Relative_urls)
    Edgeurls={links for links in All_links if links not in all_links}
    for urls in Edgeurls:
        All_URLS.add(urls)
        page = urlopen(urls)
        page_soup=soup(page,'html.parser')
        Absolute_urls={links.get("href") for links in page_soup.find_all("a",attrs={'href':re.compile('^http://')})}
        Relative_urls={url+links["href"] for links in page_soup.find_all("a",attrs={'href':re.compile('^/')})}
        All_links=Absolute_urls.union(Relative_urls)
        Edgeurls={links for links in All_links if links not in all_links}
        for urls in Edgeurls:
            All_URLS.add(urls)
            page = urlopen(urls)
            page_soup=soup(page,'html.parser')
            Absolute_urls=[links.get("href") for links in page_soup.find_all("a",attrs={'href':re.compile('^http://')})]
            Relative_urls=[url+links["href"] for links in page_soup.find_all("a",attrs={'href':re.compile('^/')})]
            All_links=Absolute_urls+Relative_urls
            Edgeurls=[links for links in All_links if links not in all_links]
for urls in All_URLS:#Start crawling all the urls of web page
    if urls in s3files and str(timestamp)<start_time:
        print("Proceed to crawl the page!!")
    elif urls in s3files and str(timestamp)>start_time:
        print("Skip the crawling page!!")
    elif urls not in s3files:
        s3files[urls]=str(datetime.datetime.now())
        print("New url found!!",urls)
        page = urlopen(urls)
        page_soup=soup(page,'html.parser')
        Absolute_urls=[links.get("href") for links in page_soup.find_all("a",attrs={'href':re.compile('^http://')})]
        Relative_urls=[url+links["href"] for links in page_soup.find_all("a",attrs={'href':re.compile('^/')})]
        All_links=Absolute_urls+(Relative_urls)
        for script in page_soup(["script","style","button","nav"]):
            script.decompose()
        text = page_soup.text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        container={"url":urls,"Edges":All_links,"content":text}
        x = 123456789101
        y = 987654321012
        name = domain+ "-" + str(random.randint(x, y)) + ".json"
        titles=domain+"/"+name
        files = open(name, 'w')
        files.write(json.dumps(container,indent=4))
        s3.Bucket('crewler-data').put_object(Key=titles,Body=json.dumps(container,indent=4))
        print("newfile created",urls)





