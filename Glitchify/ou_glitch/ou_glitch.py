'''
	The input is a python [Height * Width * 3] array, which is a picture to add glitches.
	Notice that the input value should range from 0 to 255.
	The output is a python [Height * Width * 3] array, which is a picture with glitch added.
'''

import cv2
import numpy.random as random
import matplotlib.pyplot as plt
import numpy as np

def check_val(value):
	if value > 255:
		value = 255
	if value < 0:
		value = 0
	return value

def dotted_lines(picture, lo = 15, hi = 35):
	pic = picture.copy()
	height = pic.shape[0]
	width = pic.shape[1]
	angle = random.randint(15,345)
	number_of_lines = random.randint(lo,hi+1)

	ox = random.randint(int(0.2*width), int(0.8*width))
	oy = random.randint(int(0.2*height),int(0.8*height))

	r = random.randint(0,256)
	g = random.randint(0,256)
	b = random.randint(0,256)

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
					pic[py,nx] = [r,g,b]
				if u < 0.1:
					ny = max(py-1, 0)
					pic[ny,px] = [r,g,b]
				pic[py,px] = [r,g,b]
			else:
				break   
	return pic   

def dotted_lines_radial(picture, lo = 30, hi = 60):
    pic = picture.copy()
    height = pic.shape[0]
    width = pic.shape[1]
   # angle = random.randint(15,345)
    number_of_lines = random.randint(lo,hi)

    x = random.randint(int(0.2*width), int(0.8*width))
    y = random.randint(int(0.2*height),int(0.8*height))

    r = np.random.randint(0,256)
    g = np.random.randint(0,256)
    b = np.random.randint(0,256)

    angle_step = np.floor(360 / number_of_lines)
    initial_angle = random.randint(-10,10)


    for i in np.arange(number_of_lines):
        theta = initial_angle + angle_step * i + random.randint(-5,5)
        radian = theta/180*np.pi
        if np.cos(radian) >= 0:
            hstep = random.choice([4,5,3,6])
        else:
            hstep = random.choice([4,5,3,6]) * -1
        vstep = hstep*np.tan(radian)
        for j in np.arange(random.randint(20,50)):
            px = int(x + j*hstep)
            py = int(y + j*vstep)
            if px >= 0 and px <= width-1 and py >= 0 and py <= height-1:
                u = random.uniform(0, 1)
                if u > 0.9:
                    nx = max(px-1, 0)
                    pic[py,nx] = [r,g,b]
                if u < 0.1:
                    ny = max(py-1, 0)
                    pic[ny,px] = [r,g,b]
                pic[py,px] = [r,g,b]
            else:
                break   
    return pic


def square_patches(picture, lo = 2, hi = 15):
	pic = picture.copy()
	height = pic.shape[0]
	width = pic.shape[1]
	number_of_patches = random.randint(lo,hi+1)

	first_y = -1
	first_x = -1

	r = int(random.uniform(0, 1)*255)
	g = int(random.uniform(0, 1)*255)
	b = int(random.uniform(0, 1)*255)

	for i in range(number_of_patches):
		size = random.randint(2,5)
		red = check_val(r + random.randint(-30,30))
		green = check_val(g + random.randint(-30,30))
		blue = check_val(b + random.randint(-30,30))
		color = [blue, green, red]
		if first_y < 0:
			first_y = random.randint(int(height*0.2), int(height*0.8))
			first_x = random.randint(int(width*0.2), int(width*0.8))
			pic[first_y:(first_y+size), first_x:(first_x+size)] = color
		else:
			y = first_y +  random.randint(-int(height*0.1), int(height*0.1))
			x = first_x +  random.randint(-int(width*0.1), int(width*0.1))
			pic[y:(y+size), x:(x+size)] = color

	return pic

def parallel_lines(picture, lo = 60, hi = 100):
	pic = picture.copy()
	height = pic.shape[0]
	width = pic.shape[1]
	number_of_lines = np.random.randint(lo,hi+1)
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
		colors = pic[y1,x1].astype(float)
		cv2.line(pic, (x1,y1), (x2,y2), colors, lineThickness)
		number_of_lines -= 1

	return pic 