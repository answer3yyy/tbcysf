#coding:utf-8
#from PIL import Image
#pil_im = Image.open('7.jpg')
#print pil_im

from PIL import Image
from pylab import *

# 读取图像到数组中
im = array(Image.open('7.jpg').convert('L'))
print im
# 新建一个图像
figure()
# 不使用颜色信息
gray()
# 在原点的左上角显示轮廓图像
a = contour(im, origin='image')
print a
axis('equal')
axis('off')

figure()
print im.flatten()
hist(im.flatten(),128)
show()