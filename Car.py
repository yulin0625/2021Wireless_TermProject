import random

class Car:
    speed = 0.02                 # 0.02km

    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.state = "INIT"   # 是否打電話(CALL or RELEASE)
        self.init_time = random.randint(0,60)   # random delay
        # print("Init time: {} (s)".format(self.init_time))v
        self.call_time = 0      # call 剩餘時間(s)
        self.release_time = 0   # release 剩餘時間(s)

        self.BS1 = -1
        self.BS2 = -1
        self.BS3 = -1
        self.BS4 = -1

    def Go(self):
        # print("%{}, {}".format(round(self.x * 100, 2) / 100, round(self.y * 100, 2) / 100))
        if (round(self.x * 100, 2) / 100 % 2.5 == 0) and (round(self.y * 100, 2) / 100 % 2.5 == 0):
            self.Turn()

        if self.dir == "RIGHT":         # RIGHT
            self.x += self.speed
        elif self.dir == "LEFT":        # LEFT
            self.x -= self.speed
        elif self.dir == "UP":          # UP
            self.y -= self.speed
        else:                           #DOWN
            self.y += self.speed            

    def Turn(self):
        d = random.randint(1, 32)
        if self.dir == "RIGHT":           #RIGHT
            if d <= 16:
                self.dir = "RIGHT" # 前進
            elif d <= 18:
                self.dir = "LEFT"  # 迴轉
            elif d <= 25:
                self.dir = "UP"    # 左轉
            else:
                self.dir = "DOWN"  # 右轉 
        elif self.dir == "LEFT":          #LEFT
            if d <= 16:
                self.dir = "LEFT"  # 前進
            elif d <= 18:
                self.dir = "RIGHT" # 迴轉
            elif d <= 25:
                self.dir = "DOWN"  # 左轉
            else:
                self.dir = "UP"    # 右轉 
        elif self.dir == "UP":              #UP
            if d <= 16:
                self.dir = "UP"    # 前進
            elif d <= 18:
                self.dir = "DOWN"  # 迴轉
            elif d <= 25:
                self.dir = "LEFT"  # 左轉
            else:
                self.dir = "RIGHT" # 右轉      
        else:                             #DOWN
            if d <= 16:
                self.dir = "DOWN"  # 前進
            elif d <= 18:
                self.dir = "UP"    # 迴轉
            elif d <= 25:
                self.dir = "RIGHT" # 左轉
            else:
                self.dir = "LEFT"  # 右轉       