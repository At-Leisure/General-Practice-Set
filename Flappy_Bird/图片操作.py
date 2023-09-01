from PIL import Image
import imgsPath

#改变大小-进行压缩或反压缩
def resize_picture(path,rate):
    img = Image.open(path)
    width = img.size[0]   # 获取宽度
    height = img.size[1]   # 获取高度
    img = img.resize((int(width*rate),int(height*rate)), Image.ANTIALIAS)
    img.save(path.split('\\')[-1])

#改变透明度
def change_alpha(path):
    img = Image.open(path)
    img = img.convert('RGBA') # 修改颜色通道为RGBA
    x, y = img.size # 获得长和宽

    # 设置每个像素点颜色的透明度
    for i in range(x):
        for k in range(y):
            color = img.getpixel((i, k))
            color = color[:-1] + (100, )
            img.putpixel((i, k), color)
    img.save(path.split('\\')[-1])

img = Image.open(imgsPath.score[1])
width = img.size[0]   # 获取宽度
height = img.size[1]   # 获取高度
img = img.resize((25,35), Image.ANTIALIAS)
img.save("1.png")