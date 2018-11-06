import os
from datetime import datetime
import crawler_lib as crawler
import json

dirs = os.listdir("./scraped_images")

for dir in dirs:
    if not os.path.isfile(dir):
        print("opening " , dir)
        path = "./scraped_images/"+dir+"/data.json"
        f = open(path)
        data = json.load(f)
        crawler.urllist=[]
        if len(data)>100:
            print("data is collected. skip")
        else:
            for i in range(len(data)):
                crawler.urllist.append(data[i].get("url"))
            count = len(data)
            crawler.dest = "./scraped_images/"+dir
            defurl = data[-1].get("url")
            crawler.myjson = data
            crawler.mainfun(count,defurl)
numtrying = 0
while numtrying<100:
    crawler.timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    crawler.cwd = os.path.abspath(os.curdir)
    crawler.dest = "scraped_images/youtube-"+str(crawler.timestamp)
    os.mkdir(crawler.dest)
    crawler.myjson =[]
    crawler.count = 0
    crawler.urllist = []
    crawler.mainfun() #main!!!!!!!!!!!!!!!!!!
    numtrying+=1
crawler.s.close()
