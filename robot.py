import wpilib as wpi
import enums


class MyRobot(wpilib.IterativeRobot):
    def robotInit(self):

        self.frontLeftMotor = wpi.Spark(2)
        self.rearLeftMotor = wpi.Spark(3)
        self.frontRightMotor = wpi.Spark(1)
        self.rearRightMotor = wpi.Spark(0)

        self.left = wpi.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpi.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        self.leftStick = wpi.Joystick(0)
        self.rightStick = wpi.Joystick(1)

    def autonomousInit(self):


    def teleopInit(self):

        self.myRobot.setSafetyEnabled(True)

    def teleopPeriodic(self):

        self.myRobot.tankDrive(self.leftStick.getY() * -1, self.rightStick.getY() * -1)


if __name__ == '__main__':
    wpilib.run(MyRobot)
