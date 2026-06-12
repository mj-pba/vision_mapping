1# -- coding: utf-8 --

import sys
from ctypes import *
import datetime
import numpy
import cv2
import gc
import os
from PySide6.QtGui import QImage,QPixmap
from PySide6.QtCore import Qt

#sys.path.append(r"../MVSDK")
cwd = os.getcwd()
folder_path = os.path.join(cwd, r'src\backend\image_processing\dahua_cam_api\MVSDK')
sys.path.append(folder_path)

from IMVApi import *


# Second try is to use industril camera
# Use1

class camera_frame_update():
    def __init__(self,index):

        self.cam_id_select = index # start condition
        self.capture_frame_activation = 1

        pass

    def displayDeviceInfo(self,deviceInfoList):  
        print("Idx  Type   Vendor              Model           S/N                 DeviceUserID    IP Address")
        print("------------------------------------------------------------------------------------------------")
        for i in range(0,deviceInfoList.nDevNum):
            pDeviceInfo=deviceInfoList.pDevInfo[i]
            strType=""
            strVendorName=""
            strModeName = ""
            strSerialNumber=""
            strCameraname=""
            strIpAdress=""
            for str in pDeviceInfo.vendorName:
                strVendorName = strVendorName + chr(str)
            for str in pDeviceInfo.modelName:
                strModeName = strModeName + chr(str)
            for str in pDeviceInfo.serialNumber:
                strSerialNumber = strSerialNumber + chr(str)
            for str in pDeviceInfo.cameraName:
                strCameraname = strCameraname + chr(str)
            for str in pDeviceInfo.DeviceSpecificInfo.gigeDeviceInfo.ipAddress:
                    strIpAdress = strIpAdress + chr(str)
            if pDeviceInfo.nCameraType == typeGigeCamera:
                strType="Gige"
            elif pDeviceInfo.nCameraType == typeU3vCamera:
                strType="U3V"
            print ("[%d]  %s   %s    %s      %s     %s           %s" % (i+1, strType,strVendorName,strModeName,strSerialNumber,strCameraname,strIpAdress))


    def camera_connect_input(self):
        #self.cam_input_index = cam_input_index
        deviceList=IMV_DeviceList()
        interfaceType=IMV_EInterfaceType.interfaceTypeAll
        stRecordParam=IMV_RecordParam()

        nWidth=c_uint()
        nHeight=c_uint()

        # 枚举设备
        nRet=MvCamera.IMV_EnumDevices(deviceList,interfaceType)
        if IMV_OK != nRet:
            print("Enumeration devices failed! ErrorCode",nRet)
            sys.exit()
        if deviceList.nDevNum == 0:
            print ("find no device!")
            sys.exit()

        print("deviceList size is",deviceList.nDevNum)

        #display list details 
        #self.displayDeviceInfo(deviceList)
        
        # get the input from user    # We are getting the data cam id before starting this so we dont need above section 
        #nConnectionNum = input("Please input the camera index: ")
        
        # assing self.cam_id_select to nConnectionNum
        self.nConnectionNum = self.cam_id_select

        if int(self.nConnectionNum) > deviceList.nDevNum:
            print ("intput error!")
            #sys.exit()
        else:
            print(self.nConnectionNum)

        # continue to create camera instance
        self.cam=MvCamera()
        # 创建设备句柄
        nRet=self.cam.IMV_CreateHandle(IMV_ECreateHandleMode.modeByIndex,byref(c_void_p(int(self.nConnectionNum)-1)))
        if IMV_OK != nRet:
            print("Create devHandle failed! ErrorCode",nRet)
            sys.exit()

        # 打开相机
        nRet=self.cam.IMV_Open()
        if IMV_OK != nRet:
            print("Open devHandle failed! ErrorCode",nRet)
            sys.exit()

       # 通用属性设置:设置触发模式为off
        nRet=IMV_OK
        nRet=self.cam.IMV_SetEnumFeatureSymbol("TriggerSource","Software")
        if IMV_OK != nRet:
            print("Set triggerSource value failed! ErrorCode[%d]" % nRet)
            sys.exit()

        nRet=self.cam.IMV_SetEnumFeatureSymbol("TriggerSelector","FrameStart")
        if IMV_OK != nRet:
            print("Set triggerSelector value failed! ErrorCode[%d]" % nRet)
            sys.exit()

        nRet=self.cam.IMV_SetEnumFeatureSymbol("TriggerMode","Off")
        if IMV_OK != nRet:
            print("Set triggerMode value failed! ErrorCode[%d]" % nRet)
            sys.exit()

        # 开始拉流
        nRet=self.cam.IMV_StartGrabbing()
        if IMV_OK != nRet:
            print("Start grabbing failed! ErrorCode",nRet)
            sys.exit()

        print("cam setup finished")


    def capture_frame(self):
        #isGrab = True

        if self.capture_frame_activation == 1:
            # 主动取图
            frame = IMV_Frame()
            stPixelConvertParam=IMV_PixelConvertParam()

            nRet = self.cam.IMV_GetFrame(frame, 1000)

            if  IMV_OK != nRet :
                print("getFrame fail! Timeout:[1000]ms")
                #continue
            #else:
                #print("getFrame success BlockId = [" + str(frame.frameInfo.blockId) + "], get frame time: " + str(datetime.datetime.now()))

            if  None==byref(frame) :
                print("pFrame is NULL!")
                #continue

            # 给转码所需的参数赋值
            # Assign values ​​to the parameters required for transcoding

            if IMV_EPixelType.gvspPixelMono8==frame.frameInfo.pixelFormat:
                nDstBufSize=frame.frameInfo.width * frame.frameInfo.height
            else:
                nDstBufSize=frame.frameInfo.width * frame.frameInfo.height*3

            pDstBuf=(c_ubyte*nDstBufSize)()
            memset(byref(stPixelConvertParam), 0, sizeof(stPixelConvertParam))

            stPixelConvertParam.nWidth = frame.frameInfo.width
            stPixelConvertParam.nHeight = frame.frameInfo.height
            stPixelConvertParam.ePixelFormat = frame.frameInfo.pixelFormat
            stPixelConvertParam.pSrcData = frame.pData
            stPixelConvertParam.nSrcDataLen = frame.frameInfo.size
            stPixelConvertParam.nPaddingX = frame.frameInfo.paddingX
            stPixelConvertParam.nPaddingY = frame.frameInfo.paddingY
            stPixelConvertParam.eBayerDemosaic = IMV_EBayerDemosaic.demosaicNearestNeighbor
            stPixelConvertParam.eDstPixelFormat = frame.frameInfo.pixelFormat
            stPixelConvertParam.pDstBuf = pDstBuf
            stPixelConvertParam.nDstBufSize = nDstBufSize

            # 释放驱动图像缓存
            # release frame resource at the end of use

            nRet = self.cam.IMV_ReleaseFrame(frame)
            if IMV_OK != nRet:
                print("Release frame failed! ErrorCode[%d]\n", nRet)
                sys.exit()

            # 如果图像格式是 Mono8 直接使用
            # no format conversion required for Mono8

            if stPixelConvertParam.ePixelFormat == IMV_EPixelType.gvspPixelMono8:
                imageBuff=stPixelConvertParam.pSrcData
                userBuff = c_buffer(b'\0', stPixelConvertParam.nDstBufSize)

                memmove(userBuff,imageBuff, stPixelConvertParam.nDstBufSize)
                grayByteArray = bytearray(userBuff)

                cvImage = numpy.array(grayByteArray).reshape(stPixelConvertParam.nHeight, stPixelConvertParam.nWidth)

            else:
                # 转码 => BGR24
                # convert to BGR24
                stPixelConvertParam.eDstPixelFormat=IMV_EPixelType.gvspPixelBGR8
                #stPixelConvertParam.nDstBufSize=nDstBufSize

                nRet=self.cam.IMV_PixelConvert(stPixelConvertParam)
                if IMV_OK!=nRet:
                    print("image convert to failed! ErrorCode[%d]" % nRet)
                    del pDstBuf
                    sys.exit()
                rgbBuff = c_buffer(b'\0', stPixelConvertParam.nDstBufSize)
                memmove(rgbBuff,stPixelConvertParam.pDstBuf, stPixelConvertParam.nDstBufSize)
                colorByteArray = bytearray(rgbBuff)
                cvImage = numpy.array(colorByteArray).reshape(stPixelConvertParam.nHeight, stPixelConvertParam.nWidth, 3)
                if None!=pDstBuf:
                    del pDstBuf
                    pass


            gc.collect()    
            ret = True
            return ret, cvImage


        
    

    def relese_camera(self):    
        # 停止拉流
        nRet=self.cam.IMV_StopGrabbing()
        if IMV_OK != nRet:
            print("Stop grabbing failed! ErrorCode",nRet)
            sys.exit()
        # 关闭相机
        nRet=self.cam.IMV_Close()
        if IMV_OK != nRet:
            print("Close camera failed! ErrorCode",nRet)
            sys.exit()
        # 销毁句柄
        if(self.cam.handle):
            nRet=self.cam.IMV_DestroyHandle()
        print("---Demo end---")



    def save_frame(self, full_file_path):
        self.capture_frame_activation = 0
        print(full_file_path)

        # capture frame and save
        frame = IMV_Frame()
        stPixelConvertParam=IMV_PixelConvertParam()

        nRet = self.cam.IMV_GetFrame(frame, 1000)

        if  IMV_OK != nRet :
            print("getFrame fail! Timeout:[1000]ms")
            #continue
        #else:
            #print("getFrame success BlockId = [" + str(frame.frameInfo.blockId) + "], get frame time: " + str(datetime.datetime.now()))

        if  None==byref(frame) :
            print("pFrame is NULL!")
            #continue

        # 给转码所需的参数赋值
        # Assign values ​​to the parameters required for transcoding

        if IMV_EPixelType.gvspPixelMono8==frame.frameInfo.pixelFormat:
            nDstBufSize=frame.frameInfo.width * frame.frameInfo.height
        else:
            nDstBufSize=frame.frameInfo.width * frame.frameInfo.height*3

        pDstBuf=(c_ubyte*nDstBufSize)()
        memset(byref(stPixelConvertParam), 0, sizeof(stPixelConvertParam))

        stPixelConvertParam.nWidth = frame.frameInfo.width
        stPixelConvertParam.nHeight = frame.frameInfo.height
        stPixelConvertParam.ePixelFormat = frame.frameInfo.pixelFormat
        stPixelConvertParam.pSrcData = frame.pData
        stPixelConvertParam.nSrcDataLen = frame.frameInfo.size
        stPixelConvertParam.nPaddingX = frame.frameInfo.paddingX
        stPixelConvertParam.nPaddingY = frame.frameInfo.paddingY
        stPixelConvertParam.eBayerDemosaic = IMV_EBayerDemosaic.demosaicNearestNeighbor
        stPixelConvertParam.eDstPixelFormat = frame.frameInfo.pixelFormat
        stPixelConvertParam.pDstBuf = pDstBuf
        stPixelConvertParam.nDstBufSize = nDstBufSize

        # 释放驱动图像缓存
        # release frame resource at the end of use

        nRet = self.cam.IMV_ReleaseFrame(frame)
        if IMV_OK != nRet:
            print("Release frame failed! ErrorCode[%d]\n", nRet)
            sys.exit()

        # 如果图像格式是 Mono8 直接使用
        # no format conversion required for Mono8

        if stPixelConvertParam.ePixelFormat == IMV_EPixelType.gvspPixelMono8:
            imageBuff=stPixelConvertParam.pSrcData
            userBuff = c_buffer(b'\0', stPixelConvertParam.nDstBufSize)

            memmove(userBuff,imageBuff, stPixelConvertParam.nDstBufSize)
            grayByteArray = bytearray(userBuff)

            cvImage = numpy.array(grayByteArray).reshape(stPixelConvertParam.nHeight, stPixelConvertParam.nWidth)

        else:
            # 转码 => BGR24
            # convert to BGR24
            stPixelConvertParam.eDstPixelFormat=IMV_EPixelType.gvspPixelBGR8
            #stPixelConvertParam.nDstBufSize=nDstBufSize

            nRet=self.cam.IMV_PixelConvert(stPixelConvertParam)
            if IMV_OK!=nRet:
                print("image convert to failed! ErrorCode[%d]" % nRet)
                del pDstBuf
                sys.exit()
            rgbBuff = c_buffer(b'\0', stPixelConvertParam.nDstBufSize)
            memmove(rgbBuff,stPixelConvertParam.pDstBuf, stPixelConvertParam.nDstBufSize)
            colorByteArray = bytearray(rgbBuff)
            cvImage = numpy.array(colorByteArray).reshape(stPixelConvertParam.nHeight, stPixelConvertParam.nWidth, 3)
            if None!=pDstBuf:
                del pDstBuf
                pass

        cv2.imwrite(full_file_path, cvImage)
        gc.collect()    

        self.capture_frame_activation = 1

