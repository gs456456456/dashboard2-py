def myfunc(num):
    #132
    result_list = []
    for x,y in enumerate(num):
        for z in range(len(num)):
            for a in range(len(num)):
                 #m>n
                if num[x]<num[x+z] and num[x+z]>num[x+a] and z<a and z>0 and x+z<len(num) and x+a<len(num):
                    result_list.append([num[x],num[x+z],num[x+a]])
    return result_list

class ball(object):
    def __init__(self,height,times):
        self.height = height
        self.times = times
        self.totalheight = height
    def fall(self):
        while self.times>0:
            self.totalheight += self.height/2
            self.height = self.height/2
            self.times-=1

a = ball(10,2)
a.fall()
print(a.height,a.totalheight)

if __name__ == '__main__':
    pass
    # print(myfunc([-1,3,2,4,6,5]))