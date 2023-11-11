from robolink import *    # API to communicate with RoboDK
from robodk import *      # basic matrix operations
import math as mt

_blobs = {}

# Angle Based on Frame
# CillinderFrontTarget
#   - Angle on circle 270.0 
#   - Sanding angle   -90.0
# CillinderLeftTarget  
#   - Angle on circle 180.0
#   - Sanding angle   180.0
# CillinderBackTarget  
#   - Angle on circle 90
#   - Sanding angle   90.0
# CillinderRightTarget 
#   - Angle on circle 0
#   - Sanding angle   0.0
#
#             90
#         _.-""""""-._
#       .'            `.
#      /                \
#     |                  |
# 180 |                  | 0
#     |                  |
#      \                /
#       `._          _.'
#          `-......-'
#             270

RADIUS = 134

def CalculateCartesian(angle):
    x = RADIUS * mt.cos(angle * (pi / 180))
    y = RADIUS * mt.sin(angle * (pi / 180))

    return x, y

def setBlobs(blobs):
    _blobs = blobs

def run():
    __moveToPoint()


def __moveToPoint():
    y = 2

def runDebugProcedure():
    # Connect to the RoboDK API
    RDK = Robolink()
    RDK.setSimulationSpeed(1)
    # Retrieve specific items
    robot = RDK.Item('Fanuc M-20iA/35M')
    robot.setSpeed(500)
    homeTarget = RDK.Item('Home')
    cillinderFrontTarget = RDK.Item('CillinderFrontTarget')

    # Set HomeTarget as approach and goto target
    approach = homeTarget.Pose()
    robot.MoveL(approach)

    # Set FrontTarget as approach and goto target
    approach = cillinderFrontTarget.Pose()
    print(approach)
    robot.MoveL(approach)

    # Use FrontTarget as initial start position
    XYZ = Pose_2_Fanuc(approach)

    print(XYZ)

    robot.setSpeed(50)

    XYZ[0], XYZ[1] = CalculateCartesian(225.0)
    XYZ[5] = 45.0
    middleApproach = Fanuc_2_Pose(XYZ)
    print(XYZ)
    print(middleApproach)

    XYZ[0], XYZ[1] = CalculateCartesian(180.0)
    XYZ[5] = 0.0
    finalApproach = Fanuc_2_Pose(XYZ)
    print(XYZ)
    print(finalApproach)

    robot.MoveC(middleApproach, finalApproach)

    XYZ[0], XYZ[1] = CalculateCartesian(270.0)
    XYZ[5] = 90.0
    middleApproach = Fanuc_2_Pose(XYZ)
    print(XYZ)
    print(middleApproach)

    XYZ[0], XYZ[1] = CalculateCartesian(360.0)
    XYZ[5] = 180.0
    finalApproach = Fanuc_2_Pose(XYZ)
    print(XYZ)
    print(finalApproach)

    robot.MoveC(middleApproach, finalApproach)
    robot.setSpeed(500)