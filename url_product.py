# -*- coding: utf-8 -*-
import redis
import time
import uuid
import cPickle
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
s=redis.StrictRedis('localhost')
watch_path ="url-data/"
type_list=["GRE","kaoyan","TOEFL","SAT","IELTS","GMAT"]
class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        url_path=event.src_path
        print url_path
        with open(url_path,"rb") as f:
            subprocess.call(["mv",url_path,url_path+str(uuid.uuid4().hex)])
            try:
              url_list=json.load(f)
              for item in url_list:
                 if not s.get(item["link"]) and item["name_type"] in type_list:
                    s.set(item["link"],1)
                    s.lpush("my_urls",cPickle.dumps((item["link"],item["name_type"])))
            except Exception:
                print "some error"
if __name__=="__main__":
    observer = Observer()
    observer.schedule(MyEventHandler(), watch_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1000)#每隔一秒醒来一次
    except KeyboardInterrupt:
        observer.stop()
    observer.join()