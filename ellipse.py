import numpy as np
import line
import math
class ellipse(line.line):
    def __init__(self,canvas_image,ellipse_id,w,h,R,G,B):
        line.line.__init__(self,canvas_image,ellipse_id,w,h,R,G,B)
        self.type = 2 # 2 stand for elllipse

    def draw_ellipse(self,x,y,rx,ry):
        print(x,y,rx,ry)
        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry
        
        (self.point_vec).append((x,y+ry))
        (self.point_vec).append((x,y-ry))
        (self.point_vec).append((x-rx,y))
        (self.point_vec).append((x+rx,y))

        y_index_high = ry
        x_index_high = rx

        for index_x in range(1,rx):
            if(ry*ry*index_x-rx*rx*y_index_high>0):
                print("reach break")
                break
            
            p= 4*ry*ry*index_x*index_x+rx*rx*(4*y_index_high*y_index_high-4*y_index_high+1-4*ry*ry)
            if(p>0):
                y_index_high-=1

            (self.point_vec).append((index_x+self.x,y_index_high+self.y))
            (self.point_vec).append((self.x-index_x,y_index_high+self.y))
            (self.point_vec).append((self.x-index_x,self.y-y_index_high))
            (self.point_vec).append((index_x+self.x,self.y-y_index_high))

        for index_y in range(1,ry):
            if(ry*ry*x_index_high-rx*rx*index_y<=0):
                print("reach break")
                break
            
            p= 4*rx*rx*index_y*index_y+ry*ry*(4*x_index_high*x_index_high-4*x_index_high+1-4*rx*rx)
            if(p>0):
                x_index_high-=1
            (self.point_vec).append((x_index_high+self.x,index_y+self.y))
            (self.point_vec).append((self.x-x_index_high,index_y+self.y))
            (self.point_vec).append((self.x-x_index_high,self.y-index_y))
            (self.point_vec).append((x_index_high+self.x,self.y-index_y))

    def do_translate(self,dx,dy):
        self.x+=dx
        self.y+=dy
        self.draw_ellipse(self.x,self.y,self.rx,self.ry)

    def get_text(self):
        ret='椭圆\n'
        ret+='id 为'+str(self.graphic_id)+'\n'
        ret+= 'RGB is '+ str(self.R) +' '+ str(self.G)+ ' ' + str(self.B)+'\n'
        ret+='('+str(self.x)+','+str(self.h-self.y)+')'+'  rx is '+str(self.rx)+' ry is '+str(self.ry)
        ret+='\n'
        return ret   
  
    def do_rotate(self,x,y,r):
        print("椭圆不支持旋转\n")
        pass                

    
    def do_scale(self,x,y,scale_rate):
        self.point_vec=[]
        x_range=self.x-x
        y_range=self.y-y
        y_range2=self.y+self.ry-y
        x_range2=self.x+self.rx-x
        new_y2= round(self.y+self.ry+scale_rate*(y_range2))
        new_x2= round(self.x+self.rx+scale_rate*(x_range2))
        new_x= round(x+scale_rate*(x_range))
        new_y= round(y+scale_rate*(y_range))
        self.x=new_x
        self.y=new_y
        self.rx=new_x2-new_x
        self.ry=new_y2-new_y
        self.draw_ellipse(self,self.x,self.y,self.rx,self.ry)
        
        
