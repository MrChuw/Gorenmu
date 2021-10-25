from requests import get
import random

def get_series(): 
    cs = 2 
    stillvalid = True
    while stillvalid:
        if get("http://www.scpwiki.com/scp-series-" + str(cs)).status_code == 404:
            cs -= 1
            return cs
        else:
            cs += 1

def get_random_number():
    get404 = True
    while get404:
        num = random.randint(1, (get_series() * 1000) - 1)
        num_str = ""
        if len(str(num)) == 1:
            num_str = "00" + str(num)
        elif len(str(num)) == 2:
            num_str = "0" + str(num)
        else:
            num_str = str(num)
        if get("http://www.scpwiki.com/scp-" + num_str).status_code != 404:
            return num_str