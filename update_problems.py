import consts


from proxy import *


r = requests.post(get_url("myproblems"))

f = open("problems.json", "wt")
f.write(r.text)
f.close()


