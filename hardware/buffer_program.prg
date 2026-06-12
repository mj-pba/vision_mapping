#/ Controller version = 3.13.01
#/ Date = 7/14/2025 12:28 PM
#/ User remarks = 
#0
!PNAME=Homing X
!PDESC=
! ACS inbuild homing
! homing method is 

!HOME Axis, [HomingMethod, HomingVel, MaxDistance, HomingOffset, HomingCurrLimit, HardStopThreshold,SetYawToOpen, SkewValue,LookForTwoLS, LookForTwoIndexes, Timeout]


INT AXIS = 0
ENABLE AXIS 

HOME AXIS, 50, 5,160,0

STOP
#1
!PNAME=Homing Y
!PDESC=
! ACS inbuild homing
! homing method is 

!HOME Axis, [HomingMethod, HomingVel, MaxDistance, HomingOffset, HomingCurrLimit, HardStopThreshold,SetYawToOpen, SkewValue,LookForTwoLS, LookForTwoIndexes, Timeout]


INT AXIS = 1
ENABLE AXIS 

HOME AXIS, 50, 5,160,0

STOP
#2
!PNAME=Homing Z
!PDESC=
!!!!!!!!!!!!!!!!!!!!!!!!!!Z AXIS HOMING
int Slave_Number,Axis,Touch_Probe_Status, limit_speed, index_speed
real Index_Position

!initialize variables
Slave_Number= 2
Axis=2
limit_speed = 5
index_speed = 1

ERRORMAPOFF Axis, 0

!set motion paramters for homing
VEL(Axis) = 1
ACC(Axis) = 10
DEC(Axis) = 10
JERK(Axis) = 10
KDEC(Axis) = 1

!disable default limit response
FMASK(Axis).#LL = 0
FMASK(Axis).#RL = 0
wait 500
FMASK(Axis).#LL = 1
FMASK(Axis).#RL = 1

FDEF(Axis).#RL = 0
FDEF(Axis).#LL = 0
!enable default connection
MFLAGS(Axis).#DEFCON =1

enable (Axis)

!reset touchprobe function
coewrite/2 (Slave_Number,0x60B8,0,0)

wait 200
ACC(Axis) = 1000
DEC(Axis) = 1000
JERK(Axis) = 50000
KDEC(Axis) = 50000
!move in - dir till RL 
jog/v Axis, -limit_speed
while (IN(Slave_Number).17)
!wait 5
end
kill Axis
till ^MST(Axis).#MOVE
WAIT 1000
!enable touch probe function
coewrite/2 (Slave_Number,0x60B8,0,21)
Touch_Probe_Status=coeread/2 (Slave_Number,0x60B9,0)
WAIT 500
!move in + direction till index
jog/v Axis,index_speed
while ^(Touch_Probe_Status=67)
Touch_Probe_Status=coeread/2 (Slave_Number,0x60B9,0)
if (Touch_Probe_Status = 67)
HALT Axis
!kill Axis
SET FPOS(Axis) = 0
end
end

!enable default limit response
FDEF(Axis).#RL = 1
FDEF(Axis).#LL = 1
wait 200


Index_Position=coeread/4 (Slave_Number,0x60BA,0)
!set FPOS(Axis)= (ActualPos_MT(Axis) - Index_Position)/10000+18



!set default motion paramters for
VEL(Axis) = 1
ACC(Axis) = 100
DEC(Axis) = 100
JERK(Axis) = 1000
KDEC(Axis) = 5000

!travel to 0 position
ptp/ev Axis, 0, 5

Z_Mapping_Done = 0
start 13,1
till Z_Mapping_Done

Z_homing_done = 1

stop


#3
!PNAME=Tuning X and Y
!PDESC=
! Tunining parameters for each objects
! MalithJKD

!------ Bottom axis ----!

VEL(0) 	= 5
ACC(0) 	= 500
DEC(0) 	= 500 
JERK(0)	= 5000

SLIKI(0)	= 16150	! 
SLIKP(0)	= 722

SLPKP(0)	= 90
SLVKP(0)	= 400
SLVKI(0)	= 2000!600

MFLAGS(0).#NOFILT = 0 
SLVSOF(0)	= 1200
SLVSOFD(0)	= 0.707

MFLAGS(0).#NOTCH = 1
SLVNATT(0)	= 3.88832
SLVNFRQ(0)	= 287.5
SLVNWID(0)	= 64

MFLAGS(0).#BI_QUAD = 0
SLVB0DD(0)	= 0.707
SLVB0DF(0)	= 400
SLVB0ND(0)	= 0.7
SLVB0NF(0)	= 300

MFLAGS(0).#BI_QUAD1 = 0
SLVB1DD(0)	= 0.707
SLVB1DF(0)	= 400
SLVB1ND(0)	= 0.707
SLVB1NF(0)	= 300

SLAFF(0)	= 20
SLJFF(0)	= 0
SLSFF(0)	= 0

SETTLE(0)	= 1
TARGRAD(0)	= 5E-6		! Target is 40 nm 


!------ Top Axis ------!

VEL(1) 	= 5
ACC(1) 	= 500 
DEC(1) 	= 500 
JERK(1)	= 5000

SLIKI(1)	= 19000 ! 
SLIKP(1)	= 530

SLPKP(1)	= 120
SLVKP(1)	= 230
SLVKI(1)	= 2000!950

MFLAGS(1).#NOFILT =0 
SLVSOF(1)	= 950
SLVSOFD(1)	= 0.707

MFLAGS(1).#NOTCH	= 1
SLVNATT(1)	= 2.78887
SLVNFRQ(1)	= 374.7
SLVNWID(1)	= 146.7

MFLAGS(1).#BI_QUAD = 0
SLVB0DD(1)	= 0.707
SLVB0DF(1)	= 400
SLVB0ND(1)	= 0.707
SLVB0NF(1)	= 300

MFLAGS(1).#BI_QUAD1 = 0
SLVB1DD(1)	= 0.707
SLVB1DF(1)	= 400
SLVB1ND(1)	= 0.707
SLVB1NF(1)	= 300

SLAFF(1)	= 25.51
SLJFF(1)	= 0
SLSFF(1)	= 0

SETTLE(1)	= 0
TARGRAD(1)	= 5E-6		! Target is 40 nm 

STOP
#4
!PNAME=Z Stetup
!PDESC=
INT AXIS 

AXIS = 2

DISABLE AXIS

EFAC(AXIS) = 10E-5 ! covert count to mm	
XVEL(AXIS) = 50 ! max speed
XACC(AXIS) = 500 ! max acc
JERK(AXIS) = 500 ! jerk
CERRI(AXIS) = 1 ! idle error
CERRA(AXIS) = 5 ! acc error
CERRV(AXIS) = 2 ! constant speed error
!TARGRAD(AXIS)= 0.001?
!SETTLE(AXIS)=?10

STOP
#8
!PNAME=Thermal sensor mapping
!PDESC=
! Setup temparature sensors
! Zhang Song 
! 2024.09.04

! To start auto exiculte while switching on the motor 
! AUTOEXEC:

! Define values 
int TempRep_offset_1,TempRep_offset_2,TempRep_offset_3, TempRep_offset_4, Device

! Node or device from ACS network or #ETHERCAT command
Device = 3

! get the "offset" value from "netowrk valriable name"
DISP " MAPPING TEMPRATURE SENSOR..."
TempRep_offset_1 = ECGETOFFSET("Input(s).Channel 1, Word 1", Device)  !#ETHERCAT 285
TempRep_offset_2 = ECGETOFFSET("Input(s).Channel 2, Word 1", Device)
TempRep_offset_3 = ECGETOFFSET("Input(s).Channel 3, Word 1", Device)
TempRep_offset_4 = ECGETOFFSET("Input(s).Channel 4, Word 1", Device)

! Actual mapping of the offset value to globally accesible variable 
ecin(TempRep_offset_1, Temparature_sensor_1)
ecin(TempRep_offset_2, Temparature_sensor_2)
ecin(TempRep_offset_3, Temparature_sensor_3)
ecin(TempRep_offset_4, Temparature_sensor_4)

!DISP TempRep_offset_1
!disp "TempRep: ", Temparature_sensor_1, Temparature_sensor_2,Temparature_sensor_3 

DISP " MAPPING TEMPRATURE SENSOR FINISHED."

STOP
#A
!PNAME=
!PDESC=
!axisdef X=0,Y=1,Z=2,T=3,A=4,B=5,C=6,D=7
!axisdef x=0,y=1,z=2,t=3,a=4,b=5,c=6,d=7
global int I(100),I0,I1,I2,I3,I4,I5,I6,I7,I8,I9,I90,I91,I92,I93,I94,I95,I96,I97,I98,I99
global int ActualPos_MT1, ActualPos_MT2, ActualPos_MT3, Axis_2
global int ActualPos_MT(3)
global int ActualCurrent_MT(1)
global real V(100),V0,V1,V2,V3,V4,V5,V6,V7,V8,V9,V90,V91,V92,V93,V94,V95,V96,V97,V98,V99

AXISDEF AXIS_Y=1, AXIS_X=0, AXIS_Z=2
global real static CORRECTION_MAP0(11), CORRECTION_MAP1(11)
global real static CORRECTION_MAPX2(5)(5), CORRECTION_MAPY2(5)(5), CORRECTION_MAP2(11)

global int ControlWord_MT1, ControlWord_MT2, ControlWord_MT3
global int const noOfAxis = 3

global int actual_current, actual_current_status
global int wago_input_value_1,wago_input_value_2,wago_input_value_3,wago_input_value_4
global int wago_input_value_5,wago_input_value_6,wago_input_value_7,wago_input_value_8

global int X_Mapping_Done, Y_Mapping_Done, Z_Mapping_Done 

global int Fault_clearing_done
global int X_homing_done, Y_homing_done, Z_homing_done
GLOBAL INT PT1000_4_WIRE_1,PT100_4WIRE,PT1000_4_WIRE_2,PT100_2_WIRE

global REAL LOCATION_0(24)(24)
global REAL LOCATION_1(24)(24)
global real TempRep, Temparature_sensor_1,Temparature_sensor_2, Temparature_sensor_3, Temparature_sensor_4

!vgv


global static REAL CorrectionMap2(15)


global static real Map1_correctionTable(76)(76);
global static real Map1_refAxis0_positions(76)
global static real Map1_refAxis1_positions(76)

global static real Map2_correctionTable(76)(76);
global static real Map2_refAxis0_positions(76)
global static real Map2_refAxis1_positions(76)

