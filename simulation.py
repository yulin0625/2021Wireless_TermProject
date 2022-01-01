import numpy as np
import cv2
import time
import random
import math
from Car import Car
from BS import BS

#常數定義
mapsize = 500
width = int(mapsize / 10)
blockSize = 2.5             # 地圖上一格為實際的2.5km
Pt = 120                    # 基地台發送功率(dB)
Pmin = 20                   # Algo 1
Entropy = 25                # 閾值E=25dB

BS_list = []
CarInMap = []
CarOUTMAP = []
CarInCall = 0
t = 0                       # 計時器
handoff_1 = 0
handoff_2 = 0
handoff_3 = 0
handoff_4 = 0


def KmToPixel(km):
    return int(mapsize / 25 * km)

def GetPr(Xc, Yc, Xb, Yb, freq):
    d = math.sqrt(pow(abs(Xc - Xb), 2) + pow(abs(Yc - Yb), 2))
    Pl = 32.45 + 20 * math.log10(freq) + 20 * math.log10(d)
    global Pt
    if Pt - Pl > 0:
        Pr = Pt - Pl
    else:
        Pr = 0
    return Pr

def checkHandoff_1():
    for car in CarInMap:
        if car.state == "CALL":
            isHandoff = 0
            if car.BS1 != -1:
                first = 0
                Pr = GetPr(car.x, car.y, BS_list[car.BS1].x, BS_list[car.BS1].y, BS_list[car.BS1].freq)
            else:
                first = 1
                Pr = 0
            if Pr < Pmin:
                max = Pr
                for i in range(len(BS_list)):
                    Pr_new = GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)
                    if Pr_new > max:
                        max = Pr_new
                        car.BS1 = i
                        isHandoff = 1
                if isHandoff == 1:
                    if first == 0:
                        global handoff_1
                        handoff_1 += 1
                        # print("time {}, algo1 handoff: {}".format(t, car.BS1))
                        # for i in range(len(BS_list)):
                        #     print("BS{}: {}".format(i, GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)) )
                    # else:
                        # print("algo1: first connect to BS{}".format(car.BS1))
                        # for i in range(len(BS_list)):
                            # print("BS{}: {}".format(i, GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)) )

def checkHandoff_2():           # Best_effort
    for car in CarInMap:
        if car.state == "CALL":
            isHandoff = 0
            if car.BS2 != -1:
                first = 0
                Pr = GetPr(car.x, car.y, BS_list[car.BS2].x, BS_list[car.BS2].y, BS_list[car.BS2].freq)
            else:
                first = 1
                Pr = 0
            max = Pr
            for i in range(len(BS_list)):
                Pr_new = GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)
                if Pr_new > max:
                    max = Pr_new
                    car.BS2 = i
                    isHandoff = 1
            if isHandoff == 1:
                if first == 0:
                    global handoff_2
                    handoff_2 += 1
                    # print("time {}, algo2 handoff: {}".format(t, car.BS2))
                    # for i in range(len(BS_list)):
                    #     print("BS{}: {}".format(i, GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)) )
                # else:
                #     print("algo2: first connect to BS{}".format(car.BS2))
                #     for i in range(len(BS_list)):
                #         print("BS{}: {}".format(i, GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)) )

def checkHandoff_3():
    for car in CarInMap:
        if car.state == "CALL":
            isHandoff = 0
            if car.BS3 != -1:
                first = 0
                Pr = GetPr(car.x, car.y, BS_list[car.BS3].x, BS_list[car.BS3].y, BS_list[car.BS3].freq)
            else:
                first = 1
                Pr = 0
            max = Pr
            for i in range(len(BS_list)):
                Pr_new = GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)
                if Pr_new > max and (Pr_new - Pr) > Entropy :
                    max = Pr_new
                    car.BS3 = i
                    isHandoff = 1
            if isHandoff == 1:
                if first == 0:
                    global handoff_3
                    handoff_3 += 1
                    # print("time {}, algo2 handoff: {}".format(t, car.BS3))
                    # for i in range(len(BS_list)):
                    #     print("BS{}: {}".format(i, GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)) )
                # else:
                #     print("algo2: first connect to BS{}".format(car.BS3))
                #     for i in range(len(BS_list)):
                #         print("BS{}: {}".format(i, GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)) )
            
def checkHandoff_4():   # Minimum + Entropy
    for car in CarInMap:
        if car.state == "CALL":
            isHandoff = 0
            if car.BS4 != -1:
                first = 0
                Pr = GetPr(car.x, car.y, BS_list[car.BS4].x, BS_list[car.BS4].y, BS_list[car.BS4].freq)
            else:
                first = 1
                Pr = 0
            if Pr < Pmin:
                max = Pr
                for i in range(len(BS_list)):
                    Pr_new = GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)
                    if Pr_new > max and (Pr_new - Pr) > 5:
                        max = Pr_new
                        car.BS4 = i
                        isHandoff = 1
                if isHandoff == 1:
                    if first == 0:
                        global handoff_4
                        handoff_4 += 1
                        # print("time {}, algo4 handoff: {}".format(t, car.BS4))
                        # for i in range(len(BS_list)):
                        #     print("BS{}: {}".format(i, GetPr(car.x, car.y, BS_list[i].x, BS_list[i].y, BS_list[i].freq)) )
def AddOneCar(x, y, dir):
    car = Car(x, y, dir)
    CarInMap.append(car)

def CreateCar():
    # 上、下
    # print(np.random.poisson(1/12,1))

    for i in range(1,10):
        p1 = random.random()
        if p1 <= np.random.poisson(1/12,1):
            AddOneCar(i*2.5, 0, "DOWN")
        p2 = random.random()
        if p2 <= np.random.poisson(1/12,1):
            AddOneCar(i*2.5, 25, "UP")
    # 左、右
    for j in range(1,10):
        p1 = random.random()
        if p1 <= np.random.poisson(1/12,1):
            AddOneCar(0, j*2.5, "RIGHT")
        p2 = random.random()
        if p2 <= np.random.poisson(1/12,1):
            AddOneCar(25, j*2.5, "LEFT")    

def MoveCar():
    i = 0
    while i < len(CarInMap):    # 有些car會被pop掉，所以要用while
        if(CarInMap[i].x < 0 or CarInMap[i].x > 25 or CarInMap[i].y < 0 or CarInMap[i].y > 25):
                CarOUTMAP.append(CarInMap.pop(i))
        else:
            CarInMap[i].Go()
            i += 1  

def Printmap():
    global t
    # 建立一張 512x512 的 RGB 圖片（白色）
    img = np.full((mapsize + 100, mapsize, 3), 255, np.uint8)
    # print line
    for i in range(10):
        d = (i + 1) * width
        cv2.line(img, (0, d), (mapsize, d), (190, 190, 190), 1)
        cv2.line(img, (d, 0), (d, mapsize), (190, 190, 190), 1)
    # print BS
    for bs in BS_list:
        cv2.circle(img, (KmToPixel(bs.x), KmToPixel(bs.y)), 1, (255, 0, 0), 2) # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
    # print car
    for car in CarInMap:
        cv2.circle(img, ( KmToPixel(car.x), KmToPixel(car.y)), 1, (0, 0, 255), 1)
    # print text
    t_info = "Time: {}(s)".format(t)
    cv2.putText(img, t_info, (10, 520), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 0, cv2.LINE_AA)
    bs_info = "BS in map: {}".format(len(BS_list))
    cv2.putText(img, bs_info, (10, 540), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 0, cv2.LINE_AA)
    # car info
    car_info = "Car in map: {}".format(len(CarInMap))
    cv2.putText(img, car_info, (10, 560), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 0, cv2.LINE_AA)
    call_info = "Car in call: {}".format(CarInCall)
    cv2.putText(img, call_info, (10, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 0, cv2.LINE_AA)
    # handoff info
    h1_info = "Minimum: {}".format(handoff_1)
    cv2.putText(img, h1_info, (200, 520), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 0, cv2.LINE_AA)
    h2_info = "Best effort: {}".format(handoff_2)
    cv2.putText(img, h2_info, (200, 540), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 0, cv2.LINE_AA)
    h3_info = "Entropy: {}".format(handoff_3)
    cv2.putText(img, h3_info, (200, 560), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 0, cv2.LINE_AA)
    h4_info = "My Algo: {}".format(handoff_4)
    cv2.putText(img, h4_info, (200, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 0, cv2.LINE_AA)
    
    cv2.imshow("map", img)
    cv2.waitKey(1)
    time.sleep(0.001)
    t = t + 1

def CheckCall():
    for car in CarInMap:
        if car.state == "CALL":
            if car.call_time == 0:          # reset status
                car.BS1 = -1
                car.BS2 = -1
                car.BS3 = -1
                car.BS4 = -1
                car.release_time = int(random.gauss(1620, 10))       # mean = 27 min = 1620 sec
                car.state = "RELEASE"
                # print("Release {} sec".format(car.release_time))
            else:       
                car.call_time -= 1

        elif car.state == "RELEASE":
            if car.release_time == 0:
                car.call_time = int(random.gauss(180, 1))       # mean = 27 min = 1620 sec
                car.state = "CALL"
                # print("Call {} sec".format(car.call_time))
            else:
                car.release_time -= 1
        else:
            if random.randint(0, 1) == 0:
                if random.randint(0, 1) == 1:                       # CALL
                    car.call_time = int(random.gauss(180, 1))       # mean = 27 min = 1620 sec
                    car.state = "CALL"
                    # print("Call {} sec".format(car.call_time))
                else:                                               # RELEASE
                    car.release_time = int(random.gauss(1620, 10))  # mean = 27 min = 1620 sec
                    car.state = "RELEASE"
                    # print("Release {} sec".format(car.release_time))
            else:
                car.init_time -= 1
    global CarInCall
    CarInCall = 0
    for car in CarInMap:
        if car.state == "CALL":
            CarInCall +=1

def main():
    #建立基地台
    for i in range(10):
        for j in range(10):
            p = random.random()
            if p >= 0.9:
                dx = j * blockSize + int(blockSize/2)
                dy = i * blockSize + int(blockSize/2)

                dir = random.randint(1, 4)
                if dir == 1:
                    dy -= 0.1
                elif dir == 2:
                    dy += 0.1
                elif dir == 3:
                    dx -= 0.1
                else:
                    dx += 0.1
                # set frequency   
                f = random.randint(1,10)
                freq = f * 100 # MHZ
                bs = BS(dx, dy, freq)
                global BS_list
                BS_list.append(bs)
    # print BS info and location
    print("number of BS:{}".format(len(BS_list)))
    i = 1
    for i in range(len(BS_list)):
        bs = BS_list[i]
        print("BS{}: ({:.2f}, {:.2f}), Frequency:{:d}".format(i+1, bs.x, bs.y, bs.freq))

    while 1:
        CreateCar()
        MoveCar()
        CheckCall()
        checkHandoff_1()
        checkHandoff_2()
        checkHandoff_3()
        checkHandoff_4()
        Printmap()
        
if __name__ == '__main__':
    main()    