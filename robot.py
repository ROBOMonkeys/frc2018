import wpilib as wpi
import networktables.util as ntu
import networktables.networktable as nt
import wpilib.drive as drive
from wpilib.interfaces.generichid import GenericHID



class MyRobot(wpi.IterativeRobot):
    solenoidChannel = 0
    solenoidChannel = 1

    def set_dump_mode(self, value):
        self.dump_mode = value
    
    def robotInit(self):
        '''        
        self.auto_goal = 0
        self.auto_state = 0
        self.sd.putBoolean("Center Lane", False)
        self.sd.putBoolean("Left lane", False)
        self.sd.putBoolean("Right lane", False)
        self.sd.putBoolean("right goal", False)
        self.sd.putBoolean("left goal", False)
        '''
        self.sd = wpi.SmartDashboard()
        
        self.sd.putNumber("team", wpi.DriverStation.getInstance().getAlliance())
        
        self.dump_mode = True
        self.dump_chooser = wpi.SendableChooser()
        self.dump_chooser.addDefault("Yes", True)
        self.dump_chooser.addObject("No", False)
        self.sd.putData("Dump?", self.dump_chooser)
        
        self.cc = ntu.ChooserControl("Dump?",
                                     None,
                                     self.set_dump_mode)
        
        wpi.CameraServer.launch("vision/vision.py:run")
        
        self.gripper_sole = wpi.DoubleSolenoid(0,2)
        self.dump_sole = wpi.Solenoid(1)
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
    
    
    def teleopInit(self):
        self.sd.putString("state", "teleop")
        self.drive.setSafetyEnabled(True)
    
    def teleopPeriodic(self):
        # motor for lift
        self.lift.set(self.joystick.getTriggerAxis(GenericHID.Hand.kLeft) + self.joystick.getTriggerAxis(GenericHID.Hand.kRight))
        
        #for dumper boi
        if self.joystick.getXButtonPressed():
            self.dump_sole.set(not self.dump_sole.get())
        
        # for grabber piston boiii
        if not self.gripper_sole.get() == wpi.DoubleSolenoid.Value.kForward and (self.joystick.getAButton()):
            self.gripper_sole.set(wpi.DoubleSolenoid.Value.kForward)
        elif self.gripper_sole.get() == wpi.DoubleSolenoid.Value.kForward and not (self.joystick.getAButton()):
            self.gripper_sole.set(wpi.DoubleSolenoid.Value.kReverse)
        
        self.drive.tankDrive(self.joystick.getY(GenericHID.Hand.kLeft) * -1, self.joystick.getY(GenericHID.Hand.kRight) * -1)
    
    
    def autonomousInit(self):
       ''' if self.sd.getBoolean("Left lane", False):
            self.auto_state = 1
        elif self.sd.getBoolean("Center lane", False):
            self.auto_state = 3
        elif self.sd.getBoolean("Right lane", False):
            self.auto_state = 4

        if self.sd.getBoolean("left goal", False):
            self.auto_goal = 5
        elif self.sd.getBoolean("right goal", False):
            self.auto_goal = 6
       '''

       self.drive.setSafetyEnabled(True)
       self.sd.putString("state", "auto")
       self.timer.stop()
       self.timer.reset()
       self.timer.start()
    
    def autonomousPeriodic(self):
        '''
        #left lane left goal
        if self.auto_state == 1:
            if self.auto_goal == 5:
                if self.timer.get() < 2.000:
                    self.drive.tankDrive(.5,.5)
                elif self.timer.get() < 3.000:
                   self.drive.tankDrive(.5,0)
                else:
                    self.drive.tankDrive(0, 0)
            else:
                # left lane right goal
                if self.timer.get() < 2.00:
                    self.drive.tankDrive(.5, .5)
                elif self.timer.get() < 3.000:
                    self.drive.tankDrive(.35, .2)
                elif self.timer.get() < 4.000:
                    self.drive.tankDrive(.4, 0)
                #center lane right goal
        elif self.auto_state == 3:
            if self.auto_goal == 6:
                if self.timer.get() < 1.000:
                    self.drive.tankDrive(.5, .5)
                elif self.timer.get() < 3.00:
                    self.drive.tankDrive(.3, .1)
                elif self.timer.get() < 5.00:
                    self.drive.tankDrive(.0, .3)
                else:
                    self.drive.tankDrive(0, 0)
            else:
                # center lane left goal
                if self.timer.get() < .850:
                    self.drive.tankDrive(0, .4)
                elif self.timer.get() < 3.00:
                    self.drive.tankDrive(.1, .3)
                elif self.timer.get()< 4.75:
                    self.solenoid.set(True)
                elif self.timer.get() < 5.00:
                    self.drive.tankDrive(.3, 0)
                    #right lane right goal
        elif self.auto_state == 4:
            if self.auto_goal == 6:
                if self.timer.get() < 3.650:
                    self.drive.tankDrive(.75, .7)
                elif self.timer.get() < 5.110:
                    self.drive.tankDrive(.5, 0)
                elif self.timer.get() < 6.00:
                    self.drive.tankDrive(-.55, -.58)
                #elif self.timer.get() < 8.50:
                    #self.dump_sole.set(True)
                else:
                    self.drive.tankDrive(0, 0)
            else:
                #right lane left goal
                if self.timer.get() < 1.00:
                    self.drive.tankDrive(.2, .2)
                elif self.timer.get() < 3.000:
                    self.drive.tankDrive(.25, .35)
                elif self.timer.get() < 4.000:
                    self.drive.tankDrive(., 0)
                elif self.timer.get()< 4.75:
                    self.solenoid.set(True)
                elif self.timer.get() < 5.25:
                    self.drive.tankDrive(0,.4)
                    #pugs indeed lolzzzz
        '''
        
        if self.timer.get() < 2.00:
            self.drive.tankDrive(-.5,-.5)
        else:
            self.drive.tankDrive(0,0)
            
            if self.sd.getBoolean("dump", False) and self.dump_mode:
                self.dump_sole.set(True)
    

if __name__ == '__main__':
    wpi.run(MyRobot)
