

import collections
import pandas as pd
import phe
import time
from functools import cmp_to_key
import keypair
import protocol as phe_protocol
import sspld

def mycmp(x,y):
   return phe_protocol.PHEProtocol(x[1]).pin_boolmore(y[1])
def lastans(ans,k):
    a = collections.OrderedDict(sorted(ans.items(), key=cmp_to_key(mycmp)))
    b = []
    cnt = 0
    for i in a:
        if cnt<k:
            b.append(i)
    return b



def SSD(p0,p1):
    return  phe_protocol.PHEProtocol(p0[0] - p1[0]).phe_pow() + phe_protocol.PHEProtocol(p0[1] - p1[1]).phe_pow()
def sminxy(pk,index):
    x=pk.encrypt(10000000000)
    y= pk.encrypt(10000000000)
    for p in index:
        x=phe_protocol.PHEProtocol(p[0]).phe_min(x)
        y=phe_protocol.PHEProtocol(p[1]).phe_min(y)
    return [x,y]
def smaxxy(pk,index):
    x = pk.encrypt(-10000000000)
    y = pk.encrypt(-10000000000)
    for p in index:
        x = phe_protocol.PHEProtocol(p[0]).phe_max(x)
        y = phe_protocol.PHEProtocol(p[1]).phe_max(y)
    return [x,y]
def enpoint(pk):
    point = [[96, 94], [164, 64], [67, 150], [104, 190], [190, 209], [221, 233], [230, 307], [200, 290], [413, 47],
             [380, 95], [566, 30], [676, 58], [786, 104], [750, 50], [437, 324], [543, 267], [470, 454], [399, 389],
             [827, 394], [753, 448], [786, 583], [826, 513], [957, 676], [926, 533], [891, 785], [757, 770], [962, 814],
             [981, 773], [595, 983], [677, 853], [542, 892], [476, 835], [282, 895], [400, 950], [185, 9], [220, 39],
             [65, 570], [100, 620], [180, 581], [200, 600], [70, 521], [88, 550], [66, 380], [160, 420], [500, 508],
             [552, 562], [806, 812], [861, 909], ]
    enoint=[]
    for p in point:
        enoint.append([pk.encrypt(p[0]),pk.encrypt(p[1])])
    return enoint

class BinaryTree:

    def __init__(self):
        self.val = None
        self.left = None
        self.mid = None
        self.right = None
        self.index = []
        self.child = []
        self.minxy = []
        self.maxxy = []


    def bulidTree(self, arrs,p,pk):
        if not len(arrs):
            return None
        if arrs[0]=='null':
            self.val = None
            arrs.pop(0)
            return
        elif arrs[0]=='*':
            self.val = '*'
            arrs.pop(0)
            zindex = int(arrs[0])
            self.index.append(p[zindex])
            self.child.append(zindex)
            arrs.pop(0)
            zindex = int(arrs[0])
            self.index.append(p[zindex])
            self.child.append(zindex)
            arrs.pop(0)
            return
        else:
            self.val = arrs[0]
            arrs.pop(0)
            self.left = BinaryTree()
            self.mid = BinaryTree()
            self.right = BinaryTree()
            self.left.bulidTree(arrs,p,pk)
            self.index.extend(self.left.index)
            self.mid.bulidTree(arrs,p,pk)
            self.index.extend(self.mid.index)
            self.right.bulidTree(arrs,p,pk)
            self.index.extend(self.right.index)
            self.minxy=sminxy(pk,self.index).copy()
            self.maxxy=smaxxy(pk,self.index).copy()


    def levelBulidTree(self, arrs):
        # 递归建树
        def add(self, val):
            queue = [self]
            while len(queue):
                head = queue[0]
                queue.pop(0)

                if head.left == None:
                    head.left = BinaryTree()
                    head.left.val = val
                    return
                elif head.mid == None:
                    head.mid = BinaryTree()
                    head.mid.val = val
                    return
                elif head.right == None:
                    head.right = BinaryTree()
                    head.right.val = val
                    return
                else:
                    queue.append(head.left)
                    queue.append(head.mid)
                    queue.append(head.right)

        if not len(arrs):
            return None
        self.val = arrs[0]
        for i in range(1, len(arrs)):
            add(self, arrs[i])


    def preTravel(self):
        if self.val == None or self.val == 'null':
            print('null', end=',')
            return
        else:
            print(self.val, end=',')
            if self.left != None:
                self.left.preTravel()
            if self.mid != None:
                self.mid.preTravel()
            if self.right != None:
                self.right.preTravel()
    def isinrect(self,point):
        if self.val==None or self.val=='null':
            return -1
        elif phe_protocol.PHEProtocol(point[0]).pin_boolmore(self.minxy[0]) and phe_protocol.PHEProtocol(self.maxxy[0]).pin_boolmore(point[0]) and phe_protocol.PHEProtocol(point[1]).pin_boolmore(self.minxy[1]) and phe_protocol.PHEProtocol(self.maxxy[1]).pin_boolmore(point[1]):
            return 1
        else:
            return 0
    def mindist(self,point,pk):
        if self.isinrect(point)==1:
            return pk.encrypt(0)
        elif self.isinrect(point)==-1:
            return pk.encrypt(10000)
        else:
            min1 = sspld.phe_sspld(pk,point,[self.minxy[0],self.minxy[1]],[self.maxxy[0], self.minxy[1]])
            min2 = sspld.phe_sspld(pk,point,[self.minxy[0],self.minxy[1]],[self.minxy[0], self.maxxy[1]])
            min3 = sspld.phe_sspld(pk,point, [self.maxxy[0], self.maxxy[1]],[self.maxxy[0], self.minxy[1]])
            min4 = sspld.phe_sspld(pk,point, [self.maxxy[0], self.maxxy[1]],[self.minxy[0], self.maxxy[1]])
            min5 = SSD(point,[self.minxy[0],self.minxy[1]])
            min6 = SSD(point, [self.minxy[0], self.maxxy[1]])
            min7 = SSD(point, [self.maxxy[0], self.minxy[1]])
            min8 = SSD(point, [self.maxxy[0], self.maxxy[1]])
            return phe_protocol.PHEProtocol(phe_protocol.PHEProtocol(phe_protocol.PHEProtocol(phe_protocol.PHEProtocol(phe_protocol.PHEProtocol(phe_protocol.PHEProtocol(phe_protocol.PHEProtocol(min1).phe_min(min2)).phe_min(min3)).phe_min(min4)).phe_min(min5)).phe_min(min6)).phe_min(min7)).phe_min(min8)
    def minmaxdist(self,point,pk):
        min1 = sspld.phe_sspld(pk,point, [self.minxy[0], self.minxy[1]], [self.maxxy[0], self.minxy[1]])
        min2 = sspld.phe_sspld(pk,point, [self.minxy[0], self.minxy[1]], [self.minxy[0], self.maxxy[1]])
        min3 = sspld.phe_sspld(pk,point, [self.maxxy[0], self.maxxy[1]], [self.maxxy[0], self.minxy[1]])
        min4 = sspld.phe_sspld(pk,point, [self.maxxy[0], self.maxxy[1]], [self.minxy[0], self.maxxy[1]])
        if phe_protocol.PHEProtocol(min2).pin_boolmore(min1) and phe_protocol.PHEProtocol(min3).pin_boolmore(min1)and phe_protocol.PHEProtocol(min4).pin_boolmore(min1):
            return phe_protocol.PHEProtocol(SSD(point,[self.minxy[0], self.minxy[1]])).phe_max(SSD(point,[self.maxxy[0], self.minxy[1]]))
        elif phe_protocol.PHEProtocol(min1).pin_boolmore(min2) and phe_protocol.PHEProtocol(min3).pin_boolmore(min2) and phe_protocol.PHEProtocol(min4).pin_boolmore(min2):
            return phe_protocol.PHEProtocol(SSD(point, [self.minxy[0], self.minxy[1]])).phe_max(SSD(point, [self.minxy[0], self.maxxy[1]]))
        elif phe_protocol.PHEProtocol(min1).pin_boolmore(min3) and phe_protocol.PHEProtocol(min2).pin_boolmore(min3) and  phe_protocol.PHEProtocol(min4).pin_boolmore(min3):
            return phe_protocol.PHEProtocol(SSD(point, [self.maxxy[0], self.maxxy[1]])).phe_max(SSD(point, [self.maxxy[0], self.minxy[1]]))
        elif phe_protocol.PHEProtocol(min1).pin_boolmore(min4) and phe_protocol.PHEProtocol(min2).pin_boolmore(min4) and phe_protocol.PHEProtocol(min3).pin_boolmore(min4):
            return phe_protocol.PHEProtocol(SSD(point, [self.maxxy[0], self.maxxy[1]])).phe_max(SSD(point, [self.minxy[0], self.maxxy[1]]))

    def knn(self,qx, qy, k,pk):
        ans={}
        anspoint={}
        qpoint = [pk.encrypt(qx), pk.encrypt(qy)]
        qunne = [self]
        mindistv =pk.encrypt(1000000)
        minmaxdistv = pk.encrypt(1000000)
        dist = pk.encrypt(1000000)

        while len(qunne) != 0:
            start=time.time()
            node = qunne.pop(0)


            if node.left.val=='*':
                dist0=SSD(qpoint, node.left.index[0])
                end0 = time.time()
                dist1=SSD(qpoint, node.left.index[1])
                end1 = time.time()
                dist = phe_protocol.PHEProtocol(phe_protocol.PHEProtocol(dist0).phe_min(dist1)).phe_min(dist)
                anspoint[node.left.child[0]] = dist0
                anspoint[node.left.child[1]] = dist1
                end = time.time()
                ans[node.val] = (end - start) * 1000
                ans[node.left.child[0]] = (end0 - start) * 1000
                ans[node.left.child[1]] = (end1 - start) * 1000
                continue
            leftmindist=node.left.mindist(qpoint,pk)
            midmindist= node.mid.mindist(qpoint,pk)
            rightmindist=node.right.mindist(qpoint,pk)

            if phe_protocol.PHEProtocol(minmaxdistv).pin_boolmore(leftmindist)  and node.left is not None and node.left.val !='null' and node.left.val !=None and phe_protocol.PHEProtocol(dist).pin_boolmore(leftmindist):
                qunne.append(node.left)
                mindistv=phe_protocol.PHEProtocol(leftmindist).phe_min(mindistv)
                minmaxdistv=phe_protocol.PHEProtocol(node.left.minmaxdist(qpoint,pk)).phe_min(minmaxdistv)
            if phe_protocol.PHEProtocol(minmaxdistv).pin_boolmore(midmindist)  and node.mid is not None and node.mid.val !='null' and node.mid.val !=None and phe_protocol.PHEProtocol(dist).pin_boolmore(midmindist):
                qunne.append(node.mid)
                mindistv=phe_protocol.PHEProtocol(midmindist).phe_min(mindistv)
                minmaxdistv=phe_protocol.PHEProtocol(node.mid.minmaxdist(qpoint,pk)).phe_min(minmaxdistv)
            if phe_protocol.PHEProtocol(minmaxdistv).pin_boolmore(rightmindist)  and node.right is not None and node.right.val !='null' and node.right.val !=None and phe_protocol.PHEProtocol(dist).pin_boolmore(rightmindist):
                qunne.append(node.right)
                mindistv=phe_protocol.PHEProtocol(rightmindist).phe_min(mindistv)
                minmaxdistv=phe_protocol.PHEProtocol(node.right.minmaxdist(qpoint,pk)).phe_min(minmaxdistv)
            end = time.time()
            ans[node.val]=(end-start)*1000


        return lastans(anspoint,k),ans


def sknn(qx, qy, k,length):
    arr = [' root ', ' R0 ', ' R3 ', ' R6 ', '*', '14', '15', 'null', 'null', ' R7 ', '*', '16', '17', 'null',
           'null', ' R8 ', '*', '44', '45', 'null', 'null', ' R4 ', ' R12 ', '*', '8', '9', 'null', 'null', ' R13 ',
           '*', '10', '11', 'null', 'null', ' R14 ', '*', '12', '13', 'null', 'null', ' R5 ', ' R9 ', '*', '18',
           '19', 'null', 'null', ' R10 ', '*', '20', '21', 'null', 'null', ' R11 ', '*', '22', '23', 'null', 'null',
           ' R1 ', ' R27 ', ' R30 ', '*', '32', '33', 'null', 'null', ' R31 ', '*', '30', '31', 'null', 'null',
           ' R32 ', '*', '28', '29', 'null', 'null', ' R28 ', ' R33 ', '*', '46', '47', 'null', 'null', ' R34 ',
           '*', '24', '25', 'null', 'null', ' R35 ', '*', '26', '27', 'null', 'null', 'null', ' R2 ', ' R15 ',
           ' R18 ', '*', '2', '3', 'null', 'null', ' R19 ', '*', '0', '1', 'null', 'null', ' R20 ', '*', '34', '35',
           'null', 'null', ' R16 ', ' R21 ', '*', '42', '43', 'null', 'null', ' R22 ', '*', '4', '5', 'null',
           'null', ' R23 ', '*', '6', '7', 'null', 'null', ' R17 ', ' R24 ', '*', '36', '37', 'null', 'null',
           ' R25 ', '*', '41', '40', 'null', 'null', ' R26 ', '*', '38', '39', 'null', 'null']
    keypair.generate_keypair(length)
    pk = phe.PaillierPublicKey(n=int(pd.read_pickle(keypair.PUBLIC_KEY_PATH).loc['n'][0]))
    a = BinaryTree()
    point = enpoint(pk)
    a.bulidTree(arr, point,pk)
    return  a.knn(qx, qy, k,pk)


if __name__ == '__main__':
    print(sknn(600,200,8,128))



