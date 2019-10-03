import numpy as np
import line
import math
class curve(line.line):
    def __init__(self,canvas_image,curve_id,w,h,R,G,B):
        line.line.__init__(self,canvas_image,curve_id,w,h,R,G,B)
        self.type = 3 # 3 stand for curves
        self.algorithm = 'Bezier'

    def draw_curve(self,xy_vec,algorithm):
         
        self.xvec=[]
        self.yvec=[]

        print(xy_vec)
        xy_len = int(len(xy_vec)/2)
        print(xy_len)
        print('reach here')
        self.n=xy_len
        for j in range(xy_len):
            self.xvec.append((int)(xy_vec[2*j]))
            self.yvec.append((int)(xy_vec[2*j+1]))
        self.draw_curve2()

    def draw_curve2(self):

        if(self.n==2):
            self.draw_line(self.xvec[0],self.yvec[0],self.xvec[1],self.yvec[1],'DDA')
            return 

        if(self.algorithm=="Bezier"):
            self.draw_Bezier()    
        
        elif(self.algorithm=="B-spline"):
            self.draw_Bspline()

    def C(self,a,b):
        return (math.factorial(a)/math.factorial(b))/math.factorial(a-b)

    def draw_Bezier(self):
        self.point_vec.append((self.xvec[0],self.yvec[0]))
        self.point_vec.append((self.xvec[-1],self.yvec[-1]))
        
        rate = 0.000
        last_val=(-1,-1)
        for i in range(1000):
            t=rate
            B_tx=0.0
            B_ty=0.0
            for j in range(0,self.n):
                B_t =self.C(self.n-1,j)*((1-t)**(self.n-1-j))*(t**j)
                B_tx += B_t*self.xvec[j]
                B_ty += B_t*self.yvec[j]
            #print((round(B_tx),round(B_ty)))
            if((round(B_tx),round(B_ty))!=last_val):
                last_val= (round(B_tx),round(B_ty))
                self.point_vec.append((round(B_tx),round(B_ty)))
            rate+=0.001
    
    def N(self,i,p,u):
        if(p==0):
            if(self.u[i]<=u and u<self.u[i+1]):
                return 1.0
            else:
                return 0.0
        else:
            if(self.u[i+p]-self.u[i]==0):
                first_arg=0.0
            else:
                first_arg=((u-self.u[i])/(self.u[i+p]-self.u[i]))
            if((self.u[i+p+1]-self.u[i+1])==0):
                second_arg=0.0
            else:
                second_arg=((self.u[i+p+1]-u)/(self.u[i+p+1]-self.u[i+1]))

            
            ret_val=  first_arg*self.N(i,p-1,u)+second_arg*self.N(i+1,p-1,u) 
            return ret_val
    
    def B_spline(self,t):
        x_val=0.0
        y_val =0.0
        for i in  range(0,self.n):
            x_val+=self.N(i,self.dim,t)*self.xvec[i]
            y_val+=self.N(i,self.dim,t)*self.yvec[i]
        return (round(x_val),round(y_val))

    def draw_Bspline(self):
        
        self.dim=3 #set the dim

        assert(self.n>=self.dim+1)
        self.node_size = self.n+self.dim+1
        self.u=[]
        
        #set the note val
        u_val=0.0
        inter = 1.0/(self.node_size-2*self.dim-1)
        for i in range(self.node_size):
            if(i<=self.dim):
                self.u.append(u_val)
            else:
                u_val+=inter
                if(u_val>=1.0):
                    u_val=1.0
                self.u.append(u_val)

        start_rate=0.000
        last_val=(-1,-1)
        for i in range(1000):
            
            val=self.B_spline(start_rate)
            if(val!=last_val):
                last_val=val
                self.point_vec.append(val)
                #print(val)
            start_rate+=0.001


    def do_translate(self,dx,dy):
        for i in range(len(self.xvec)):
            self.xvec[i]+=dx
            self.yvec[i]+=dy
        self.draw_curve2()

    def get_text(self):
        ret='曲线\n'
        ret+='id 为'+str(self.graphic_id)+'\n'
        ret+= 'RGB is '+ str(self.R) +' '+ str(self.G)+ ' ' + str(self.B)+'\n'
        for i in range(len(self.xvec)):
            ret+='('+str(self.xvec[i])+','+str(self.h-self.yvec[i])+')'
        ret+='\n'
        return ret  

    def do_rotate(self,x,y,r):
        self.point_vec=[]
        for i in range(len(self.xvec)):
            
            pi=math.pi
            r_dgree=(1-(float(r)/360))*2*pi
            new_x=x+(self.xvec[i]-x)*math.cos(r_dgree)-(self.yvec[i]-y)*math.sin(r_dgree)
            new_y=y+(self.xvec[i]-x)*math.sin(r_dgree)+(self.yvec[i]-y)*math.cos(r_dgree)
            self.xvec[i]=new_x
            self.yvec[i]=new_y
        self.draw_curve2()
    
    
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
        self.draw_curve2()
            
                

        

         
        
