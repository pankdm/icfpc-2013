

from solver import *

from sys import argv

num = int(argv[1])

if len(argv) == 2:
	mode = []
else: mode = [argv[2]]

random.seed(0)
Config.TRAINING = True
# p = proxy.make_train(8, ["tfold"])
# p = proxy.make_train(12, mode)
# p = proxy.make_train(14)
p = proxy.make_train(num, mode)
solve(p)
