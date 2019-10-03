import numpy as np
import line
import math
class polygon(line.line):
    def __init__(self,canvas_image,line_id,w,h,R,G,B):
        line.line.__init__(self,canvas_image,line_id,w,h,R,G,B)
        self.type=1 # 1 stand for polygon
   
    def get_text(self):
        ret='多边形\n'
        ret+='id 为'+str(self.graphic_id)+'\n'
        ret+= 'RGB is '+ str(self.R) +' '+ str(self.G)+ ' ' + str(self.B)+'\n'
        for i in range(len(self.xvec)):
            ret+='('+str(self.xvec[i])+','+str(self.h-self.yvec[i])+')'
        ret+='\n'
        return ret   
 
    def draw_poly(self,xy_vec,algorithm):
        
        self.xvec=[]
        self.yvec=[]
        self.algorithm=algorithm
        print(xy_vec)
        xy_len = int(len(xy_vec)/2)
        print(xy_len)

        for j in range(xy_len):
            self.xvec.append(int(xy_vec[2*j]))
            self.yvec.append(int(xy_vec[2*j+1]))
        self.draw_poly2()

    def draw_poly2(self):
        for i in range(len(self.xvec)):
            if(i==len(self.xvec)-1):
                self.draw_line(self.xvec[-1],self.yvec[-1],self.xvec[0],self.yvec[0],self.algorithm)
                break
            x1_index=self.xvec[i]
            y1_index=self.yvec[i]
            x2_index=self.xvec[i+1]
            y2_index=self.yvec[i+1]
            self.draw_line(x1_index,y1_index,x2_index,y2_index,self.algorithm)


    def do_rotate(self,x,y,r):
        self.point_vec=[]
        pi=math.pi
        r_dgree=(1-(float(r)/360))*2*pi
        for i in range(len(self.xvec)):
            new_x=x+(self.xvec[i]-x)*math.cos(r_dgree)-(self.yvec[i]-y)*math.sin(r_dgree)
            new_y=y+(self.xvec[i]-x)*math.sin(r_dgree)+(self.yvec[i]-y)*math.cos(r_dgree)
            self.xvec[i]=new_x
            self.yvec[i]=new_y
        print('inside rotate',self.point_vec)
        self.draw_poly2()
        
        
        

    def do_translate(self,dx,dy):
        print('reach translate')
        for i in range(len(self.xvec)):
            self.xvec[i]+=dx
            self.yvec[i]+=dy
        self.point_vec=[]       
        self.draw_poly2()


    def do_scale(self,x,y,scale_rate):
        self.point_vec=[]
        for i in range(len(self.xvec)):
            x_index = self.xvec[i]
            y_index = self.yvec[i]
            x_range = x_index-x
            y_range = y_index-y
            new_x=round(x+scale_rate*(x_range))
            new_y=round(y+scale_rate*(y_range))
            self.xvec[i]=new_x
            self.yvec[i]=new_y
        self.draw_poly2()

        
    


        
    
