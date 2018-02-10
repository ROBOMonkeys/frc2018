import wpilib as wpi
import wpilib.drive as drive
from wpilib.interfaces.generichid import GenericHID

class MyRobot(wpi.IterativeRobot):
    def robotInit(self):

        self.frontLeftMotor = wpi.Spark(2)
        self.rearLeftMotor = wpi.Spark(3)
        self.frontRightMotor = wpi.Spark(1)
        self.rearRightMotor = wpi.Spark(0)

        self.left = wpi.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpi.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.drive = drive.DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)

        self.controller = wpi.XboxController(0)

    def teleopInit(self):

        self.drive.setSafetyEnabled(True)

    def teleopPeriodic(self):

        self.drive.tankDrive(self.controller.getY(GenericHID.Hand.kLeft) * -1, self.controller.getY(GenericHID.Hand.kRight) * -1)

  #  def autonomousInit(self):

if __name__ == '__main__':
    wpi.run(MyRobot)
