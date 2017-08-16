import csv
from numpy import *
import matplotlib.pyplot as plt
#listx is the list of x value
#listy is the list of y value
#max_x is used for the scale of x axis
#max_y is used for the scale of y axis
def read():
    listx = []
    listy = []
    max_x=0
    max_y=0
    with open('1.csv') as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for row in f_csv:
            tmpx=int(row[0])
            tmpy=int(row[1])
            listx.append(tmpx)
            listy.append(tmpy)
            if abs(tmpx)>max_x:
                max_x=abs(tmpx)
            if abs(tmpy)>max_y:
                max_y=abs(tmpy)
    print max_x
    print max_y
    return listx,listy,max_x,max_y

def draw(listx,listy):
    #offset is used to margin the x,y axis
    offset=2
    fig = plt.figure()
    fig.suptitle('plot')
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.scatter(listx, listy)
    plt.xlim((-1*(max_x+offset), max_x+offset))
    plt.ylim((-1*(max_y+offset), max_y+offset))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

listx,listy,max_x,max_y=read()
draw(listx,listy)