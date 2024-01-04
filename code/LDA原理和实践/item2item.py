import sys
import math
import heapq
from heapq import heappush, heappop

items_D = {} ## key: id

CNT = 0

class pq:
    def __init__(self, k):
        self._queue = []
        self._k = k;

    def push(self, item, priority):
        heappush(self._queue, (priority, item))
        while len(self._queue) > self._k:
            heappop(self._queue)

    def get_all(self):
        return sorted(self._queue, cmp=lambda x,y:cmp(x[0],y[0]))


def load_data():
    global items_D
    inFp = open("lda_desc_formatted.csv", 'r')
    while True:
        line = inFp.readline()
        if not line:
            break
        items = line.strip().split(',')
        if len(items) != 54:
            continue
        item_D = {}
        item_D['soft_package_name'] = items[2]
        item_D['name'] = items[1]
        item_D['id'] = int(items[0])
        item_D['topics'] = map(float, items[3:53])
        item_D['sum'] = float(items[53])
        items_D[item_D['id']] = item_D
    print len(items_D)


def dis1(A, B):
    return sum( A['topics'][i] * B['topics'][i] for i in range(50))

def dis2(A, B):
    return sum( 100 - abs(A['topics'][i] - B['topics'][i]) for i in range(50))

def search_similar():
    while True:
        line = sys.stdin.readline()
        idx = int(line.strip())
        itemX = items_D[idx]
        sim = -1.0
        for idy, itemy in items_D.items():
            simy = dis1(items_D[idx], items_D[idy])
            if simy > sim and idx!=idy:
                sim = simy
                itemY = itemy
        print "%s\tass\t%s"%(itemX['name'], itemY['name'])

def find_all_similar():
    outFp = open("lda_item2item", 'w')
    for idx, itemx in items_D.items():
        pqx = pq(5)
        for idy, itemy in items_D.items():
            pqx.push(itemy, dis1(itemx,itemy))
        res_L = pqx.get_all()
        for i in range(5):
            outFp.write("%d\t%s\t%s\t%d\t%s\t%s\t%d\tlda_desc\n"%( itemx['id'], \
                    itemx['soft_package_name'], \
                    itemx['name'], \
                    res_L[i][1]['id'], \
                    res_L[i][1]['soft_package_name'], \
                    res_L[i][1]['name'], \
                    i+1))
        """
        print "%d\t%s\t%s,%.3f\t%s,%.3f\t%s,%.3f\t%s,%.3f\t%s,%.3f" % ( itemx['id'], \
                itemx['name'], \
                res_L[0][1]['name'], res_L[0][0],\
                res_L[1][1]['name'], res_L[1][0],\
                res_L[2][1]['name'], res_L[2][0],\
                res_L[3][1]['name'], res_L[3][0],\
                res_L[4][1]['name'], res_L[4][0])
        """

load_data()
#search_similar()
find_all_similar()

