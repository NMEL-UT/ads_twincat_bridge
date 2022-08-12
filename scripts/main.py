#!/usr/bin/env python

import pyads
import rospy
import bridge

if __name__ == '__main__':
    bridge = bridge.BridgeTwincat()
    bridge.setEMGNAme(['recabd_r', 'recabd_l', 'intobl_r', 'intobl_l', 'extobq_r', 'extobq_l', 'iliocost_r', 'iliocost_l', 'longlumb_r', 'longlumb_l', 'longthor_r', 'longthor_l'])
    bridge.run()
    