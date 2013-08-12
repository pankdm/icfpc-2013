import consts

import json
import requests


from time import time, sleep

from token import token
from consts import BASE_URL, LAST

def get_url(method):
	url =  "%s/%s?auth=%s" %(BASE_URL, method, token)
	print 'url = ', url
	return url

class Proxy:
	def __init__(self):
		self.last_request = None

	def make_guess(self, pid, program):
		print 'making guess request, program = ', program
		params = {"id": pid, "program": program}
		return self.internal_request("guess", params)

	def make_eval(self, pid, hex_input):
		print 'making eval request by id = ', pid
		params = {"id": pid, "arguments": hex_input}
		return self.internal_request("eval", params)

	def make_train(self, size, ops = []):
		print 'Getting train problem'
		params = {"size": size, "operators": ops}
		return self.internal_request("train", params)

	# private:
	def internal_request(self, method, params):
		while True:
			current = time()
			if self.last_request != None:
				delta = self.last_request + 4 - current
				print 'Waiting ', delta, 'seconds'
				if delta > 0:
					sleep(delta)

			js = json.dumps(params)
			r = requests.post(get_url(method), data=js)
			print 'Error code:', r.status_code
			print r.text[:1000]
			if str(r.status_code) == '429':
				print 'Waiting 10 seconds'
				sleep(10)
				continue

			data = json.loads(r.text)
			self.last_request = time()
			return data





