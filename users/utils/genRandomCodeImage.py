#coding:utf-8
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
img = Image.new(mode="RGB",size=(120,30),color=(255,255,255))
draw = ImageDraw.Draw(img,mode="RGB")

# draw.point([10,10],fill="red")# 画点
# draw.point([30,20],fill="black") #画点
#
# draw.line((100,100,100,300),fill="red")
# draw.line((100,100,300,100), fill="red")
#
# draw.arc((120,100,300,300),0,90,fill="red") 画圆
# draw.arc((120,100,300,300),90,180,fill="red")
# draw.arc((120,100,300,300),180,270,fill="red")
# draw.arc((120,100,300,300),270,360,fill="red")

# draw.text([10,20],"python","red") 写文字

#
# font = ImageFont.truetype("kumo.ttf",18) 设置字体文件

# t1 = chr(random.randint(65,90))  生成随机的英文字符
# t2 = chr(random.randint(65,90))
# t3 = chr(random.randint(65,90))
# t4 = chr(random.randint(65,90))
#
# draw.text((50,10),"{}{}{}{}".format(t1,t2,t3,t4),fill="red",font=font) # 写文字
# print(chr(65))


class BigPainter:


    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance


    def __init__(self):
        self.width = 120
        self.height = 30
        self.font = ImageFont.truetype(font="Monaco.ttf",size=28)
        self.img = Image.new(mode="RGB",size=(self.width,self.height),color=(255,255,255))
        self.draw = ImageDraw.Draw(self.img,mode="RGB")
        self.code = []

        self.char_length = 5

    def randChar(self,):
        """生成随机字符"""
        return chr(random.randint(65,90))

    def randColor(self):
        """生成随机颜色"""
        return (random.randint(0,255),random.randint(10, 255),random.randint(64, 255))

    def gen_line(self):
        for i in range(5):  # 画干扰线
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)

            self.draw.line((x1, y1, x2, y2), fill=self.randColor())

    def gen_point(self):
        for i in range(40):  # 画干扰点
            self.draw.point([random.randint(0, self.width), random.randint(0, self.height)])

    def gen_arc(self):
        for i in range(40):  # 画干扰圈
            self.draw.point([random.randint(0, self.width), random.randint(0, self.height)], fill=self.randColor())
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.randColor())

    def draw_picture(self):


        for i in range(5):  # 随机字符
            char = self.randChar()
            self.code.append(char)
            h = random.randint(0, 4)
            self.draw.text([i * self.width / self.char_length, h], char, font=self.font, fill=self.randColor())

        self.gen_line() #干扰线
        self.gen_point()#干扰点
        self.gen_arc()#干扰圈

        img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        return img, "".join(self.code)

    @classmethod
    def Draw(cls):#再次封装
        return cls().draw_picture()

if __name__ == '__main__':
    img,code = BigPainter.Draw()
    print(code)
    # with open("code.png","wb")as f:
    #     img.save(f,format="png")
    from io import BytesIO
    stream = BytesIO()
    img.save(stream, 'png')
    with open("code.png","w+b")as f:
        f.write(stream.getvalue())




