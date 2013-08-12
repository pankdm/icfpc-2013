
import requests
import json
from token import token

def get_train_problem(size):
	BASE_URL = "http://icfpc2013.cloudapp.net/"
	params = {"size": size, "operators": []}
	r = requests.post("%s/train?auth=%s" %(BASE_URL, token), data=json.dumps(params))
	print r.text
	data = json.loads(r.text)
	return data

def solve(p):
	assert p["size"] == 3


p = get_train_problem(3)








