import sys

class Config:
	TRAINING = False

def get_MAX_SIZE():
	if Config.TRAINING: return TRAIN_MAX_SIZE
	else: return MAX_SIZE

def get_MAX_GRAPHS():
	if Config.TRAINING: return TRAIN_MAX_GRAPHS
	else: return MAX_GRAPHS

MAX_SIZE  = 13
MAX_GRAPHS = 10*10**6

TRAIN_MAX_SIZE = 13
TRAIN_MAX_GRAPHS = 8*10**6

sys.dont_write_bytecode = True

BASE_URL = "http://icfpc2013.cloudapp.net"
LAST = 0xffffffffffffffff

