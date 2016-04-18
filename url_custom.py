import redis
import post_save
import cPickle
import os
if __name__=="__main__":
   s=redis.StrictRedis('172.16.3.190')
   os.popen("rm -f /tmp/the.lock")
   for i in range(10):
       if os.fork():
           break
   while True:
     print "heffasdf"
     url_tuple_tem=s.brpop("my_urls")

     print url_tuple_tem
     print type(url_tuple_tem)
     url_tuple=cPickle.loads(url_tuple_tem[1])
     print url_tuple
     post_save.save_post1(url_tuple[0],url_tuple[1])
     print "end"
     # except:
     #   print "some error"
   # while True:
   #    print "hehe"