import reademail
import time

count = 0
while(True):
    reademail.reademail()
    time.sleep(2)
    print count
    count += 2
