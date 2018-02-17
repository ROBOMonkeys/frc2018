import wpilib as wpi
import wpilib.drive as drive
from wpilib.interfaces.generichid import GenericHID

class MyRobot(wpi.IterativeRobot):
    def robotInit(self):
        self.auto_state = 0

        self.sd = wpi.SmartDashboard()

        self.sd.putBoolean("Autonomous Center", False)
        self.sd.putBoolean("Autonomous Left", False)
        self.sd.putBoolean("Autonomous Right", False)

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
    def autonomousPeriod(self):
        #left side left switch boi
     if self.auto_state == 1:
        if self.timer.get() < 1.000:
            self.drive.tankDrive(.2,.2)
        elif self.timer.get() < 3.000:
            self.drive.tankDrive(.4,0)
        else:
            self.drive.tankDrive(0, 0)
        # right side left switch
     elif self.auto_state == 2:
        if self.timer.get() < 1.00:
             self.drive.tankDrive(.2,.2)
        elif self.timer.get() < 3.000:
            self.drive.tankDrive(.25,.35)
        elif self.timer.get() < 4.000:
            self.drive.tankDrive(.4,0)
        else:
            self.drive.tankDrive(0, 0)
        # center pos left switch boi
     elif self.auto_state == 3:
           if self.timer.get() < 1.000:
            self.drive.tankDrive(0,.4)
        elif self.timer.get() < 3.00
            self.drive.tankDrive(.1,.3)
        elif self.timer.get() < 5.00
            self.drive.tankDrive(.3,.0)
        else:
            self.drive.tankDrive(0, 0)
       # for left switch right  pos
       elif self.auto_state == 4:
        if self.timer.get() < 1.000:
            self.drive.tankDrive(.2,.2)
        elif self.timer.get() < 3.000:
            self.drive.tankDrive(.4,0)
        else:
            self.drive.tankDrive(0, 0)
        # left pos right switch
        elif self.auto_state == 5:
        if self.timer.get() < 1.00:
            self.drive.tankDrive(.2,.2)
        elif self.timer.get() < 3.000:
             self.drive.tankDrive(.35,.2)
        elif self.timer.get() < 4.000:
            self.drive.tankDrive(.4,0)
        else:
            self.drive.tankDrive(0, 0)
        #center pos right switch
        elif self.auto_state == 6:
        if self.timer.get() < 1.000:
         self.drive.tankDrive(.3,.3)
        elif self.timer.get() < 3.00
         self.drive.tankDrive(.3,.1)
        elif self.timer.get() < 5.00
            self.drive.tankDrive(.0,.3)
        else:
            self.drive.tankDrive(0,0)


if __name__ == '__main__':
wpi.run(MyRobot)