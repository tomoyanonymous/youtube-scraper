import os
from datetime import datetime
import crawler_lib as crawler

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
