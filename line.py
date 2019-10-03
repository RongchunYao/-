import numpy as np
import math
class line:
    def __init__(self,canvas_image,line_id,w,h,R,G,B):
        self.x1=0
        self.y1=0
        self.x2=0
        self.y2=0
        self.w=w
        self.h=h
        self.R=R
        self.G=G
        self.B=B
        self.algorithm='Bresenham'
        self.type = 0 # 0 stand for line
        #print(self.R,self.G,self.B)
        self.graphic_id=line_id
        self.canvas_image=canvas_image
        #self.canvas_red=canvas_red
        #self.canvas_green=canvas_green
        #self.canvas_blue=canvas_blue
        #self.point_vec = np.zeros((w,h),dtype=int)
        self.point_vec=[]

    def get_text(self):
        ret='直线\n'
        ret+='id 为'+str(self.graphic_id)+'\n'
        ret+= 'RGB is '+ str(self.R) +' '+ str(self.G)+ ' ' + str(self.B)+'\n'
        ret +='('+str(self.x1)+','+str(self.h-self.y1)+')'
        ret +='('+str(self.x2)+','+str(self.h-self.y2)+')'
        ret+='\n'
        return ret

    def draw_line(self,x1,y1,x2,y2,algorithm):
        print(x1,y1,x2,y2)
        self.x1=round(x1)
        self.x2=round(x2)
        self.y1=round(y1)
        self.y2=round(y2)
        x1=round(x1)
        x2=round(x2)
        y1=round(y1)
        y2=round(y2)
        self.point_vec.append((x1,y1))
        self.point_vec.append((x2,y2))
        self.algorithm=algorithm
        #print(x1,y1,x2,y2)
        if(x1==x2):
            start_y=y1
            end_y=y2
            self.step=1 if start_y<end_y else -1
            for index_y in range(start_y,end_y,self.step):
                #self.point_vec[x1][index_y]=1
                self.point_vec.append((x1,index_y))
            return
        
        if(y1==y2):
            start_x=x1
            end_x=x2
            self.step=1 if start_x<end_x else -1
            for index_x in range(start_x,end_x,self.step):
                #self.point_vec[index_x][y1]=1
                self.point_vec.append((index_x,y1))
            return
        if(algorithm=="DDA"):
            self.draw_DDA(x1,y1,x2,y2)
        elif(algorithm=="Bresenham"):
            self.draw_Bresenham(x1,y1,x2,y2)

    def draw_DDA(self,x1,y1,x2,y2):
        print(x1,y1,x2,y2)
        self.rate=((float)(y2)-(float)(y1))/((float)(x2)-(float)(x1))
        self.re_rate=1.0/self.rate
        if(-1.0<self.rate and self.rate<1.0):  
            start_x = x1
            end_x=x2
            y_val=float(y1)
            self.step=1 if start_x<end_x else -1
            for index_x in range(start_x,end_x,self.step):
                #print(self.step)
                #self.point_vec[index_x][round(y_val)]=1
                self.point_vec.append((index_x,round(y_val)))
                y_val+=self.rate*self.step
            
        else:
            start_y=y1
            end_y=y2
            x_val=float(x1)
            self.step=1 if start_y<end_y else -1
            for index_y in range(start_y,end_y,self.step):
                #self.point_vec[round(x_val)][index_y]=1
                self.point_vec.append((round(x_val),index_y))
                x_val+=self.re_rate*self.step
        
            
    
    def draw_Bresenham(self,x1,y1,x2,y2):
        start_x=x1
        end_x=x2
        tmp_y=y1
        end_y=y2
        start_y=y1
        start_x=x1
        if(abs(y2-y1)<abs(x2-x1)):           
            if(y2<y1):
                start_x=x2
                end_x=x1
                tmp_y=y2
                end_y=y1
                start_y=y2
            self.step=-1 if start_x>end_x else 1
            for index_x in range(start_x,end_x,self.step):
                if((end_x-start_x)*(2*tmp_y+1-2*start_y)<2*(end_y-start_y)*(index_x-start_x)):
                    if(end_x>start_x):
                        tmp_y+=1
                else:
                    if(end_x<start_x):
                        tmp_y+=1
                #self.point_vec[index_x][tmp_y]=1
                self.point_vec.append((index_x,tmp_y))
        else:
            start_y=y1
            end_y=y2
            tmp_x=x1
            start_x=x1
            end_x=x2
            if(x2<x1):
                start_y=y2
                end_y=y1
                tmp_x=x2
                end_x=x1
                start_x=x2
            self.step=-1 if start_y>end_y else 1
            for index_y in range(start_y,end_y,self.step):
                if((end_y-start_y)*(2*tmp_x+1-2*start_x)<2*(end_x-start_x)*(index_y-start_y)):             
                    if(end_y>start_y):
                        tmp_x+=1     
                else:
                    if(end_y<start_y):
                        tmp_x+=1
                #self.point_vec[tmp_x][index_y]=1
                self.point_vec.append((tmp_x,index_y))
                
            
    def paint_to_canvas(self):
        #print(self.point_vec)
        for (x,y) in self.point_vec:
            #print(x,y)
            self.canvas_image[y][x][0]=self.R
            self.canvas_image[y][x][1]=self.G
            self.canvas_image[y][x][2]=self.B

    def do_translate(self,dx,dy):
        self.x1+=dx
        self.x2+=dx
        self.y1+=dy
        self.y2+=dy
        self.point_vec=[]
        self.draw_line(self.x1,self.y1,self.x2,self.y2,self.algorithm)

    def do_rotate(self,x,y,r):
        self.point_vec=[]
        pi=math.pi
        r_dgree=(1-(float(r)/360))*2*pi
        #print(self.x1,self.y1,self.x2,self.y2,x,y,r,r_dgree)
        new_x1=x+(self.x1-x)*math.cos(r_dgree)-(self.y1-y)*math.sin(r_dgree)
        new_y1=y+(self.x1-x)*math.sin(r_dgree)+(self.y1-y)*math.cos(r_dgree)
        new_x2=x+(self.x2-x)*math.cos(r_dgree)-(self.y2-y)*math.sin(r_dgree)
        new_y2=y+(self.x2-x)*math.sin(r_dgree)+(self.y2-y)*math.cos(r_dgree)
        #print(new_x1,new_y1,new_x2,new_y2)
        self.x1=round(new_x1)
        self.x2=round(new_x2)
        self.y1=round(new_y1)
        self.y2=round(new_y2)
        self.draw_line(self.x1,self.y1,self.x2,self.y2,self.algorithm)

    def do_scale(self,x,y,scale_rate):
        self.point_vec=[]
        x1_range=self.x1-x
        x2_range=self.x2-x
        y1_range=self.y1-y
        y2_range=self.y2-y
        new_x1= round(x+scale_rate*(x1_range))
        new_x2= round(x+scale_rate*(x2_range))
        new_y1= round(y+scale_rate*(y1_range))
        new_y2= round(y+scale_rate*(y2_range))
        self.x1=new_x1
        self.x2=new_x2
        self.y1=new_y1
        self.y2=new_y2
        self.draw_line(self.x1,self.y1,self.x2,self.y2,self.algorithm)
        
    def do_clip(self,x1,y1,x2,y2,algorithm):
        
        if(algorithm=='Cohen-Sutherland'):
            return self.do_clip_cohen(x1,y1,x2,y2)
        elif(algorithm=='Liang-Barsky'):
            return self.do_clip_liang(x1,y1,x2,y2)

    def liang_test(self,p,q,t_list):
#to judge if the line is possible be inside the rectangle
        u=0.0
        if(p<0.0):
            u=q/p
            if(u>t_list[1]):
                return False
                #this is impossible because x1<x2 and the left point is at the left side of the left side
            elif(u>t_list[0]):
                t_list[0]=u
        elif(p>0.0):
            u=q/p
            if(u<t_list[0]):
                return False
                #this is also impossible
            elif(u<t_list[1]):
                t_list[1]=u
        else:
            if(q<0.0):
                return False
        return True

    
    def do_clip_liang(self,x1,y1,x2,y2):
        print('reach here')
        self.point_vec=[]
        x_min=min(x1,x2)
        x_max=max(x1,x2)
        y_min=min(y1,y2)
        y_max=max(y1,y2)
        t_list=[0.0,1.0]
        dx=float(self.x2-self.x1)
        dy=float(self.y2-self.y1)
        if(self.liang_test(-dx,float(self.x1-x_min),t_list)):
            if(self.liang_test(dx,float(x_max-self.x1),t_list)):
                if(self.liang_test(-dy,float(self.y1-y_min),t_list)):
                    if(self.liang_test(dy,float(y_max-self.y1),t_list)):
                        if(t_list[1]<=1.0):
                            self.x2=self.x1+t_list[1]*dx
                            self.y2=self.y1+t_list[1]*dy
                        if(t_list[0]>=0.0):
                            self.x1+=t_list[0]*dx
                            self.y1+=t_list[0]*dy
                        
                        self.draw_line(self.x1,self.y1,self.x2,self.y2,self.algorithm) 
                        print(self.x1,self.y1,self.x2,self.y2,t_list)
                        return True
                        #True represent that there is smthing inside 
        return False

    def do_clip_cohen(self,x1,y1,x2,y2):
        self.point_vec=[]
        x_max_real=max(self.x2,self.x1)
        x_min_real=min(self.x2,self.x1)
        y_min_real=min(self.y1,self.y2)
        y_max_real=max(self.y1,self.y2)
        x_max=max(x1,x2)
        x_min=min(x1,x2)
        y_max=max(y1,y2)
        y_min=min(y1,y2)
        print(x_min,x_max,y_min,y_max)
        bit1=self.y1>y_max
        bit2=self.y1<y_min
        bit3=self.x1>x_max
        bit4=self.x1<x_min

        bit5=self.y2>y_max
        bit6=self.y2<y_min
        bit7=self.x2>x_max
        bit8=self.x2<x_min

        print(bit1,bit2,bit3,bit4,bit5,bit6,bit7,bit8)
        

        if(not bit1 and not bit2 and not bit3 and not bit4 and not bit5 and not bit6 and not bit7 and not bit8):
            return True
            #no need inside the rectangular            
        elif((bit1 and bit5) or (bit2 and bit6) or (bit3 and bit7) or (bit4 and bit8)):
            return False
        else:
            if(self.x1==self.x2):
                self.y1=max(y_min_real,y_min)
                self.y2=min(y_max_real,y_max)    
                self.draw_line(self.x1,self.y1,self.x2,self.y2,self.algorithm) 
                return True
            elif(self.y1==self.y2):
                self.x1=max(x_min_real,x_min)
                self.x2=min(x_max_real,x_max)  
                self.draw_line(self.x1,self.y1,self.x2,self.y2,self.algorithm)
                return True
            else:
                print('reach here cal')
                rate=((float)(self.y1-self.y2))/((float)(self.x1-self.x2))
                print('rate is ',rate)
                y0=float(self.y1)-rate*self.x1
                y1=x_min*rate+y0
                y2=x_max*rate+y0
                x1=(y_min-y0)/rate
                x2=(y_max-y0)/rate
                print(y1,y2,x1,x2)
                print('xy_min is',x_min_real,y_min_real,x_max_real,y_max_real)
                new_x1=0
                new_x2=0
                new_y1=0
                new_y2=0
                point_index=0
                if(y1<y_max and y1>y_min and y1>=y_min_real and y1<=y_max_real):
                    point_index=1
                    new_x1=x_min
                    new_y1=y1
                if(y2<y_max and y2>y_min and y2>=y_min_real and y2<=y_max_real):
                    if(point_index==0):
                        point_index=1
                        new_x1=x_max
                        new_y1=y2
                    elif(point_index==1):
                        point_index=2
                        new_x2=x_max
                        new_y2=y2
                if(x1<=x_max and x1>=x_min and x1<=x_max_real and x1>=x_min_real):
                    if(point_index==0):
                        point_index=1
                        new_x1=x1
                        new_y1=y_min                
                    elif(point_index==1):
                        point_index=2
                        new_x2=x1
                        new_y2=y_min
                if(x2<=x_max and x2>=x_min and x2<=x_max_real and x2>=x_min_real):
                    if(point_index==0):
                        point_index=1
                        new_x1=x2
                        new_y1=y_max          
                    elif(point_index==1):
                        point_index=2
                        new_x2=x2
                        new_y2=y_max
                if(point_index==0):
                    print("index is 0")
                    return False
                if(point_index==1):
                    if(not bit1 and not bit2 and not bit3 and not bit4):
                        self.x2=new_x1
                        self.y2=new_y1
                        self.draw_line(self.x1,self.y1,self.x2,self.y2,self.algorithm)
                        return True
                    elif(not bit5 and not bit6 and not bit7 and not bit8):
                        self.x2=new_x1
                        self.y2=new_y1
                        self.draw_line(self.x1,self.y1,self.x2,self.y2,self.algorithm)
                        return True
                            
                elif(point_index==2):
                    self.x1=new_x1
                    self.y1=new_y1
                    self.x2=new_x2
                    self.y2=new_y2
                    self.draw_line(self.x1,self.y1,self.x2,self.y2,self.algorithm)
                    return True
                                
    




