#!/usr/bin/env python


import pyads
import rospy
from TwincatData import ADSConnection
from sensor_msgs.msg import JointState

class BridgeTwincat:

    def __init__(self,ams_net_id: str = "127.0.0.1.1.1",
        ams_net_port: int = 350,
        ip_address: str = None,
        ):
    
        #connect to twincat project
        self.adsConnection = ADSConnection(ams_net_id, ams_net_port, ip_address)
        
        #create publisher for the external torque sensed by the device (most of the time human-devices joint torque)
        self.pubExtTorque = rospy.Publisher('Joint_Torque_Ext', JointState, queue_size=10)
        
        #connect to the variables for the external joint torque to publish in ROS
        self.adsConnection.registerReadVariable('Joint_Torque_Ext', 'Object1 (KinestheticFeedback).Output.HapticTorque')
        
        #create publisher for the EMG sensed by the device (up to 16 in our Twincat project)
        self.pubEMG = rospy.Publisher('emg', JointState, queue_size=10)
        
        #connect to the variables for the external EMG to publish in ROS
        self.adsConnection.registerReadVariable('emg', 'Object2 (EMGOBTwincat).Output.EMGFilt', 0, 16)
        
        #Create the ROS node
        rospy.init_node('bridge', anonymous=True)
        
        #running at 100Hz since it's use to control the device
        self.rate = rospy.Rate(100)
        
        #subscribe to the biological joint torque
        rospy.Subscriber("joint_state", JointState, self.callbackJointState)
        
        #connect to the twincat variables to send the biological joint torque (from CEINMS)
        self.adsConnection.registerWriteVariable('Joint_Torque', 'Object1 (KinestheticFeedback).Input.NMSTorques')
        
        #connect to the twincat variables to send the biological joint position (from Xsens)
        self.adsConnection.registerWriteVariable('Joint_Position', 'Object1 (KinestheticFeedback).Input.DangerousLevel')
    
    
    def setEMGNAme(self, emgName):
        self.emgName = emgName
    
    def run(self):
        while not rospy.is_shutdown():
            #get the data from twincat for the external hoint torque
            dataExtJointTorque = self.adsConnection.readVariable('Joint_Torque_Ext')
            
            #create the message...
            msgExtJointTorque = JointState()
            msgExtJointTorque.name = ['L5_S1_Flex_Ext']
            msgExtJointTorque.effort = [dataExtJointTorque]
            
            #... and send it
            self.pubExtTorque.publish(msgExtJointTorque)
            
            #Get EMG data from Twincat
            emgData = self.adsConnection.readVariableArray('emg')
            
            #create the message...
            msgNMS = JointState()
            msgNMS.name = self.emgName
            msgNMS.position = emgData[:len(self.emgName)]
            
            #... and send it
            self.pubEMG.publish(msgNMS)
            
            #sleep to run at 100Hz
            self.rate.sleep()
    
    def __del__(self):
        self.disconnect()
            
    def disconnect(self):
        self.adsConnection.disconnect()
    
    def callbackJointState(self, data):
        index = data.name.index('L5_S1_Flex_Ext')
        
        if len(data.effort)>0:
            self.adsConnection.writeVariable('Joint_Torque', data.effort[index])
        
        if len(data.position)>0:
            self.adsConnection.writeVariable('Joint_Position', data.position[index])
        

