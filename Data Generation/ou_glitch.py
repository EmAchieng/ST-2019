import cv2
import random
import matplotlib.pyplot as plt
import numpy as np

def dotted_lines(picture):
    pic = picture.copy()
    height = pic.shape[0]
    width = pic.shape[1]
    angle = random.randint(15,345)
    number_of_lines = random.randint(15,35)

    ox = random.randint(int(0.2*width), int(0.8*width))
    oy = random.randint(int(0.2*height),int(0.8*height))

    for i in np.arange(number_of_lines):
        x = ox + random.randint(-int(0.2*width), int(0.2*width))
        y = oy + random.randint(-int(0.2*height),int(0.2*height))
        theta = angle + random.randint(-20,20)
        tangent = np.tan(theta/180*np.pi)
        hstep = random.choice([-4,4,-5, 5,-3,3,-6,6])
        vstep = hstep*tangent
        for j in np.arange(random.randint(20,50)):
            px = int(x + j*hstep)
            py = int(y + j*vstep)
            if px >= 0 and px <= width-1 and py >= 0 and py <= height-1:
                u = random.uniform(0, 1)
                if u > 0.9:
                    nx = max(px-1, 0)
                    pic[py,nx] = [0,0,0]
                if u < 0.1:
                    ny = max(py-1, 0)
                    pic[ny,px] = [0,0,0]
                pic[py,px] = [0,0,0]
            else:
                break   
    return pic    

def square_patches(picture):
    pic = picture.copy()/255
    height = pic.shape[0]
    width = pic.shape[1]
    number_of_patches = random.randint(2,10)

    first_y = -1
    first_x = -1

    for i in range(number_of_patches):
        size = random.randint(2,5)
        if first_y < 0:
            first_y = random.randint(int(height*0.2), int(height*0.8))
            first_x = random.randint(int(width*0.2), int(width*0.8))
            color = [random.uniform(0, 0.4), random.uniform(0, 0.5),random.uniform(0.6, 0.9)]
            pic[first_y:(first_y+size), first_x:(first_x+size)] = color
        else:
            y = first_y +  random.randint(-int(height*0.1), int(height*0.1))
            x = first_x +  random.randint(-int(width*0.1), int(width*0.1))
            color = [random.uniform(0, 0.4), random.uniform(0, 0.5),random.uniform(0.6, 0.9)]
            pic[y:(y+size), x:(x+size)] = color

    return pic

def parallel_lines(picture):
    pic = picture.copy()/255
    height = pic.shape[0]
    width = pic.shape[1]
    number_of_lines = np.random.randint(60,100)
    theta = np.random.randint(10,35)
    angle = np.tan(theta/180*np.pi)
    u = np.random.uniform(0,1)
    sign = random.choice([1,-1])

    while number_of_lines > 0:
        x1 = random.randint(int(0.3*width),int(0.6*width))
        y1 = random.randint(int(0.2*height),int(0.8*height))
        if u < 0.5:
            x2 = 0
            y2 = y1 + sign*int(x1*angle)
            if y2 >= height or y2 < 0:
                continue
        else:
            x2 = width-1
            y2 = y1 + sign*int((width-x1-1)*angle)
            if y2 >= height or y2 < 0:
                continue     
        lineThickness = random.randint(1,3)
        color = pic[y1,x1]
        cv2.line(pic, (x1,y1), (x2,y2), color, lineThickness)
        number_of_lines -= 1

    return pic 
