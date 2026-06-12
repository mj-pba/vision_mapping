# This is the camera feed input manipulation block.
# 1. Initilizing the camera.
# 2. Starting and stopping of the camera.
# 3. Get the camera capture and display the image center point at lable center.
# 4. Display enable and disable the referance cycle.  

import cv2
from PySide6.QtGui import QImage,QPixmap
from PySide6.QtCore import Qt


# First try we use basic webcam type hobby microcope camera to deverlop the software
# Follwoing code is there to use connecting webcam or basic usb camera
# 
class camera_in():
    def __init__(self,ui,index):

        self.ui = ui
        self.cam_id_select = index

        # user select camare index
        #self.ui.cam_id_combo_box.currentIndexChanged.connect(self.camera_select_input)
        #self.cam_id_select = -1 # start condition
        #self.camera = None 

        # Check if hardware acceleration is availabl
        #if cv2.useOptimized():
        #    print("Hardware acceleration is enabled")
        #else:
        #    print("Hardware acceleration is not available")
        self.ui.select_circle_radio_button.toggled.connect(self.update_circle)
        self.draw_circle = True

        self.capture_frame = capture_frame_update() 
        self.frame_update_activation = 1

    # have to start split test

    def update_frame(self):
        
        if self.cam_id_select != -1 and self.frame_update_activation == 1:
            ret, frame = self.capture_frame.capture_frame(self.cam_id_select)
            if ret:
                if self.draw_circle:
                    # cv2.circle(frame, pix_value_center_x, pix_value_center_y, radius, size )
                    cv2.circle(frame, (960, 540), 453, (0, 255, 0), 1)
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert image from BGR to RGB
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.ui.cam_input_lable.setAlignment(Qt.AlignCenter)
                self.ui.cam_input_lable.setPixmap(QPixmap.fromImage(q_image))
                #print(h,w,ch)           # set the image resolution 
            else:
                print("Error: Camara feedback is not avelable")
        else:
            print("Error: Camera not selected")
        # Note: 
        # Need error for camera disconnection, no camera avelable, 




    def update_circle(self, state):
        # Assuming you have a variable self.draw_circle that indicates whether to draw the circle or not
        self.draw_circle = state
        print(self.draw_circle)

    # Get the Camera index value to select the camaera
    #def camera_select_input(self):
    #    self.cam_id_select = int(self.ui.cam_id_combo_box.currentText()) if self.ui.cam_id_combo_box.currentText() else -1
    #
    #    if self.cam_id_select == -1:
    #        print("Camera stopped")
    #        if self.camera:
    #            self.camera.release()
    #            self.camera = None
    #    else:
    #        print("Selected camera ID:", self.cam_id_select)
    #        if self.camera:
    #            self.camera.release()
    #            self.camera = None
        
    #    Need to do something to relesed the previous camera
    #    othersize camera may consume computation. 




class capture_frame_update():
    def __init__(self,index):
        self.camera = None
        self.cam_id_select = index
        self.ret = False
        self.frame = None
        self.frame_update_activation = 1
        pass

    def capture_frame(self):
        if self.cam_id_select != -1 and self.frame_update_activation == 1:
            if self.camera is None:    # we create camera object only one time and use it until index changeed by use
                self.camera = cv2.VideoCapture(self.cam_id_select)
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.ret, self.frame = self.camera.read()
            return self.ret, self.frame
        else:
            return False, self.frame

    def relese_camera(self):
        self.camera.release()
        print("release camera")

    def save_frame(self,filename):
        # self.frame_update_activation = 0 # to stop displaying the camara feedback in update frame
        print(self.cam_id_select)
        if self.cam_id_select != -1:
            if self.camera is None:    # we create camera object only one time and use it until index changeed by use
                self.camera = cv2.VideoCapture(self.cam_id_select)
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.ret, self.frame = self.camera.read()
            if self.ret:
                print(filename)
                cv2.imwrite(filename, self.frame)
            else:
                print("ret is none")
        # self.frame_update_activation = 1

        return True