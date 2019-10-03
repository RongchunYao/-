import sys
import canvas
import numpy as np
import line
import polygon
import gc
import math
import curve
import ellipse
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class graphic(canvas.canvas):
    def __init__(self):
        canvas.canvas.__init__(self)
        self.do_line=0
        self.graphic_id=0
        self.click_vec=[]
        self.do_polygon=0
        self.do_ellipse=0
        self.do_curve=0
        self.name='图形学大作业'
        self.window = QWidget()
        self.fix_width=800
        self.fix_height=800
        self.window.resize(self.fix_width+400, self.fix_height)
        self.text=QTextEdit(self.window)
        self.text.setGeometry(self.fix_width,0,400,250)
        self.text2=QTextEdit(self.window)
        self.text2.setGeometry(self.fix_width,250,400,150)
        self.text3=QTextEdit(self.window)
        self.text3.setGeometry(self.fix_width,400,275,400)
        #self.window.move(300, 300)
        self.window.setWindowTitle(self.name)
        self.image=QLabel(self.window)
        self.image.setGeometry(0,0,self.fix_width,self.fix_height)
        self.image.setScaledContents(True)
        self.image.setAlignment(Qt.AlignTop)
        self.image.setAlignment(Qt.AlignLeft)
        
        self.LineButton = QPushButton("线段",self.window)
        self.PolygonButton = QPushButton("多边形",self.window)
        self.EllipseButton = QPushButton("椭圆",self.window)
        self.CurveButton  = QPushButton("曲线",self.window)
        self.SaveButton = QPushButton("保存",self.window)
        self.CmdButton = QPushButton("执行命令行",self.window)
        self.CleanButton = QPushButton("清空画布",self.window)
        self.LineButton.clicked.connect(self.click_line)
        self.PolygonButton.clicked.connect(self.click_polygon)
        self.EllipseButton.clicked.connect(self.click_ellipse)
        self.CurveButton.clicked.connect(self.click_curve)
        self.SaveButton.clicked.connect(self.click_save)
        self.CmdButton.clicked.connect(self.click_cmd)
        self.CleanButton.clicked.connect(self.click_clean)
        self.image.mousePressEvent=self.click_image
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.LineButton)
        vbox.addWidget(self.PolygonButton)
        vbox.addWidget(self.EllipseButton)
        vbox.addWidget(self.CurveButton)
        vbox.addWidget(self.SaveButton)
        vbox.addWidget(self.CmdButton)
        vbox.addWidget(self.CleanButton)
        hbox=QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        self.window.setLayout(hbox)
        self.refresh()
        self.window.show()
    def click_clean(self):
        self.graphics=[]
        self.refresh()
        
    def click_image(self,event):
        x_pos= event.pos().x()
        y_pos= event.pos().y()
        print(x_pos,self.canvas_height-y_pos)
        if(self.do_line or self.do_polygon or self.do_curve or self.do_ellipse):
            self.click_vec.append((round(x_pos*float(self.canvas_width)/float(self.fix_width)),round(self.canvas_height-1-y_pos*float(self.canvas_height)/float(self.fix_height))))
        text=''
        for i in self.click_vec:
            text+='点击点： '+str(i[0])+','+str(i[1])+'\n'
        self.last_click_info=text
        self.text2.setText(text)
        print('click_image')

    def click_cmd(self):
        cmd=self.text3.toPlainText()
        if_last=0
        print('cmd is ,',cmd)
        cmd=cmd.split('\n')
        for i in cmd:                
                origin=i
                if(if_last==1):
                    last_cmd=last_cmd.replace('\n','')
                    i=last_cmd+' '+i
                i=i.replace('\n','')
                tmp_list = i.split(' ')
                if(len(tmp_list)==1):
                    continue
                if(len(i)==0):
                    continue
                res_list = tmp_list[1:]
                cmd_type = tmp_list[0]
                if(cmd_type=='drawPolygon' or cmd_type=='drawCurve'):
                    last_cmd=origin
                    if(if_last==1):
                        print('execute cmd is',cmd_type,res_list)
                        self.execute_cmd(cmd_type,res_list)
                        if_last=0
                    else:
                        if_last=1
                    continue
                print('execute cmd is',cmd_type,res_list)
                self.execute_cmd(cmd_type,res_list)
        print(self.graphics)
        for i in self.graphics:
            print('type is',i.type)
        self.refresh()
        self.text2.setText('命令行执行完毕\n')

    def check_click(self):
        
        if((self.do_line + self.do_polygon + self.do_curve + self.do_ellipse<2)==False):
            print('不规范的鼠标操作，已重置')
            self.do_line=0
            self.do_polygon=0
            self.do_curve=0
            self.do_ellipse=0
            self.click_vec=[]
            
    def click_save(self):
        self.check_click()        
        self.save_canvas(['output.bmp'])
        self.text2.setText('成功保存图片，图片名称为output.bmp')

    def click_line(self):
        
        print('click line')
        self.do_line +=1
        if(self.do_line==1):
            self.click_vec=[]
        if(self.do_line==2):
            
            line_id=self.graphic_id
            max_id=0
            for i in self.graphics:
                max_id=max(max_id,i.graphic_id)
            self.graphic_id=max_id+1
            algorithm='DDA'
            print(self.click_vec,self.R,self.G,self.B)
            new_line = line.line(self.canvas_image,line_id,self.canvas_width,self.canvas_height,self.R,self.G,self.B)
            new_line.draw_line(self.click_vec[0][0],self.click_vec[0][1],self.click_vec[1][0],self.click_vec[1][1],algorithm)
            self.do_line=0
            self.graphics.append(new_line)
            self.refresh()
            self.click_vec=[]
            return
            self.text2.setText('直线绘制完毕,点击的所有点为\n'+self.last_click_info)
        self.text2.setText('开始绘制直线')

    def click_polygon(self):
        self.check_click()
        print('click polygon')
        self.do_polygon+=1
        if(self.do_polygon==1):
            self.click_vec=[]
        if(self.do_polygon==2):
            
            poly_id=self.graphic_id
            max_id=0
            for i in self.graphics:
                max_id=max(max_id,i.graphic_id)
            self.graphic_id=max_id+1
            algorithm='DDA'
            print(self.click_vec,self.R,self.G,self.B)
            new_poly= polygon.polygon(self.canvas_image,poly_id,self.canvas_width,self.canvas_height,self.R,self.G,self.B)
            xy_vec=[]
            for i in range(len(self.click_vec)):
                xy_vec.append(self.click_vec[i][0])
                xy_vec.append(self.click_vec[i][1])
            new_poly.draw_poly(xy_vec,algorithm)
            self.do_polygon=0
            self.graphics.append(new_poly)
            self.refresh()
            self.click_vec=[]
            self.text2.setText('绘制多边形完毕,点击的所有点为\n'+self.last_click_info)
            return
        self.text2.setText('开始绘制多边形')

    def click_ellipse(self):
        self.check_click()
        print('click ellipse')
        self.do_ellipse+=1
        if(self.do_ellipse==1):
            self.click_vec=[]
        if(self.do_ellipse==2):
            ellipse_id=self.graphic_id
            max_id=0
            for i in self.graphics:
                max_id=max(max_id,i.graphic_id)
            self.graphic_id=max_id+1
            print(self.click_vec,self.R,self.G,self.B)
            new_ellipse = ellipse.ellipse(self.canvas_image,ellipse_id,self.canvas_width,self.canvas_height,self.R,self.G,self.B)
            print(self.click_vec[0][0],self.click_vec[0][1],self.click_vec[1][0],self.click_vec[1][1],self.click_vec[2][0],self.click_vec[2][1])
            new_ellipse.draw_ellipse(self.click_vec[0][0],self.click_vec[0][1],abs(self.click_vec[1][0]-self.click_vec[0][0]),abs(self.click_vec[2][1]-self.click_vec[0][1]))
            self.do_ellipse=0
            self.graphics.append(new_ellipse)
            self.refresh()
            self.click_vec=[]
            self.text2.setText('绘制椭圆完毕,点击的所有点为\n'+self.last_click_info)
            return
        self.text2.setText('开始绘制椭圆')


    def click_curve(self):
        self.check_click()
        print('click curve')
        self.do_curve+=1
        if(self.do_curve==1):
            self.click_vec=[]
        if(self.do_curve==2):
            curve_id=self.graphic_id
            max_id=0
            for i in self.graphics:
                max_id=max(max_id,i.graphic_id)
            self.graphic_id=max_id+1
            algorithm = 'B-spline'
            print(self.click_vec,self.R,self.G,self.B)
            new_curve = curve.curve(self.canvas_image,curve_id,self.canvas_width,self.canvas_height,self.R,self.G,self.B)
            xy_vec=[]
            for i in range(len(self.click_vec)):
                xy_vec.append(self.click_vec[i][0])
                xy_vec.append(self.click_vec[i][1])
            print(xy_vec)
            new_curve.draw_curve(xy_vec,algorithm)
            self.do_curve=0
            self.graphics.append(new_curve)
            self.refresh()
            self.click_vec=[]
            self.text2.setText('曲线绘制完毕,点击的所有点为\n'+self.last_click_info)
            return
        self.text2.setText('开始绘制曲线')

    def refresh(self):
        show_text=''
        print('刷新屏幕')
        super().refresh()
        for i in self.graphics:
            i.paint_to_canvas()
            show_text+=i.get_text()
        self.text.setText(show_text)
        #print(self.canvas_image)
        tmp_image=np.zeros((self.canvas_height,self.canvas_width,3),dtype=int)
        for i in range(self.canvas_height):
                    tmp_image[i]=self.canvas_image[self.canvas_height-1-i]
        data=np.require(tmp_image,np.uint8,'C')
        pixmap = QPixmap.fromImage(QImage(data,data.shape[1],data.shape[0],data.strides[0],QImage.Format_RGB888))
        gc.collect()
        self.image.setPixmap(pixmap)

        
    
        

if __name__ == '__main__':
    argv_list = sys.argv
    
    if(len(argv_list)==1):
        app = QApplication(sys.argv)
        graphic=graphic()
        sys.exit(app.exec_())


    if(len(argv_list)==2):
        my_canvas = canvas.canvas()
        if_last=0
        input_file = argv_list[1]
        with open(input_file,'r') as cmd_file:
            cmd=cmd_file.readlines()
            last_cmd=''
            if_last=0
            for i in cmd:
                
                origin=i
                if(if_last==1):
                    last_cmd=last_cmd.replace('\n','')
                    i=last_cmd+' '+i
                i=i.replace('\n','')
                tmp_list = i.split(' ')
                if(len(tmp_list)==1):
                    continue
                if(len(i)==0):
                    continue
                res_list = tmp_list[1:]
                cmd_type = tmp_list[0]
                if(cmd_type=='drawPolygon' or cmd_type=='drawCurve'):
                    last_cmd=origin
                    if(if_last==1):
                        print('execute cmd is',cmd_type,res_list)
                        my_canvas.execute_cmd(cmd_type,res_list)
                        if_last=0
                    else:
                        if_last=1
                    continue
                print('execute cmd is',cmd_type,res_list)
                my_canvas.execute_cmd(cmd_type,res_list)




