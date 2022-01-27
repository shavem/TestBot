import wpilib
import ctre
import magicbot
# import navx
import wpilib.drive
from networktables import NetworkTables
import logging

# from enum import IntEnum
from wpilib import Solenoid, DoubleSolenoid




'''
python py/robot/robot.py deploy --skip-tests
'''

'''
pip install wpilib

py -3 -m pip install -U robotpy[ctre]'''




# otherNumber = sd.getNumber('otherNumber')

class SpartaBot(magicbot.MagicRobot):

    def createObjects(self):

        # Initialize SmartDashboard
        logging.basicConfig(level=logging.DEBUG)
        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd = NetworkTables.getTable('SmartDashboard')
        self.drive_controller = wpilib.XboxController(1)

        self.timer = wpilib.Timer()

        # drivetrain
        self.drivetrain_left_motor_master = ctre.WPI_TalonSRX(0)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(1)
        self.drivetrain_right_motor_master = ctre.WPI_TalonSRX(5)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonSRX(6)
        self.left = wpilib.SpeedControllerGroup(
            self.drivetrain_left_motor_master, self.drivetrain_left_motor_slave)
        self.right = wpilib.SpeedControllerGroup(
            self.drivetrain_right_motor_master, self.drivetrain_right_motor_slave)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)


    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()
        self.forward = 0
        self.turning = 0
        print("autonomousInit")

    def autonomousPeriodic(self):
        print("autonomous running")
        time = self.timer.get()
        print(time)
        if time < 1.0:  # 0-1 secs
            self.forward = 0.5
            self.turning = 0
            print("0-1 secs")
        elif time < 2.5:  # 1-2.5 secs
            self.forward = 0
            self.turning = 0
            print("1-2.5 secs")
        elif time < 3.5:  # 2.5 - 3.5 secs
            self.forward = 0
            self.turning = 0.5
            print("2.5 - 3.5 secs")
        else:  # after 3.5 secs
            self.forward = 0
            self.turning = 0
            print("after 3.5 secs")

        self.drive.arcadeDrive(self.turning, self.forward)

    def teleopInit(self):
        # self.drivetrain.setSafetyEnabled(True)
        self.drive.setSafetyEnabled(False)
        # self.intake_arm_solenoid.set(DoubleSolenoid.Value.kForward)

    def teleopPeriodic(self):
        angle = self.drive_controller.getLeftX()
        speed = self.drive_controller.getLeftY()
        if (abs(angle) > 0.05 or abs(speed) > 0.05):
            self.drive.arcadeDrive(angle, speed, True)
            self.sd.putNumber('Left Master Speed: ', self.drivetrain_left_motor_master.get())
            self.sd.putNumber("Left Slave Speed: ", self.drivetrain_left_motor_slave.get())
            self.sd.putNumber('Right Master Speed: ', -self.drivetrain_right_motor_master.get())
            self.sd.putNumber("Right Slave Speed: ", -self.drivetrain_right_motor_slave.get())
        else:
            self.drive.arcadeDrive(0, 0, True)


if __name__ == '__main__':
    wpilib.run(SpartaBot)
