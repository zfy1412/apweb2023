import math
import numpy as np

def line(p, a, b):
    a, b, p = np.array(a), np.array(b), np.array(p)	 # trans to np.array
    d = np.divide(b - a, np.linalg.norm(b - a))	# normalized tangent vector
    s = np.dot(a - p, d)	# signed parallel distance components
    t = np.dot(p - b, d)
    h = np.maximum.reduce([s, t, 0])	# clamped parallel distance
    c = np.cross(p - a, d)  # perpendicular distance component
    return np.hypot(h, np.linalg.norm(c))
def ptp(a,b):
    return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))
def minxy(index):
    x=10000000000
    y=10000000000
    for p in index:
        x=min(p[0],x)
        y=min(p[1],y)
    return [x,y]
def maxxy(index):
    x=-10000000000
    y=-10000000000
    for p in index:
        x=max(p[0],x)
        y=max(p[1],y)
    return [x,y]

class BinaryTree:
    '''定义一个树'''

    def __init__(self):
        self.val = None
        self.left = None
        self.mid = None
        self.right = None
        self.index = []
        self.minxy = []
        self.maxxy = []


    '''前序遍历建树'''

    def bulidTree(self, arrs,p):
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
            arrs.pop(0)
            zindex = int(arrs[0])
            self.index.append(p[zindex])
            arrs.pop(0)
            return
        else:
            self.val = arrs[0]
            arrs.pop(0)
            self.left = BinaryTree()
            self.mid = BinaryTree()
            self.right = BinaryTree()
            self.left.bulidTree(arrs,p)
            self.index.extend(self.left.index)
            self.mid.bulidTree(arrs,p)
            self.index.extend(self.mid.index)
            self.right.bulidTree(arrs,p)
            self.index.extend(self.right.index)
            self.minxy=minxy(self.index).copy()
            self.maxxy=maxxy(self.index).copy()



    '''层序遍历建树'''

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

    '''前序遍历树'''

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
        elif self.minxy[0] <= point[0] <= self.maxxy[0] and self.minxy[1] <= point[1] <= self.maxxy[1]:
            return 1
        else:
            return 0
    def mindist(self,point):
        if self.isinrect(point)==1:
            return 0
        elif self.isinrect(point)==-1:
            return 100000000
        else:
            min1 = line(point,[self.minxy[0],self.minxy[1]],[self.maxxy[0], self.minxy[1]])
            min2 = line(point,[self.minxy[0],self.minxy[1]],[self.minxy[0], self.maxxy[1]])
            min3 = line(point, [self.maxxy[0], self.maxxy[1]],[self.maxxy[0], self.minxy[1]])
            min4 = line(point, [self.maxxy[0], self.maxxy[1]],[self.minxy[0], self.maxxy[1]])
            min5 = ptp(point,[self.minxy[0],self.minxy[1]])
            min6 = ptp(point, [self.minxy[0], self.maxxy[1]])
            min7 = ptp(point, [self.maxxy[0], self.minxy[1]])
            min8 = ptp(point, [self.maxxy[0], self.maxxy[1]])
            return min(min1,min2,min3,min4,min5,min6,min7,min8)
    def minmaxdist(self,point):
        min1 = line(point, [self.minxy[0], self.minxy[1]], [self.maxxy[0], self.minxy[1]])
        min2 = line(point, [self.minxy[0], self.minxy[1]], [self.minxy[0], self.maxxy[1]])
        min3 = line(point, [self.maxxy[0], self.maxxy[1]], [self.maxxy[0], self.minxy[1]])
        min4 = line(point, [self.maxxy[0], self.maxxy[1]], [self.minxy[0], self.maxxy[1]])
        minn=min(min1,min2,min3,min4)
        if min1==minn:
            return max(ptp(point,[self.minxy[0], self.minxy[1]]),ptp(point,[self.maxxy[0], self.minxy[1]]))
        elif min2==minn:
            return max(ptp(point, [self.minxy[0], self.minxy[1]]), ptp(point, [self.minxy[0], self.maxxy[1]]))
        elif min3==minn:
            return max(ptp(point, [self.maxxy[0], self.maxxy[1]]), ptp(point, [self.maxxy[0], self.minxy[1]]))
        elif min4==minn:
            return max(ptp(point, [self.maxxy[0], self.maxxy[1]]), ptp(point, [self.minxy[0], self.maxxy[1]]))

    def knn(self,qx, qy, k):
        qpoint = [qx, qy]
        qunne = [self]
        mindistv = 1000000
        minmaxdistv = 1000000
        dist = 100000
        while len(qunne) != 0:
            node = qunne.pop(0)
            print(node.val)
            if node.left.val=='*':
                dist=min(ptp(qpoint,node.left.index[0]),ptp(qpoint,node.left.index[1]),dist)
                continue
            if node.left.mindist(qpoint) <= minmaxdistv and node.left is not None and node.left.val !='null' and node.left.val !=None and node.left.mindist(qpoint)<dist:
                qunne.append(node.left)
                mindistv=min(node.left.mindist(qpoint),mindistv)
                minmaxdistv=min(node.left.minmaxdist(qpoint),minmaxdistv)
            if node.mid.mindist(qpoint) <= minmaxdistv and node.mid is not None and node.mid.val != 'null' and node.mid.val != None and node.mid.mindist(qpoint)<dist:
                qunne.append(node.mid)
                mindistv = min(node.mid.mindist(qpoint), mindistv)
                minmaxdistv = min(node.mid.minmaxdist(qpoint), minmaxdistv)
            if node.right.mindist(qpoint) <= minmaxdistv and node.right is not None and node.right.val != 'null' and node.right.val != None  and node.right.mindist(qpoint)<dist :
                qunne.append(node.right)
                mindistv = min(node.right.mindist(qpoint), mindistv)
                minmaxdistv = min(node.right.minmaxdist(qpoint), minmaxdistv)
        print(dist)





# def knn(qx,qy,k):
#     point = [[96,94],[164,64],[67,150],[104,190],[190,209],[221,233],[230,307],[200,290],[413,47],[380,95],[566,30],[676,58],[786,104],[750,50],[437,324],[543,267],[470,454],[399,389],[827,394],[753,448],[786,583],[826,513],[957,676],[926,533],[891,785],[757,770],[962,814],[981,773],[595,983],[677,853],[542,892],[476,835],[282,895],[400,950],[185,9],[220,39],[65,570],[100,620],[180,581],[200,600],[70,521],[88,550],[66,380],[160,420],[500,508],[552,562],[806,812],[861,909],]
#     qpoint = [qx,qy]
#     qunne = [root]
#     mindistv=1000000
#     minmaxdistv=1000000
#     dist =100000
#     while len(qunne)!=0:
#         node = qunne.pop()
#         if mindist


if __name__ == '__main__':
    a = BinaryTree()
    point = [[96, 94], [164, 64], [67, 150], [104, 190], [190, 209], [221, 233], [230, 307], [200, 290], [413, 47],
             [380, 95], [566, 30], [676, 58], [786, 104], [750, 50], [437, 324], [543, 267], [470, 454], [399, 389],
             [827, 394], [753, 448], [786, 583], [826, 513], [957, 676], [926, 533], [891, 785], [757, 770], [962, 814],
             [981, 773], [595, 983], [677, 853], [542, 892], [476, 835], [282, 895], [400, 950], [185, 9], [220, 39],
             [65, 570], [100, 620], [180, 581], [200, 600], [70, 521], [88, 550], [66, 380], [160, 420], [500, 508],
             [552, 562], [806, 812], [861, 909], ]
    arrs = ['root','R0', 'R1', 'R2','R3', 'R4','R5', 'R27','R28','null', 'R15', 'R16','R17','R6', 'R7','R8','R12', 'R13','R14','R9', 'R10','R11','R30', 'R31','R32','R33', 'R34','R35','null','null','null','R18', 'R19','R20','R21', 'R22','R23','R24', 'R25','R26']
  #  a.levelBulidTree(arrs)
    arr =[' root ',' R0 ',' R3 ',' R6 ','*','14','15','null','null',' R7 ','*','16','17','null','null',' R8 ','*','44','45','null','null',' R4 ',' R12 ','*','8','9','null','null',' R13 ','*','10','11','null','null',' R14 ','*','12','13','null','null',' R5 ',' R9 ','*','18','19','null','null',' R10 ','*','20','21','null','null',' R11 ','*','22','23','null','null',' R1 ',' R27 ',' R30 ','*','32','33','null','null',' R31 ','*','30','31','null','null',' R32 ','*','28','29','null','null',' R28 ',' R33 ','*','46','47','null','null',' R34 ','*','24','25','null','null',' R35 ','*','26','27','null','null','null',' R2 ',' R15 ',' R18 ','*','2','3','null','null',' R19 ','*','0','1','null','null',' R20 ','*','34','35','null','null',' R16 ',' R21 ','*','42','43','null','null',' R22 ','*','4','5','null','null',' R23 ','*','6','7','null','null',' R17 ',' R24 ','*','36','37','null','null',' R25 ','*','41','40','null','null',' R26 ','*','38','39','null','null']
    a.bulidTree(arr,point)
    a.knn(600,200,1)
    a.preTravel()

