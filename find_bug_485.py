

from solver import *
from incremental_solver import *

ops =  [u'if0', u'or', u'plus', u'shl1', u'shr16', u'tfold']
size = 12

table = get_all_graphs(size, ops)
check = collapse_table(table)
print 'Total functions = ', len(check)

points = [(2789245159971548692, 497693943335247057, 18333075476750278956L), (2307266683941581497, 7599723334012235164, 12568073944161868743L), (7883618184973541837, 9077893354896094611, 647428185899519925), (1544941801686878690, 16706990179954549270L, 13019411550371209286L), (15516769919813209666L, 4382381423515739655, 5547785924338764870), (0, 0, 0), (2594073385365405696, 16722059525100146250L, 11781394235203543875L)]
values = map(from_hex, ["0x0000000000000028","0x0000000000000022","0x000000000000006F","0x0000000000000017","0x00000000000000D9","0x0000000000000000","0x0000000000000024"])

v = values[-1]
res = add_mismatched(points[-1][0])
points = res + points
values = [v] * len(res) + values

assert len(points) == len(values)

xs = [p[0] for p in points]
index = find_first_good(check, 0, xs, values)
print check[index][1].dump()

print "now with hashing"

f = get_good_function(size, ops, points, values)



