# -*- coding: utf-8 -*-
'''
作者:ＣＵＧＢ赵治
硬件环境：PC
运行环境：Windows10
可能会出现的报错：
    RuntimeError: PROJ: proj_create_from_database: Cannot find proj.db。空间参考定义由于GDAL3.0以后的版本依赖的PROJ库必须是6.0+的版本，解决办法有两个--》
    1.将proj.db文件所在路径加入系统变量中。
    2.安装GADL3.0以下的版本
'''
import sys, time,os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']# 脚本打包后由于不再是由Python解释脚本的形式运行，__file__变量会失去作用。此时具有类似效用的是sys.executable，同时可以利用sys.frozen属性来判断是打包的exe还是py脚本。需要在导入PyQt5之前引入该语句。
import cv2 as cv
import numpy as np
import math
from osgeo import gdal, ogr, osr,gdal_array #地理及遥感数据运算的核心开源库。
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import Qt,QPoint, QPointF, QLine, QLineF, QRect, QRectF,QTime,qrand
from PyQt5.QtGui import QImage, QPixmap,QPainter,QBrush, QPen, QColor, QRadialGradient,QPainterPath,QPicture,QPolygonF,QPolygon
from PyQt5.QtWidgets import QAction,QWidget, QPushButton, QApplication, QMessageBox, QFileDialog,QGraphicsScene, QGraphicsPixmapItem,QMainWindow,QGraphicsView,QGraphicsItem,QSizePolicy
#通过from…import…导入PyQt5中所需的模块，减轻脚本依赖。

from GUI.Main1 import Ui_MainWindow as  GUI0 #导入界面脚本。
from GUI.SFC1 import sFC
from GUI.ShowGraphic import myGraphicsScene,myGraphicsView
from GUI.WindowMove import windowMove
gdal.UseExceptions()   # 抛出gdal异常
gdal.AllRegister()    #gdal库需要注册后使用。
ogr.UseExceptions()  #抛出异常
ogr.RegisterAll()   #ogr库需要注册后使用。
wholefiletype =['.jpg','.jpeg','.JPG','.JPEG','.tif','.TIF'] #创建一个数组存储图象格式
currentfiletype =['.shp','.txt'] #创建一个存储矢量文件的数组。
global points
points= []

class mainGUI(QMainWindow, GUI0):
    count = 0
    path = ""
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.btnsample.clicked.connect(self.samplegui)
        # self.btnpre.clicked.connect(self.show_panel)
        # self.btnfolder.clicked.connect(self.show_panel)
        # self.addfile.clicked.connect(self.read_file)
        #显示图片的控件
        self.item = QGraphicsPixmapItem()
        self.item.setZValue(0)
        self.scene = myGraphicsScene()
        self.view = myGraphicsView()
        self.view.setMinimumSize(QtCore.QSize(0, 0))
        self.picture.addWidget(self.view, 0, 0)
        self.view.setScene(self.scene)
        self.scene.mousePressEvent = self.graphicsScene_clicked
        self.current_path =""
        # self.block_size = int(self.picture_size.toPlainText())  # 设定剪裁大小,鼠标点击点即为采样点坐标原点
        self.menubar = self.menuBar()
        self.menubar.triggered[QAction].connect(self.processtrigger)

    def processtrigger(self, qaction):
        if qaction.text() == "打开":
            self.read_file()
        if qaction.text() == "锐化":
            self.sharpen()
        if qaction.text() == "NDVI":
            self.ndvi()
        if qaction.text() == "图像变化":
            self.sFC = sFC()
            self.sFC.build_comboBox(self.count)
            self.sFC.btn_SFC.clicked.connect(lambda:self.func_standardFakeColor(int(self.sFC.red.currentIndex()),int(self.sFC.green.currentIndex()),int(self.sFC.blue.currentIndex())))
            self.sFC.show()
        # if qaction.text() == "关闭":
        #     self.closeEvent()
        if qaction.text() == "全栅格自动采集":
            self.windowMove = windowMove()
            self.block_size = self.windowMove.returnwidth()
            self.windowMove.btn_WindowMove.clicked.connect(lambda:self.func_windowMove(self.windowMove.returnwidth(),self.windowMove.returnstep()))
            self.windowMove.show()
        if qaction.text() == "撤销标记":
            self.clearPoints()
        if qaction.text() == "shp文件":
            # try:
            #     self.read_current_file()
            #     self.exec_clipWithShp()
            # except:
            #     self.showpanel.append("操作异常")
            #     return
            self.read_current_file()
            self.exec_clipWithShp()
        # if qaction.text() == "txt文件":
        # if qaction.text() == "NDVI采样":
        # if qaction.text() == "开始采样":
        # if qaction.text() == "矩形":
        # if qaction.text() == "多边形":

    def read_file(self):
        '''
        加载图像函数
        '''
        self.path, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./", "All Files(*)")
        if self.errorFormatWarn1() == False:#处理异常
            return
        try:
            dataset = gdal.Open(self.path, gdal.GA_ReadOnly)
            self.data = dataset
        except:
            self.showpanel.append("无法打开影像")
            return
        self.count = dataset.RasterCount

        if(self.count>3):
            outpath= self.formatConverse(self.path)
            self.sharpenpath = outpath
            self.showpanel.append("转换为三通道显示")
        else:
            outpath = self.path
            self.sharpenpath = outpath
        self.showpanel.append("文件读取成功")
        self.showpanel.append("\n图像位置："+self.data.GetDescription() +"\n图像波段："+str(self.data.RasterCount)+"\n图像长度：" +str(self.data.RasterXSize) + "\n图像宽度：" + str(self.data.RasterYSize))
        img = cv.imread("{}".format(outpath))  # 读取图像
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # 转换图像通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        items = self.scene.items()  #获取场景中的所有图元
        if len(items)!=0:           #加载新的图像时，移除原图元
            for item in items:
                self.scene.removeItem(item)
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item.setPixmap(pix)         # 创建图元
        # self.item.setTransformOriginPoint(QPointF(0,0))
        self.scene.setSceneRect(0,0,x,y)
        self.scene.addItem(self.item)
    def read_current_file(self):
        '''
        加载已有的文件，如矢量shp格式文件或txt文件
        '''
        path, filetype = QFileDialog.getOpenFileName(self, "选取掩膜文件", "./", "All Files(*)")
        self.current_path = path
        if self.errorFormatWarn_shp() == False: #处理异常
            self.current_path = ""
            return
        else:
            self.showpanel.append("shp文件读取成功")
    def graphicsScene_clicked(self,event):
        '''
        加载图像函数
        '''
        e = event.scenePos()
        theX = int(e.x())
        theY = int(e.y())
        self.showpanel.append("栅格坐标({},{})".format(str(theX), str(theY)))
        points.append((theX,theY))
        pen = QPen(Qt.red,5)
        self.scene.addRect(theX-2,theY-2,4,4,pen)


    def closeEvent(self, event):
        '''
        界面关闭确认
        '''
        reply = QMessageBox.question(self,"警告","你确认要退出吗？",QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def errorFormatWarn1(self):
        '''
        自定义函数处理异常--载入影像格式异常
        '''
        res = os.path.splitext(self.path)[1] in wholefiletype
        if res == False:
            self.showpanel.append("请重新选择图像格式的文件")
            QMessageBox.warning(self, "警告", "请重新选择图像格式的文件！", QMessageBox.Ok)
            return False
    def errorFormatWarn_shp(self):
        '''
        自定义函数处理异常--载入矢量图像格式异常
        '''
        res = os.path.splitext(self.current_path)[1] in currentfiletype
        if res == False:
            QMessageBox.warning(self, "警告", "请重新选择图像格式的文件！", QMessageBox.Ok)
            return False
    def formatConverse(self,img):
        '''
        对一些OPENCV库不能直接显示的影像进行转换或者将多通道影像转换为三通道影像进行显示
        '''
        try:
            dataset = gdal.Open(img, gdal.GA_ReadOnly)
        except:
            self.showpanel.append('无法打开文件' + str(img) + ',请重新选取文件')
            return
        projection = dataset.GetProjection()
        geotransform = dataset.GetGeoTransform()
        data = dataset.ReadAsArray(0, 0, dataset.RasterXSize, dataset.RasterYSize)
        if 'int8' in data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        if len(data.shape) == 1:
            bands, height, width = 1, data.shape
        else:
            bands, height, width = data.shape
        # 创建文件
        if bands != 1:
            bands = 3
        driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
        conversed_path = 'optimized/conversed.tif'
        # self.filepath.setText(conversed_path)
        outdataset = driver.Create(conversed_path, width, height, bands, datatype)

        outdataset.SetGeoTransform(geotransform)  # 写入仿射变换参数
        outdataset.SetProjection(projection)  # 写入投影

        if bands == 1:
            outdataset.GetRasterBand(1).WriteArray(data)  # 写入数组数据
        else:
            # for i in range(bands):
            #     print(bands,i)
            #     outdataset.GetRasterBand(i + 1).WriteArray(data[i])
            outdataset.GetRasterBand(1).WriteArray(data[6])
            outdataset.GetRasterBand(2).WriteArray(data[3])
            outdataset.GetRasterBand(3).WriteArray(data[0])
        del outdataset
        return conversed_path
    def noPictureWarn(self):
        '''
        自定义函数处理异常--未加载图像异常
        '''
        if self.path=="":
            self.showpanel.append("请先加载图像")
            QMessageBox.warning(self, "警告", "请先加载图像！", QMessageBox.Ok)
            return False
    def func_windowMove(self,width,step):
        imgwidth = self.data.RasterXSize-10
        imglen = self.data.RasterYSize-10
        num1 = int((imgwidth - width / 2) // step)
        num2 = int((imglen - width / 2) // step)
        for i in range(num1):
            X = step * i+5
            for j in range(num2):
                Y = step * j+5
                points.append((X, Y))
        # 减少10个单位的长宽、并且采样位置分别距左上角缩进5个单位是因为仿射变换造成的偏差。

        self.gdalClip()
        self.windowMove.close()
    def ndvi(self):
        '''
       图像预处理：
           植被归一化指数计算，公式为近红外波段的反射值与红光波段的反射值之差比上两者之和，便于用户采样。
        注！！！需加载大于3个波段的卫星影像并存在近红外与红外波段，通常为第4和第3波段，以达到目的，否则加载如RGB等图片格式的图像会报错。
        Return:2值化图像
        '''
        self.showpanel.append("当前操作--NDVI计算，请等待-------------------")
        if self.noPictureWarn() == False:#处理异常
            return

        try:
            dataset = gdal.Open(self.path,gdal.GA_ReadOnly)
            band3 = dataset.GetRasterBand(3)  # 提取近红外波段，默认为第三波段
            band4 = dataset.GetRasterBand(4)  # 提取红外波段，默认为第四波段
        except Exception as e:
            self.showpanel.append("无法打开影像或者不存在四个波段,请重新选取文件"+str(e))
            return
        projection = dataset.GetProjection()
        geotransform = dataset.GetGeoTransform()

        map_band3 = band3.ReadAsArray(0, 0, dataset.RasterXSize, dataset.RasterYSize).astype(np.float32)
        map_band4 = band4.ReadAsArray(0, 0, dataset.RasterXSize, dataset.RasterYSize).astype(np.float32)

        ndvi_normalized = 1.0 * (map_band4 - map_band3) / 1.0 * (map_band4 + map_band3) #运算
        ndvi = ndvi_normalized * 255    #归一化到0-255，增大差异，方便用户观看

        red = dataset.GetRasterBand(3).ReadAsArray() * 0.0001
        nir = dataset.GetRasterBand(4).ReadAsArray() * 0.0001
        ndvi = (nir - red) / (nir + red)  # 将NAN转化为0值
        nan_index = np.isnan(ndvi)
        ndvi[nan_index] = 0
        ndvi = ndvi.astype(np.float32)
        ndvi = ndvi * 255

        prepicture_path = 'optimized/ndvi.tif'
        tif_driver = gdal.GetDriverByName("GTiff")
        out_dataset = tif_driver.Create(prepicture_path, dataset.RasterXSize, dataset.RasterYSize, 1,band3.DataType)# 设置裁剪出来图的原点坐标
        out_dataset.SetGeoTransform(geotransform)# 设置SRS属性（投影信息）
        out_dataset.SetProjection(projection)# 写入目标文件
        out_dataset.GetRasterBand(1).WriteArray(ndvi)# 将缓存写入磁盘
        out_dataset.FlushCache()
        del out_dataset
        img = cv.imread(prepicture_path)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        x = img.shape[1]
        y = img.shape[0]
        self.zoomscale = 1
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item.setPixmap(pix)
        self.scene.addItem(self.item)
        self.showpanel.append("ndvi over")
    def func_standardFakeColor(self,count1,count2,count3):
        '''
       图像预处理：
           假彩色处理（图像变换），对已加载的影像进行假彩色合成处理,用户可自定义红绿蓝三通道分别选取何种波段。
        '''
        self.showpanel.append("当前操作--假彩色变换，请等待--------------------------------")
        if self.noPictureWarn() == False:  # 处理异常
            return
        path = self.path
        arr = gdal_array.LoadFile("{}".format(path))
        prepicture_path = "optimized/standardFakeColor.tif"
        output = gdal_array.SaveArray(arr[[count1,count2,count3],:], prepicture_path, format="GTiff", prototype=path)
        output = None # 取消输出避免在某些平台上损坏文件
        img = cv.imread("{}".format(prepicture_path))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        x = img.shape[1]
        y = img.shape[0]
        self.zoomscale = 1
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item.setPixmap(pix)
        self.scene.addItem(self.item)
        self.showpanel.append("standard fake color over")#通知栏打印结果
    def sharpen(self):
        '''
        图像预处理：
            锐化，对已加载的影像进行锐化处理，并自动加载锐化后的图像，便于用户采样。
        '''
        self.showpanel.append("当前操作--锐化，请等待--------------------------------")
        if self.noPictureWarn() == False:
            return
        img = cv.imread("{}".format(self.sharpenpath),-1)
        kernel_sharpen_1 = np.array([       #创建3x3的锐化模板
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]])
        output_1 = cv.filter2D(img, -1, kernel_sharpen_1)   #使用cv2库的filter2D函数进行锐化
        prepicture_path ="optimized/sharpen.tif"
        cv.imwrite(prepicture_path,output_1)
        self.showpanel.append("sharpen over")
        img = cv.imread("{}".format(prepicture_path))  # 读取图像
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # 转换图像通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item.setPixmap(pix)
        self.scene.addItem(self.item)

    # def clipCureentShp1(self):
    #     input_shape =self.current_path.text()
    #     print(input_shape)
    # def opencvClip(self):
    #     '''
    #     主要执行功能：
    #         利用cv2开源库进行影像采样，仅栅格影像取样。
    #     '''
    #     self.showpanel.append("当前操作--opencvClip，请等待--------------------------------")
    #     if self.noPictureWarn() == False:
    #         return
    #     if self.noPictureWarn() ==False:
    #         return
    #     self.block_size = int(self.self.block_size.toPlainText())  # 设定剪裁大小,鼠标点击点即为采样点坐标原点
    #     picture_height = int(self.picture_height.toPlainText())
    #     # self.showpanel.append("裁剪长宽",self.block_size,picture_height)
    #
    #     try:
    #         img = cv.imread("{}".format(self.path))
    #     except:
    #         self.showpanel.append("无法打开影像，请重新选择")
    #         return
    #     for x,y in points:      #遍历读取用户采集点的数组，依次剪裁影像。
    #         x1 = str(x)
    #         y1 = str(y)
    #         cv.imwrite("opencvClip/sample" + x1 + "-" + y1 + ".tif",img[y:y + picture_height, x:x + self.block_size])
    #     self.showpanel.append("opencvClip success")
    #     self.clearPoints()    # 清空数组，避免每次操作时仍残留上一次采集点
    def gdalClip(self):
        '''
        主要执行功能：
            利用gdal开源库进行影像采样，仅栅格影像取样。
        注：
            两个开源库cv2和gdal对影像的处理能力略有不同，加载数据较大的影像时选择gdal库剪裁为较优选。
        '''
        self.showpanel.append("当前操作--gdalClip，请等待--------------------------------")
        if self.noPictureWarn() == False:
            return

        try:
            dataset = gdal.Open(self.path, gdal.GA_ReadOnly)
        except:
            self.showpanel.append("非栅格影像，无法使用该功能")
            return

        if self.noPictureWarn() == False:
            return

        projection = dataset.GetProjection()
        # rasterwkt = projection.ExportToWkt()
        geotransform = dataset.GetGeoTransform()
        top_left_x = geotransform[0]  # 左上角x坐标
        horizon_pixel_resolution = geotransform[1]  # 东西方向像素分辨率
        top_left_y = geotransform[3]  # 左上角y坐标
        vertical_pixel_resolution = geotransform[5]  # 南北方向像素分辨率
        # print("地理坐标 = ({}, {})\n像素等级 = ({}, {})\n影像大小 = ({}, {})\n投影= {}".format(top_left_x, top_left_y,horizon_pixel_resolution,vertical_pixel_resolution,dataset.RasterYSize,dataset.RasterXSize, projection))
        band1 = dataset.GetRasterBand(1)
        band2 = dataset.GetRasterBand(2)
        band3 = dataset.GetRasterBand(3)
        # 剪裁框大小
        for x, y in points:
            offset_x = x
            offset_y = y

            out_band1 = band1.ReadAsArray(offset_x, offset_y, self.block_size, self.block_size)
            out_band2 = band2.ReadAsArray(offset_x, offset_y, self.block_size, self.block_size)
            out_band3 = band3.ReadAsArray(offset_x, offset_y, self.block_size, self.block_size)
            tif_driver = gdal.GetDriverByName("GTiff")
            out_dataset = tif_driver.Create('gdalClip/sample' + '-' + str(offset_x) + '-' + str(offset_y) + '.tif',
                                            self.block_size, self.block_size, 3, band1.DataType)
            # 仿射变换
            top_left_x = top_left_x + offset_x * horizon_pixel_resolution
            top_left_y = top_left_y + offset_y * vertical_pixel_resolution
            # 将计算后的值组装为一个元组，以方便设置
            dst_transform = (top_left_x, geotransform[1], geotransform[2], top_left_y, geotransform[4], geotransform[5])
            # 设置裁剪出来图的原点坐标
            out_dataset.SetGeoTransform(dst_transform)
            # 设置SRS属性（投影信息）
            out_dataset.SetProjection(dataset.GetProjection())
            # 写入目标文件
            out_dataset.GetRasterBand(1).WriteArray(out_band1)
            out_dataset.GetRasterBand(2).WriteArray(out_band2)
            out_dataset.GetRasterBand(3).WriteArray(out_band3)
            # 将缓存写入磁盘
            out_dataset.FlushCache()
            del out_dataset
        self.showpanel.append("gdalClip success")
        self.clearPoints()
    # def clipWithShp(self):
    #
    #     '''
    #     主要执行功能：
    #         根据已有的shp矢量文件进行采样，得到栅格矢量配套的采样组。
    #     '''
    #     self.showpanel.append("当前操作--clipCurrentShp，请等待--------------------------------")
    #     if self.noPictureWarn() == False:
    #         return
    #     shp_driver = ogr.GetDriverByName("ESRI Shapefile")  # shp驱动器
    #     # 处理异常
    #     try:
    #         dataset = gdal.Open(self.path, gdal.GA_ReadOnly)
    #     except:
    #         self.showpanel.append("非栅格影像，无法使用该功能")
    #         return
    #     try:
    #         shp_dataset = shp_driver.Open(self.current_path)
    #     except:
    #         self.showpanel.append("无法打开矢量文件，无法使用该功能")
    #         return
    #     def xtoArray(x, offsetx, resolutionx):#返回屏幕x坐标
    #         screenx = (x - offsetx) / resolutionx
    #         return screenx
    #     def ytoArray(y, offsety, resolutiony):#返回屏幕y坐标
    #         screeny = (offsety - y) / resolutiony
    #         return screeny
    #     projection = dataset.GetProjection()
    #     # rasterwkt = projection.ExportToWkt()
    #     geotransform = dataset.GetGeoTransform()
    #     top_left_x = geotransform[0]  # 左上角x坐标
    #     horizon_pixel_resolution = geotransform[1]  # 东西方向像素分辨率
    #     top_left_y = geotransform[3]  # 左上角y坐标
    #     vertical_pixel_resolution = - geotransform[5]  # 南北方向像素分辨率
    #     # print("地理坐标 = ({}, {})\n像素等级 = ({}, {})\n影像大小 = ({}, {})\n投影= {}".format(top_left_x, top_left_y,horizon_pixel_resolution,vertical_pixel_resolution,dataset.RasterYSize, dataset.RasterXSize, projection))
    #     # gdal中的坐标系方式不同于笛卡尔
    #     band1 = dataset.GetRasterBand(1)
    #     band2 = dataset.GetRasterBand(2)
    #     band3 = dataset.GetRasterBand(3)
    #     # 剪裁框大小
    #     layer = shp_dataset.GetLayer(0)
    #     newSpatialRef = layer.GetSpatialRef()
    #     clipxmax = dataset.RasterYSize - 50
    #     clipymax = dataset.RasterXSize - 50
    #     indexOfNo = []
    #     indexOfYes = []
    #     for index, feat in enumerate(layer):
    #         geom = feat.GetGeometryRef()
    #         sp_xmin, sp_xmax, sp_ymin, sp_ymax = geom.GetEnvelope()
    #         # print(xmin,xmax,ymin,ymax)
    #         xmin = int(xtoArray(sp_xmin, top_left_x, horizon_pixel_resolution)) - 49
    #         xmax = int(xtoArray(sp_xmax, top_left_x, horizon_pixel_resolution))
    #         ymin = int(ytoArray(sp_ymax, top_left_y, vertical_pixel_resolution)) - 49
    #         ymax = int(ytoArray(sp_ymin, top_left_y, vertical_pixel_resolution))
    #         self.block_size = xmax - xmin + 49
    #         self.block_size = ymax - ymin + 49
    #
    #
    #         if xmin < 50 or ymin < 50 or xmax > clipxmax or ymax > clipymax:
    #             indexOfNo.append(index)
    #             continue
    #         #以上9行代码用于检验超出栅格剪裁范围的矢量图形，跳过
    #         createV = 'clip_current_shp/sample-' + str(index) + '.shp'  # 新建矢量名称
    #         out_datasetV = shp_driver.CreateDataSource(createV)
    #         newlayer = out_datasetV.CreateLayer('test', geom_type=ogr.wkbPolygon, srs=newSpatialRef)
    #         fieldDefn = ogr.FieldDefn('id', ogr.OFTString)
    #         fieldDefn.SetWidth(8)
    #         newlayer.CreateField(fieldDefn)
    #         featureDefn = newlayer.GetLayerDefn()
    #         newfeature = ogr.Feature(featureDefn)
    #         newfeature.SetGeometry(feat.GetGeometryRef())
    #         newfeature.SetField('id', index)
    #         newlayer.CreateFeature(newfeature)
    #         out_datasetV.Destroy()
    #         indexOfYes.append(index)
    #         #以下代码用于生成与shp文件对应的栅格图像。
    #         out_band1 = band1.ReadAsArray(xmin, ymin, self.block_size, self.block_size)
    #         out_band2 = band2.ReadAsArray(xmin, ymin, self.block_size, self.block_size)
    #         out_band3 = band3.ReadAsArray(xmin, ymin, self.block_size, self.block_size)
    #         tif_driver = gdal.GetDriverByName("GTiff")
    #         out_dataset = tif_driver.Create('clip_current_shp/sample-' + str(index) + '.tif', self.block_size, self.block_size,3, band1.DataType)
    #         top_left_x49 = sp_xmin - 49 * horizon_pixel_resolution
    #         top_left_y49 = sp_ymax + 49 * vertical_pixel_resolution  # 注意y轴的增减方向
    #         # 将计算后的值组装为一个元组，以方便设置
    #         dst_transform = (top_left_x49, geotransform[1], geotransform[2], top_left_y49, geotransform[4],geotransform[5])# 栅格数据读入时，以左上角为原点，此时ReadAsArray是屏幕坐标，但左上角的经纬度坐标是经度最小值，纬度最大值
    #         out_dataset.SetGeoTransform(dst_transform) # 设置裁剪出来图的原点坐标
    #         out_dataset.SetProjection(dataset.GetProjection())# 设置SRS属性（投影信息）
    #         # 写入目标文件
    #         out_dataset.GetRasterBand(1).WriteArray(out_band1)
    #         out_dataset.GetRasterBand(2).WriteArray(out_band2)
    #         out_dataset.GetRasterBand(3).WriteArray(out_band3)
    #         out_dataset.FlushCache()# 将缓存写入磁盘
    #         del out_dataset
    #     layer.ResetReading()  # 复位
    #     shp_dataset.Destroy()
    #     self.showpanel.append("clipCurrentShp success")
    #     indexOfNo = str(indexOfNo)
    #     self.showpanel.append(indexOfNo)
    #     self.showpanel.append("以上序号的矢量文件超出栅格范围无法剪裁")
    #     indexOfYes = str(indexOfYes)
    #     self.showpanel.append(indexOfYes)
    #     self.showpanel.append("以上序号成功剪裁")
    #     self.clearPoints()
    def exec_clipWithShp(self):
        bandcount = self.data.RasterCount
        if self.noPictureWarn() == False:
            return
        shp_driver = ogr.GetDriverByName("ESRI Shapefile")  # shp驱动器
        # 处理异常
        try:
            shp_dataset = shp_driver.Open(self.current_path)
            self.showpanel.append("当前操作--clipCurrentShp，请等待--------------------------------")
        except:
            self.showpanel.append("无法打开矢量文件，无法使用该功能")
            return
        band1 = self.data.GetRasterBand(1)
        projection = self.data.GetProjection()
        # rasterwkt = projection.ExportToWkt()
        geotransform = self.data.GetGeoTransform()
        top_left_lon = geotransform[0]  # 左上角x坐标,经度
        lon_resolution = geotransform[1]  # 东西方向像素分辨率
        top_left_lat = geotransform[3]  # 左上角y坐标，纬度
        lat_resolution = geotransform[5]  # 南北方向像素分辨率
        # print("地理坐标 = ({}, {})\n像素等级 = ({}, {})\n影像大小 = ({}, {})\n投影= {}".format(top_left_x, top_left_y,horizon_pixel_resolution,vertical_pixel_resolution,dataset.RasterYSize, dataset.RasterXSize, projection))
        # gdal中的坐标系方式不同于笛卡尔
        RasterYSize= self.data.RasterYSize
        RasterXSize= self.data.RasterXSize
        bottom_right_lon =top_left_lon+RasterXSize*lon_resolution
        bottom_right_lat =top_left_lat+RasterYSize*lat_resolution
        layer = shp_dataset.GetLayer(0)
        newSpatialRef = layer.GetSpatialRef()
        indexOfNo = []
        indexOfYes = []
        def lonToArray(x, offsetx, resolutionx):  # 返回屏幕x坐标
            screenx = (offsetx - x) / resolutionx
            return screenx
        def latToArray(y, offsety, resolutiony):  # 返回屏幕y坐标
            screeny = (offsety - y) / resolutiony
            return screeny
        def clipWithShp(xmin, ymin,out_dataset,num,size1,size2):
            for i in range(num):
                bandnum = i + 1
                band = self.data.GetRasterBand(bandnum)
                out_band = band.ReadAsArray(xmin, ymin, size1, size2)
                out_dataset.GetRasterBand(bandnum).WriteArray(out_band)
                out_dataset.FlushCache()  # 将缓存写入磁盘
        for index, feat in enumerate(layer):
            geom = feat.GetGeometryRef()
            lon_min, lon_max, lat_min, lat_max = geom.GetEnvelope()
            if lon_min<top_left_lon or lon_max>bottom_right_lon or lat_min<bottom_right_lat or lat_max>top_left_lat:
                indexOfNo.append(index)
                continue
            Xleft = int(lonToArray(top_left_lon,lon_min,lon_resolution))
            Xright = int(lonToArray(top_left_lon,lon_max,lon_resolution))
            Ybottom = int(latToArray(top_left_lat,lat_min,lat_resolution))
            Ytop = int(latToArray(top_left_lat,lat_max,lat_resolution))
            block_sizeX = Xright - Xleft
            block_sizeY = Ybottom - Ytop

            # 以上9行代码用于检验超出栅格剪裁范围的矢量图形，跳过
            createV = 'clipWithShp/sample-' + str(index) + '.shp'  # 新建矢量名称
            out_datasetV = shp_driver.CreateDataSource(createV)
            newlayer = out_datasetV.CreateLayer('test', geom_type=ogr.wkbPolygon, srs=newSpatialRef)
            fieldDefn = ogr.FieldDefn('id', ogr.OFTString)
            fieldDefn.SetWidth(8)
            newlayer.CreateField(fieldDefn)
            featureDefn = newlayer.GetLayerDefn()
            newfeature = ogr.Feature(featureDefn)
            newfeature.SetGeometry(feat.GetGeometryRef())
            newfeature.SetField('id', index)
            newlayer.CreateFeature(newfeature)
            out_datasetV.Destroy()
            indexOfYes.append(index)
            tif_driver = gdal.GetDriverByName("GTiff")
            out_dataset = tif_driver.Create('clipWithShp/sample-'+ str(index) + '.tif', block_sizeX,block_sizeY,bandcount,band1.DataType)
            # top_left_X = lon_min  * lon_resolution
            # top_left_Y = lat_max  * lat_resolution
            # 将计算后的值组装为一个元组，以方便设置
            dst_transform = (lon_min, geotransform[1], geotransform[2], lat_max, geotransform[4],
                             geotransform[5])  # 栅格数据读入时，以左上角为原点，此时ReadAsArray是屏幕坐标，但左上角的经纬度坐标是经度最小值，纬度最大值
            out_dataset.SetGeoTransform(dst_transform)  # 设置裁剪出来图的原点坐标
            out_dataset.SetProjection(projection)  # 设置SRS属性（投影信息）
            # 写入目标文件
            clipWithShp(Xleft,Ytop,out_dataset,bandcount,block_sizeX,block_sizeY)
            del out_dataset
        layer.ResetReading()  # 复位
        shp_dataset.Destroy()
        self.showpanel.append("clipShp success")
        indexOfNo = str(indexOfNo)
        self.showpanel.append(indexOfNo)
        self.showpanel.append("以上序号的矢量文件超出栅格范围无法剪裁")
        indexOfYes = str(indexOfYes)
        self.showpanel.append(indexOfYes)
        self.showpanel.append("以上序号成功剪裁")
        self.clearPoints()


    # def clipWithTxt(self):
    def createShpAndClip(self):
        '''
        主要执行功能：
            用户自行圈定采样位置，并根据用户点击的位置自动生成栅格与矢量配套采样组。
        '''
        self.showpanel.append("当前操作--createShpAndClip，请等待--------------------------------")
        if self.noPictureWarn() == False:
            return

        # 处理异常
        try:
            dataset = gdal.Open(self.path, gdal.GA_ReadOnly)
        except:
            self.showpanel.append("非栅格影像，无法使用该功能")
            return
        if self.noPictureWarn() ==False:
            return
        driver = ogr.GetDriverByName("ESRI Shapefile")  # shp驱动器
        projection = dataset.GetProjection()
        geotransform = dataset.GetGeoTransform()
        top_left_x = geotransform[0]  # 左上角x坐标
        horizon_pixel_resolution = geotransform[1]  # 东西方向像素分辨率
        top_left_y = geotransform[3]  # 左上角y坐标
        vertical_pixel_resolution = geotransform[5]  # 南北方向像素分辨率
        # gdal中的坐标系方式不同于笛卡尔
        # print("地理坐标 = ({}, {})\n像素等级 = ({}, {})\n影像大小 = ({}, {})\n投影= {}".format(top_left_x, top_left_y,horizon_pixel_resolution, vertical_pixel_resolution,dataset.RasterYSize,dataset.RasterXSize, projection))
        band1 = dataset.GetRasterBand(1)
        band2 = dataset.GetRasterBand(2)
        band3 = dataset.GetRasterBand(3)
        # 剪裁框大小
        newSpatialRef = osr.SpatialReference()
        newSpatialRef.ImportFromWkt(projection)
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for x, y in points:
            spatial_top_left_x = top_left_x + x * horizon_pixel_resolution
            spatial_top_left_y = top_left_y + y * vertical_pixel_resolution
            ring.AddPoint(spatial_top_left_x, spatial_top_left_y)
        ring.CloseRings()

        usersdefinedshp = ogr.Geometry(ogr.wkbPolygon)
        usersdefinedshp.AddGeometry(ring)

        usersdefinedshp_extent = usersdefinedshp.GetEnvelope()

        click_points_darray = np.array(points)
        xmin = int(min(click_points_darray[:, 0]))
        xmax = int(max(click_points_darray[:, 0]))
        ymin = int(min(click_points_darray[:, 1]))
        ymax = int(max(click_points_darray[:, 1]))
        self.block_size = int(xmax - xmin)
        self.block_size = int(ymax - ymin)
        self.showpanel.append("envelope:{}".format(usersdefinedshp_extent)+"\nclick_darray:{}".format(click_points_darray)+"\nxmin,xmax,ymin,ymax:{},{},{},{}".format(xmin, xmax, ymin, ymax)+"\nblockx,blocky:{},{}".format(self.block_size, self.block_size))
        #创建矢量
        createV = 'create_shp_clip/sample' + '-' + str(xmin) + '-' + str(ymin) + '.shp'  # 新建矢量名称
        out_datasetV = driver.CreateDataSource(createV)
        newlayer = out_datasetV.CreateLayer('test', geom_type=ogr.wkbPolygon, srs=newSpatialRef)
        fieldDefn = ogr.FieldDefn('id', ogr.OFTString)
        fieldDefn.SetWidth(8)
        newlayer.CreateField(fieldDefn)
        featureDefn = newlayer.GetLayerDefn()
        newfeature = ogr.Feature(featureDefn)
        newfeature.SetGeometry(usersdefinedshp)
        newfeature.SetField('id', str(points[0][0]) + '-' + str(points[0][1]))
        newlayer.CreateFeature(newfeature)
        out_datasetV.Destroy()
        self.showpanel.append("create shp Successfully")
        #创建栅格
        out_band1 = band1.ReadAsArray(xmin, ymin, self.block_size, self.block_size)
        out_band2 = band2.ReadAsArray(xmin, ymin, self.block_size, self.block_size)
        out_band3 = band3.ReadAsArray(xmin, ymin, self.block_size, self.block_size)
        tif_driver = gdal.GetDriverByName("GTiff")
        out_dataset = tif_driver.Create('create_shp_clip/sample' + '-' + str(xmin) + '-' + str(ymin) + '.tif',self.block_size, self.block_size, 3, band1.DataType)
        # 将计算后的值组装为一个元组，以方便设置
        dst_transform = (
            usersdefinedshp_extent[0], geotransform[1], geotransform[2], usersdefinedshp_extent[3], geotransform[4],geotransform[5])
        out_dataset.SetGeoTransform(dst_transform)
        out_dataset.SetProjection(dataset.GetProjection())
        out_dataset.GetRasterBand(1).WriteArray(out_band1)
        out_dataset.GetRasterBand(2).WriteArray(out_band2)
        out_dataset.GetRasterBand(3).WriteArray(out_band3)
        out_dataset.FlushCache()
        del out_dataset
        self.showpanel.append("create shp and clip successful")
        self.clearPoints()
    def clearPoints(self):
        '''
        清除已记录点
        '''
        points.clear()
        self.showpanel.append("采样点已清空")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main = mainGUI()
    Main.show()
    sys.exit(app.exec_())