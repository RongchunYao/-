import numpy as np
class BmpFileHeader:
    def __init__(self):
        self.bfType= b'\x42\x4d'
        self.bfSize= b'\x00\x00\x00\x00' #need to modify
        self.bfReserved1= b'\x00\x00'
        self.bfReserved2= b'\x00\x00'
        self.bfOffBits=b'\x36\x00\x00\x00' 

class BmpStructHeader:
    def __init__(self):
        self.biSize=b'\x28\x00\x00\x00' 
        self.biWidth=b'\x00\x00\x00\x00'  #need to modify
        self.biHeight=b'\x00\x00\x00\x00'   #need to modify 
        self.biPlanes=b'\x01\x00'    
        self.biBitCount=b'\x18\x00'
        self.biCompression=b'\x00\x00\x00\x00'
        self.biSizeImage=b'\x00\x00\x00\x00'     # since we use bi_rgb , it is 0
        self.biXPelsPerMeter=b'\x00\x00\x00\x00'
        self.biYPelsPerMeter=b'\x00\x00\x00\x00'
        self.biClrUsed = b'\x00\x00\x00\x00'
        self.biClrImportant=b'\x00\x00\x00\x00'

class Bmp(BmpFileHeader,BmpStructHeader):
    def __init__(self):
        BmpFileHeader.__init__(self)
        BmpStructHeader.__init__(self)
        self.canvas_width=800
        self.canvas_height=800 
        self.canvas_image=np.zeros((self.canvas_width,self.canvas_height,3),dtype=int)
        for i in range(0,self.canvas_width):
            for j in range(0,self.canvas_height):
                self.canvas_image[i][j][0]=255
                self.canvas_image[i][j][1]=255
                self.canvas_image[i][j][2]=255



        self.file_name="output.bmp"

    def modify_name(self,filename):
        self.file_name=filename
    
    def reset_color(self):
        for i in range(0,self.canvas_height):
            for j in range(0,self.canvas_width):
                self.canvas_image[i][j][0]=255
                self.canvas_image[i][j][1]=255
                self.canvas_image[i][j][2]=255
        
    def generate(self):
        self.biWidth=self.canvas_width.to_bytes(4,"little")
        self.biHeight=self.canvas_height.to_bytes(4,"little")
        size = 14+40+self.canvas_width*self.canvas_height*3
        self.bfSize=size.to_bytes(4,'little')
        with open(self.file_name,"wb+") as f:
            f.write(self.bfType)
            f.write(self.bfSize)
            f.write(self.bfReserved1)
            f.write(self.bfReserved2)
            f.write(self.bfOffBits)
            f.write(self.biSize)
            f.write(self.biWidth)
            f.write(self.biHeight)
            f.write(self.biPlanes)
            f.write(self.biBitCount)
            f.write(self.biCompression)
            f.write(self.biSizeImage)
            f.write(self.biXPelsPerMeter)
            f.write(self.biYPelsPerMeter)
            f.write(self.biClrUsed)
            f.write(self.biClrImportant)
            # the order is bgr
            for i in range(self.canvas_height):
                for j in range(self.canvas_width):
                    g=int(self.canvas_image[i][j][1]).to_bytes(1,"little")
                    b=int(self.canvas_image[i][j][2]).to_bytes(1,"little")
                    r=int(self.canvas_image[i][j][0]).to_bytes(1,"little")
                    
                    f.write(b+g+r)
        
