import wpilib as wpi
import wpilib.drive as drive
from wpilib.interfaces.generichid import GenericHID

class MyRobot(wpi.IterativeRobot):
    def robotInit(self):
        self.solenoid = wpi.solenoid
        self.lift = wpi.Spark(5)
        self.frontLeftMotor = wpi.Spark(2)
        self.rearLeftMotor = wpi.Spark(3)
        self.frontRightMotor = wpi.Spark(1)
        self.rearRightMotor = wpi.Spark(0)

        self.left = wpi.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpi.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.drive = drive.DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)
        self.controller = wpi.XboxController(0)

        self.timer = wpi.Timer()
        self.deltaTime = 0

    def teleopInit(self):

        self.drive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        # motor for lift
        self.lift.set(self.controller.getTriggerAxis(GenericHID.Hand.kLeft) + self.controller.getTriggerAxis(GenericHID.Hand.kRight)
        #for dumper boi
        if self.joystick.getXButton() and self.timer.get() > 0.2:
            state = self.solenoid.get()
            self.timer.reset()
            if state == False:
                self.solenoid.set(True)
            else:
                self.solenoid.set(False)



        # for grabber piston boiii
        if self.joystick.pressAButton() and self.timer.get() > 0.2:
            state = self.solenoid.get()
            self.timer.reset()
            if state == False:
                self.solenoid.set(True)
            else:
                self.solenoid.set(False)


        self.drivestate = True

        self.drive.tankDrive(self.controller.getY(GenericHID.Hand.kLeft) * -1, self.controller.getY(GenericHID.Hand.kRight) * -1)


    def autonomousInit(self):
        self.timer.stop()
        self.timer.reset()
        self.timer.start()

if __name__ == '__main__':
wpi.run(MyRobot)