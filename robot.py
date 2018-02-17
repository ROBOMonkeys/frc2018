import wpilib as wpi
import wpilib.drive as drive
from wpilib.interfaces.generichid import GenericHID

class MyRobot(wpi.IterativeRobot):
    def robotInit(self):
        self.auto_goal = 0
        self.auto_state = 0

        self.sd = wpi.SmartDashboard()

        self.sd.putBoolean("Center Lane", False)
        self.sd.putBoolean("Left lane", False)
        self.sd.putBoolean("Right lane", False)
        self.sd.putBoolean("right goal",False)
        self.sd.putBoolean("left goal",False)
        self.solenoid = wpi.Solenoid(0)
        self.lift = wpi.Spark(5)
        self.frontLeftMotor = wpi.Spark(2)
        self.rearLeftMotor = wpi.Spark(3)
        self.frontRightMotor = wpi.Spark(1)
        self.rearRightMotor = wpi.Spark(0)

        self.left = wpi.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpi.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.drive = drive.DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)
        self.joystick = wpi.XboxController(0)

        self.timer = wpi.Timer()
        self.deltaTime = 0

    def teleopInit(self):

        self.drive.setSafetyEnabled(True)

    def teleopPeriodic(self):
        # motor for lift
        self.lift.set(self.joystick.getTriggerAxis(GenericHID.Hand.kLeft) + self.joystick.getTriggerAxis(GenericHID.Hand.kRight))
        #for dumper boi
        if self.joystick.getXButton() and self.timer.get() > 0.2:
            state = self.solenoid.get()
            self.timer.reset()
            if state == False:
                self.solenoid.set(True)
            else:
                self.solenoid.set(False)



        # for grabber piston boiii
        if self.joystick.getAButton() and self.timer.get() > 0.2:
            state = self.solenoid.get()
            self.timer.reset()
            if state == False:
                self.solenoid.set(True)
            else:
                self.solenoid.set(False)


        self.drivestate = True

        self.drive.tankDrive(self.joystick.getY(GenericHID.Hand.kLeft) * -1, self.joystick.getY(GenericHID.Hand.kRight) * -1)


    def autonomousInit(self):
        if self.sd.getBoolean("Left lane", False):
            self.auto_state = 1
        elif self.sd.getBoolean("Center lane", False):
            self.auto_state = 3
        elif self.sd.getBoolean("Right lane", False):
            self.auto_state = 4

        if self.sd.getBoolean("left goal", False):
            self.sd.getBoolean = 5
        elif self.sd.getBoolean("right goal", False):
            self.sd.getBoolean = 6

        #self.timer.stop()
        self.timer.reset()
        self.timer.start()

    def autonomousPeriod(self):
        #left lane left goal
        if self.auto_state == 1:
            if self.auto_goal == 5:
                if self.timer.get() < 1.000:
                    self.drive.tankDrive(.2,.2)
                elif self.timer.get() < 3.000:
                    self.drive.tankDrive(.4,0)
                else:
                    self.drive.tankDrive(0, 0)
            else:
                # left lane right goal
                if self.timer.get() < 1.00:
                    self.drive.tankDrive(.2, .2)
                elif self.timer.get() < 3.000:
                    self.drive.tankDrive(.35, .2)
                elif self.timer.get() < 4.000:
                    self.drive.tankDrive(.4, 0)
                #center lane right goal
        elif self.auto_state == 3:
            if self.auto_goal == 6:
                if self.timer.get() < 1.000:
                    self.drive.tankDrive(.3, .3)
                elif self.timer.get() < 3.00:
                    self.drive.tankDrive(.3, .1)
                elif self.timer.get() < 5.00:
                    self.drive.tankDrive(.0, .3)
                else:
                    self.drive.tankDrive(0, 0)
            else:
                # center lane left goal
                if self.timer.get() < 1.000:
                    self.drive.tankDrive(0, .4)
                elif self.timer.get() < 3.00:
                    self.drive.tankDrive(.1, .3)
                elif self.timer.get() < 5.00:
                    self.drive.tankDrive(.3, 0)
                    #right lane right goal
        elif self.auto_state == 4:
            if self.auto_goal == 6:
                if self.timer.get() < 1.000:
                    self.drive.tankDrive(.2, .2)
                elif self.timer.get() < 3.000:
                    self.drive.tankDrive(.4, 0)
                else:
                    self.drive.tankDrive(0, 0)
            else:
                #right lane left goal
                if self.timer.get() < 1.00:
                    self.drive.tankDrive(.2, .2)
                elif self.timer.get() < 3.000:
                    self.drive.tankDrive(.25, .35)
                elif self.timer.get() < 4.000:
                    self.drive.tankDrive(.4, 0)

if __name__ == '__main__':
    wpi.run(MyRobot)