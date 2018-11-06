from requests_html import HTMLSession
import time #to use sleep function
import requests
import random
import re
import os
import json
from datetime import datetime

timestamp = ""
cwd = os.path.abspath(os.curdir)
dest = "scraped_images/youtube-"+str(timestamp)
myjson =[]
count = 0
urllist = []
s = HTMLSession()
numtrying = 0

def download_file(url,count,title):
    url = url.rsplit('?')[0]#remove query
    prefix = url.rsplit(".")[-1]
    urllist = url.split('/')
    joinedurl = urllist[-2]+"."+prefix
    title = re.sub('\W', '-', title)
    local_filename = os.path.join(dest,str(count)+"_"+title+"_"+joinedurl)
    print("thumb_img:",local_filename)
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


def search_nexturl(index, urllist,videolist):
    print("counting, ",index)
    urls = videos[index].absolute_links
    for url in urls:
        print(url)
        if index>10:
            print("index exceeded 10")
            return False
        else:
            if (url in urllist):
                print("duplicating. searching next")
                search_nexturl(index+1,urllist,videolist)#recursive
            else:
                print("new url. append to list")
                urllist.append(url)
                res = [index,url]
                return res


def get_firstlink(url,count,urllist,vcount,_json=None):
    print("Moved to next page. ",url)
    href=""
    r = s.get(url)
    r.html.render(sleep=2.5,timeout=10.)# need to sleep to get sidebars...
    videos =r.html.find("#thumbnail")
    titles =r.html.find("#video-title")
#     nextlink = search_nexturl(0,urllist,videos)
    check =True

    print("number-of-videos",len(titles))
    while(check):
        if vcount>10 or vcount>=len(videos):
            print("count exceeded 10,break")
            nextlink=False
            break
        href = videos[vcount].attrs.get("href")
        if (href != None):
            temphref = href
            is_playlist = (temphref.split("/")[-1].rsplit("?")[0] == "playlist")
            skipmsg = "Skip Because of "
            is_ad   =  ("googleads" in href)
            is_list = ("list" in href)


            skipmsg+= "Ads " if is_ad else ""
            skipmsg+= "mixlist " if is_list else ""
            skipmsg+=  "playlist " if is_playlist else ""
            href = href.split("&")[0]
            url = "https://youtube.com"+href
            is_duplicate = url in urllist
            skipmsg+=  "duplicate" if is_duplicate else ""
            videoid = href.rsplit("=")[-1]
            is_skip = (is_list or is_playlist or is_ad or is_duplicate)
            if(is_skip):
                print(skipmsg)
                vcount+=1
            else:
                urllist.append(url)
                nextlink=url
                check=False
                break
        else:
            vcount+=1

    if nextlink!=False:
        mydict= {}
        # print(nextlink)
        nexturl = nextlink

        thum_url = "https://i.ytimg.com/vi/"+videoid+"/hqdefault.jpg"
        title= titles[vcount].attrs.get("title")
        print(count,title,nexturl)
        localfilename = download_file(thum_url,count,title)
        mydict["url"]=nexturl
        mydict["thum_url"]=thum_url
        mydict["localfilename"]=localfilename
        mydict["title"]=title
        myjson.append(mydict)
        fname = dest+"/data.json"
        f = open(fname, "w")
        json.dump(myjson, f, ensure_ascii=False)
        return nexturl
    else:
        print("no url,end")
        return False

def mainfun(_count=0,_defurl=None,resumejson=None):
    defurl = "https://www.youtube.com/watch?v=lCAdCzyuReg" if (_defurl==None) else _defurl
    nexturl = defurl
    print(str(numtrying).center(50,"#"))
    count=_count
    while count<100:
        vcount = 0 if count==0 else 0
        nexturl = get_firstlink(nexturl,count,urllist,vcount,resumejson)
        if nexturl:
            count+=1
    #         time.sleep(0.2)
        else:
            break
