import wpilib
import ctre
import magicbot
# import navx
import wpilib.drive
# from enum import IntEnum
from wpilib import Solenoid, DoubleSolenoid




'''python py/robot/robot.py deploy --skip-tests'''

'''
pip install wpilib

py -3 -m pip install -U robotpy[ctre]'''


'''
NetworkTables.initialize(server='roborio-5045-frc.local')

sd = NetworkTables.getTable('SmartDashboard')
sd.putNumber('someNumber', 1234)
otherNumber = sd.getNumber('otherNumber')


# ./py/venv/Scripts/activate
'''

# CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeftHand
# CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRightHand

class SpartaBot(magicbot.MagicRobot):

    def createObjects(self):

        self.drive_controller = wpilib.XboxController(1)

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
        # self.hood_solenoid.set(DoubleSolenoid.Value.kForward)
        # self.intake_arm_solenoid.set(DoubleSolenoid.Value.kReverse)
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        # self.drivetrain.setSafetyEnabled(True)
        self.drive.setSafetyEnabled(False)
        # self.intake_arm_solenoid.set(DoubleSolenoid.Value.kForward)

    def teleopPeriodic(self):
        angle = self.drive_controller.getLeftX()
        speed = self.drive_controller.getLeftY()
        if (abs(angle) > 0.05 or abs(speed) > 0.05):
            self.drive.arcadeDrive(speed, -angle, True)
        else:
            self.drive.arcadeDrive(0, 0, True)


if __name__ == '__main__':
    wpilib.run(SpartaBot)
