import gc
import numpy as np
import bmp
import line
import polygon
import ellipse
import curve
import math

class canvas(bmp.Bmp):
    def __init__(self):
         
        bmp.Bmp.__init__(self)
        self.R=0
        self.G=0
        self.B=0
        self.graphics=[]

    def reset_canvas(self,res_cmd):
    
        w = int(res_cmd[0])
        h = int(res_cmd[1])
        self.canvas_image = []
        self.graphics=[]
        gc.collect()
        self.canvas_width=w
        self.canvas_height=h
        self.canvas_image = np.zeros((h,w,3),dtype=int)
        self.reset_color()
        gc.collect()
        for i in self.graphics:
            i.canvas_image=self.canvas_image
            i.w=w
            i.h=h

    def refresh(self):
        self.canvas_image = np.zeros((self.canvas_height,self.canvas_width,3),dtype=int)
        self.reset_color()
        gc.collect()
        for i in self.graphics:
            i.canvas_image=self.canvas_image
    
    def set_color(self,res_cmd):
        self.R=int(res_cmd[0])
        self.G=int(res_cmd[1])
        self.B=int(res_cmd[2])

    def save_canvas(self,res_cmd):
        name=res_cmd[0]
        self.modify_name(name)
        
        self.refresh()
        for i in self.graphics:
            i.paint_to_canvas()
        self.generate()

    def draw_line(self,res_cmd):
        line_id=int(res_cmd[0])
        x1=int(res_cmd[1])
        y1=int(res_cmd[2])
        x2=int(res_cmd[3])
        y2=int(res_cmd[4])
        algorithm=res_cmd[5]
        new_line = line.line(self.canvas_image,line_id,self.canvas_width,self.canvas_height,self.R,self.G,self.B)
        new_line.draw_line(x1,y1,x2,y2,algorithm)
        self.graphics.append(new_line)

    def draw_poly(self,res_cmd):
        poly_id=int(res_cmd[0])
        n=int(res_cmd[1])
        algorithm=res_cmd[2]
        xy_vec=res_cmd[3:]
        new_poly= polygon.polygon(self.canvas_image,poly_id,self.canvas_width,self.canvas_height,self.R,self.G,self.B)
        new_poly.draw_poly(xy_vec,algorithm)
        self.graphics.append(new_poly)
    
    def draw_curve(self,res_cmd):
        curve_id=int(res_cmd[0])
        curve_id=int(res_cmd[0])
        n=int(res_cmd[1])
        algorithm=res_cmd[2]
        xy_vec=res_cmd[3:]
        new_curve= curve.curve(self.canvas_image,curve_id,self.canvas_width,self.canvas_height,self.R,self.G,self.B)  
        new_curve.draw_curve(xy_vec,algorithm)
        self.graphics.append(new_curve)

    def draw_ellipse(self,res_cmd):
        ellipse_id = int(res_cmd[0])
        x = int(res_cmd[1])
        y = int(res_cmd[2])
        rx = int(res_cmd[3])
        ry = int(res_cmd[4])
        new_ellipse = ellipse.ellipse(self.canvas_image,ellipse_id,self.canvas_width,self.canvas_height,self.R,self.G,self.B)       
        new_ellipse.draw_ellipse(x,y,rx,ry)
        self.graphics.append(new_ellipse)        
    
    def translate(self,res_cmd):
        graphic_id = int(res_cmd[0])
        dx=int(res_cmd[1])
        dy=int(res_cmd[2])
        for i in self.graphics:
            if i.graphic_id == graphic_id:
                i.do_translate(dx,dy)

    def rotate(self,res_cmd):
        
        graphic_id=int(res_cmd[0])
        x=int(res_cmd[1])
        y=int(res_cmd[2])
        degree=float(res_cmd[3])
        for i in self.graphics:
            if i.graphic_id == graphic_id:
                i.do_rotate(x,y,degree)

    def scale(self,res_cmd):
        graphic_id=int(res_cmd[0])
        x=int(res_cmd[1])
        y=int(res_cmd[2])
        scale_rate=float(res_cmd[3])
        for i in self.graphics:
            if i.graphic_id == graphic_id:
                i.do_scale(x,y,scale_rate)

    def clip(self,res_cmd):
        graphic_id=int(res_cmd[0])
        x1=int(float(res_cmd[1]))
        y1=int(float(res_cmd[2]))
        x2=int(float(res_cmd[3]))
        y2=int(float(res_cmd[4]))
        algorithm=res_cmd[5]
        for i in range(len(self.graphics)):
            if self.graphics[i].graphic_id == graphic_id:
                retval=self.graphics[i].do_clip(x1,y1,x2,y2,algorithm)
                if(retval==False):
                    del self.graphics[i]

    def execute_cmd(self,cmd_type,res_list):
        if(cmd_type=="resetCanvas"):
            self.reset_canvas(res_list)
        elif(cmd_type=="saveCanvas"):
            self.save_canvas(res_list)
        elif(cmd_type=="setColor"):
            self.set_color(res_list)
        elif(cmd_type=="drawLine"):
            self.draw_line(res_list)
        elif(cmd_type=="drawPolygon"):
            self.draw_poly(res_list)
        elif(cmd_type=="drawEllipse"):
            self.draw_ellipse(res_list)
        elif(cmd_type=="drawCurve"):
            self.draw_curve(res_list)
        elif(cmd_type=="translate"):
            self.translate(res_list)
        elif(cmd_type=="rotate"):
            self.rotate(res_list)
        elif(cmd_type=="scale"):
            self.scale(res_list)
        elif(cmd_type=="clip"):
            self.clip(res_list)
    
