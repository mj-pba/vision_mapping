from backend.motor_control.acs_python_modules import get_axis_parameters
from backend.motor_control.acs_python_modules import set_axis_perameters
from backend.motor_control.acs_python_modules import motor_activation
from backend.motor_control.acs_python_modules import control_all_axis


class axis_z_ui_controller:
    def __init__(self,ui):
        self.ui = ui #pass the ui instance to the controller

        # Axis X select
        self.ui.select_axis_z_combo_box.currentIndexChanged.connect(self.handle_axis_z_input_select)
        self.axis_z_updater_start_stop(0)  # to create update function activate variables & getting ready to update


        # Object for acs python class of update axis parameters
        self.get_axis_z_parameter = get_axis_parameters()   # object for read values from acs update parameters
        self.axis_z_fpos = 0
        self.axis_z_velocity = 0                            # Velocity varible from ACS and user input
        self.axis_z_acceleration = 0
        self.axis_z_deceleration = 0
        self.axis_z_kill_deceleration = 0
        self.axis_z_jerk = 0
        self.axis_z_motor_state = 0
        
        # Set axis values function 
        self.set_axis_z_parameters = set_axis_perameters()  # object to set values to ACS
        
        # get the absolute motion next point 
        self.ui.axis_z_set_position_line_edit.editingFinished.connect(self.axis_z_set_position_line_edit_finished)
        
        # update (SetVelocity) velocity to ACS controller on display current value 
        self.ui.axis_z_velocity_line_edit.cursorPositionChanged.connect(self.axis_z_velocity_line_edit_cursor_position)
        self.axis_z_velocity_le_cursor_position = -1         # Use to stop velcoity update
        self.ui.axis_z_velocity_line_edit.editingFinished.connect(self.axis_z_velocity_line_edit_editing_finished)
        
        # update (SetAcceleration) 
        self.ui.axis_z_acceleration_line_edit.cursorPositionChanged.connect(self.axis_z_acceleration_line_edit_cursor_position)
        self.axis_z_acceleration_line_edit_cursor_position = -1 
        self.ui.axis_z_acceleration_line_edit.editingFinished.connect(self.axis_z_acceleration_line_edit_editing_finished)

        # update (SetDeceleration) 
        self.ui.axis_z_deceleration_line_edit.cursorPositionChanged.connect(self.axis_z_deceleration_line_edit_cursor_position)
        self.axis_z_deceleration_line_edit_cursor_position = -1
        self.ui.axis_z_deceleration_line_edit.editingFinished.connect(self.axis_z_deceleration_line_edit_editing_finished)

        #update (SetKillDeceleraion)
        self.ui.axis_z_kill_deceleration_line_edit.cursorPositionChanged.connect(self.axis_z_kill_deceleration_line_edit_cursor_position)
        self.axis_z_kill_deceleration_line_edit_cursor_position = -1
        self.ui.axis_z_kill_deceleration_line_edit.editingFinished.connect(self.axis_z_kill_deceleration_line_edit_editing_finished)

        # update (SetJerk)
        self.ui.axis_z_jerk_line_edit.cursorPositionChanged.connect(self.axis_z_jerk_line_edit_cursor_position)
        self.axis_z_jerk_line_edit_cursor_position = -1
        self.ui.axis_z_jerk_line_edit.editingFinished.connect(self.axis_z_jerk_line_edit_editing_finished)

        # motor start stop button 
        self.ui.axis_z_motion_start_button.clicked.connect(self.axis_z_motion_start_button_clicked)

        # enable motor
        self.axis_z_motor_activation = motor_activation()
        self.ui.axis_z_enable_button.clicked.connect(self.axis_z_enable_button_clicked)
        
        # emergency stop button 
        self.all_axis_control = control_all_axis()
        self.ui.emergency_stop_button.clicked.connect(self.emergency_stop_button_clicked)

        pass

    def set_communication(self,hc):
        self.hc = hc
        # print("hc", hc)
        if self.hc == -1:
            self.axis_z_updater_start_stop(0)
        #print("axis",self.axis)

    ## Note: The process of the functional block diagram of the bellow operation is explaned in backend/README.md file.
    ## Select axis
    def handle_axis_z_input_select(self):
        self.axis_z_select = self.ui.select_axis_z_combo_box.currentText()  # get the edited
        #print(self.axis_z_select)
        if self.axis_z_select == '':        # If user selected the very first "None" item
            # print("select axis and contiue")
            # STOP AXIS UPDATE 
            self.axis_z_updater_start_stop(0)               # Updater stop
            self.axis_z_select = -1
        else:                                               # If user serlect any other value
            self.axis_z_updater_start_stop(1)               # Updater start
            self.axis_z_select = int(self.axis_z_select)    # convert selected axis to int
            

      ## Errors: If user selcted axis which are defined in the software but not in the controller, there will be some errors.
      ## to address that some cousetions have to take.     

    def send_axis_select(self):
        return self.axis_z_select



    ## setting up next motion position
    def axis_z_set_position_line_edit_finished(self):
        self.axis_z_set_position = self.ui.axis_z_set_position_line_edit.text()
        # print("get the next position")
    # We need to have max posisiton limits
    # We need to hav mil mosition limits
    
    ## Axis enable
    def axis_z_enable_button_clicked(self):
        self.axis_z_motor_enable_status_updater_activation = 0
        
        if self.axis_z_motor_state == 0:
            ts = self.axis_z_motor_activation.enable(self.hc, int(self.axis_z_select))
            print("Enable errors: ",ts)

        elif self.axis_z_motor_state == 1:
            ts = self.axis_z_motor_activation.disable(self.hc, int(self.axis_z_select))
            print("Disable error: ",ts)

        self.axis_z_motor_enable_status_updater_activation = 1
    

    ## Axis x velocity update controller and getting user input
    def axis_z_velocity_line_edit_cursor_position(self):
        self.axis_z_velocity_le_cursor_position = self.ui.axis_z_velocity_line_edit.cursorPosition()
    ## editing finished
    def axis_z_velocity_line_edit_editing_finished(self):   
        self.axis_z_velocity = self.ui.axis_z_velocity_line_edit.text() # get the value from the and send to ACS
        self.set_axis_z_parameters.axis_velocity(self.hc, int(self.axis_z_select), float(self.axis_z_velocity))
        self.axis_z_velocity_le_cursor_position = -1                # set axis curser position to -1

    ## Axis x accleration update controller and getting user input
    def axis_z_acceleration_line_edit_cursor_position(self):
        self.axis_z_acceleration_line_edit_cursor_position = self.ui.axis_z_acceleration_line_edit.cursorPosition()
    # editing finished
    def axis_z_acceleration_line_edit_editing_finished(self):
        self.axis_z_acceleration = self.ui.axis_z_acceleration_line_edit.text() #get value
        self.set_axis_z_parameters.axis_acceleration(self.hc,int(self.axis_z_select),float(self.axis_z_acceleration)) # send to acs
        self.axis_z_acceleration_line_edit_cursor_position = -1
    
    ## Axis x deceleration update control and getting user inputs
    def axis_z_deceleration_line_edit_cursor_position(self):
        self.axis_z_deceleration_line_edit_cursor_position = self.ui.axis_z_deceleration_line_edit.cursorPosition()
    # editing finished
    def axis_z_deceleration_line_edit_editing_finished(self):
        self.axis_z_deceleration = self.ui.axis_z_deceleration_line_edit.text()
        self.set_axis_z_parameters.axis_deceleration(self.hc,int(self.axis_z_select),float(self.axis_z_deceleration))
        self.axis_z_deceleration_line_edit_cursor_position = -1

    ## Axis x deceleration update control and getting user inputs
    def axis_z_kill_deceleration_line_edit_cursor_position(self):
        self.axis_z_kill_deceleration_line_edit_cursor_position = self.ui.axis_z_kill_deceleration_line_edit.cursorPosition()
    # editing finished
    def axis_z_kill_deceleration_line_edit_editing_finished(self):
        self.axis_z_kill_deceleration = self.ui.axis_z_kill_deceleration_line_edit.text()
        self.set_axis_z_parameters.axis_kill_deceleration(self.hc,int(self.axis_z_select),float(self.axis_z_kill_deceleration))
        self.axis_z_kill_deceleration_line_edit_cursor_position = -1

    ## Axis x deceleration update control and getting user inputs
    def axis_z_jerk_line_edit_cursor_position(self):
        self.axis_z_jerk_line_edit_cursor_position = self.ui.axis_z_jerk_line_edit.cursorPosition()
    # editing finished
    def axis_z_jerk_line_edit_editing_finished(self):
        self.axis_z_jerk = self.ui.axis_z_jerk_line_edit.text()
        self.set_axis_z_parameters.axis_jerk(self.hc,int(self.axis_z_select),float(self.axis_z_jerk))
        self.axis_z_jerk_line_edit_cursor_position = -1

    def axis_z_motion_start_button_clicked(self):
        self.axis_z_set_position_line_edit_finished()
        #print("move to ",self.axis_z_set_position)
        if self.axis_z_motor_state == 1:
            tc = self.axis_z_motor_activation.absolute_motion(self.hc, int(self.axis_z_select), float(self.axis_z_set_position))
            print(tc)
            ### Note: need to setup errors based on tc
        else: 
            print("motor on disable state error")

    # emergency stop button to stop all motors
    def emergency_stop_button_clicked(self):
        self.all_axis_control.desable_all(self.hc)



## Axis parameter Updater 
    ## X axis Updater  control function
    def axis_z_updater_start_stop(self,value):     
        if value == 1 and self.hc != -1:                                # 
            self.axis_z_position_feedback_updater_activation = 1
            self.axis_z_position_error_updater_activation = 1
            self.axis_z_motor_enable_status_updater_activation = 1
            self.axis_z_enable_updater_activation = 1
            self.axis_z_velocity_parameter_updater_activation = 1       # parameter upate function start 
            self.axis_z_acceleration_parameter_updater_activation = 1   # parameter upate function start
            self.axis_z_deceleration_parameter_updater_activation = 1
            self.axis_z_kill_deceleration_parameter_updater_activation = 1
            self.axis_z_jerk_parameter_updater_activation = 1
            
        else:
            self.axis_z_position_feedback_updater_activation = 0
            self.axis_z_position_error_updater_activation = 0
            self.axis_z_motor_enable_status_updater_activation = 0
            self.axis_z_enable_updater_activation = 0
            self.axis_z_velocity_parameter_updater_activation = 0
            self.axis_z_acceleration_parameter_updater_activation = 0
            self.axis_z_deceleration_parameter_updater_activation = 0
            self.axis_z_kill_deceleration_parameter_updater_activation = 0
            self.axis_z_jerk_parameter_updater_activation = 0

     ## Updater function
    def axis_z_update_parameters(self):
        if self.axis_z_position_feedback_updater_activation == 1:
            #get fpos from ACS and reformt to show only 4 decimle points
            self.axis_z_fpos = "{:.6f}".format(self.get_axis_z_parameter.axis_fpos(self.hc,int(self.axis_z_select)))
            self.ui.axis_z_fpos_lable.setText(str(self.axis_z_fpos))

        if self.axis_z_position_error_updater_activation == 1:
            self.axis_z_position_error = self.get_axis_z_parameter.axis_pe(self.hc,self.axis_z_select)
            self.ui.axis_z_position_error.setText(str(self.axis_z_position_error))

        if self.axis_z_motor_enable_status_updater_activation == 1:
            # get MFLAG(axis).0 from acs
            self.axis_z_motor_state = int(self.axis_z_motor_activation.state(self.hc, str(self.axis_z_select)))
            if self.axis_z_motor_state == 1:
                self.ui.axis_z_enable_button.setText("Disable")
                self.ui.axis_z_enable_button.setStyleSheet("background-color: #B1F7A6 ")
            if self.axis_z_motor_state ==0:
                self.ui.axis_z_enable_button.setText("Enable")
                self.ui.axis_z_enable_button.setStyleSheet("background-color: light gray ")

        if self.axis_z_velocity_parameter_updater_activation == 1 and self.axis_z_velocity_le_cursor_position == -1:
            self.axis_z_velocity = self.get_axis_z_parameter.axis_velocity(self.hc,int(self.axis_z_select)) # get velocity from ACS
            self.ui.axis_z_velocity_line_edit.setText(str(self.axis_z_velocity)) # update value in UI
            self.axis_z_velocity_le_cursor_position = -1 # Reset the axis velocity line edit cursor positon

        if self.axis_z_acceleration_parameter_updater_activation == 1 and self.axis_z_acceleration_line_edit_cursor_position == -1:
            self.axis_z_acceleration = self.get_axis_z_parameter.axis_acceleration(self.hc, int(self.axis_z_select))    # get value
            self.ui.axis_z_acceleration_line_edit.setText(str(self.axis_z_acceleration))                                # update value
            self.axis_z_acceleration_line_edit_cursor_position = -1                                                    # reset couser position

        if self.axis_z_deceleration_parameter_updater_activation == 1 and self.axis_z_deceleration_line_edit_cursor_position == -1:
            self.axis_z_deceleration = self.get_axis_z_parameter.axis_deceleration(self.hc, int(self.axis_z_select))
            self.ui.axis_z_deceleration_line_edit.setText(str(self.axis_z_deceleration))
            self.axis_z_deceleration_line_edit_cursor_position = -1

        if self.axis_z_kill_deceleration_parameter_updater_activation == 1 and self.axis_z_kill_deceleration_line_edit_cursor_position == -1:
            self.axis_z_kill_deceleration = self.get_axis_z_parameter.axis_kill_deceleration(self.hc, int(self.axis_z_select))
            self.ui.axis_z_kill_deceleration_line_edit.setText(str(self.axis_z_kill_deceleration))
            self.axis_z_kill_deceleration_line_edit_cursor_position = -1

        if self.axis_z_jerk_parameter_updater_activation == 1 and self.axis_z_jerk_line_edit_cursor_position == -1:
            self.axis_z_jerk = self.get_axis_z_parameter.axis_jerk(self.hc, int(self.axis_z_select))
            self.ui.axis_z_jerk_line_edit.setText(str(self.axis_z_jerk))    
            self.axis_z_jerk_line_edit_cursor_position = -1
        
        
