import wpilib
from wpilib.drive import DifferentialDrive


class MyRobot(wpilib.IterativeRobot):
    
    def robotInit(self):
        '''Robot initialization function'''
        
        # object that handles basic drive operations
        self.frontLeftMotor = wpilib.Spark(1)
        # self.middleLeftMotor = wpilib.Spark(4)
        self.rearLeftMotor = wpilib.Spark(2)

        self.frontRightMotor = wpilib.Spark(3)
        # self.middleRightMotor = wpilib.Spark(1)
        self.rearRightMotor = wpilib.Spark(4)

        self.ihigh_motor = wpilib.Spark(6)
        self.ilow_motor = wpilib.Spark(9)

        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        self.high = 0
        self.low = 0
        self.gameData = ''

        # joysticks 1 & 2 on the driver station
        self.Stick1 = wpilib.XboxController(0)
        self.Stick2 = wpilib.Joystick(1)
        
        self.aSolenoidLow = wpilib.DoubleSolenoid(2,3)
        self.aSolenoidHigh = wpilib.DoubleSolenoid(0,1)
        self.iSolenoid = wpilib.DoubleSolenoid(4,5)

        self.gyro = wpilib.ADXRS450_Gyro()

    def autonomousInit(self):
        self.iSolenoid.set(2)
        self.aSolenoidLow.set(2)
        self.aSolenoidHigh.set(2)
        self.gameData = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        global timer
        timer = wpilib.Timer()
        timer.start()
        global firstTime 
        firstTime = True

        


    def autonomousPeriodic(self):
        # This program tests 90 degree turn with gyro
        global firstTime, maxV, minV
        while firstTime:
            global fD, fluc, sD, v
            sD = self.gyro.getAngle()
            fD = sD - 90
            firstTime = False
            v = 0.65


        cD = self.gyro.getAngle()
        # left smaller right bigger
        if cD > fD :
            cD = self.gyro.getAngle()
            speed_turn  = v 
            self.myRobot.tankDrive(-speed_turn, speed_turn)
            # print ("nD " + str(needD)) 
            # print ("speed " + str(speed_turn))
        else:
            self.myRobot.tankDrive(0,0)
            
        

        
    def disabledInit(self):
        self.myRobot.tankDrive(0,0)
        self.iSolenoid.set(0)
        self.aSolenoidLow.set(0)
        self.aSolenoidHigh.set(0)
    
    def disabledPeriodic(self):
        pass

    def teleopInit(self):
        '''Execute at the start of teleop mode'''
        self.myRobot.setSafetyEnabled(True)
        self.iSolenoid.set(1)
        lastspeed = 0

    def teleopPeriodic(self):
        if self.isOperatorControl() and self.isEnabled():
            forward = self.Stick1.getTriggerAxis(1)
            backward = self.Stick1.getTriggerAxis(0)

            sp = forward - backward
            if abs(self.Stick1.getX(0)) > 0.1:
                steering = (self.Stick1.getX(0) + 0.1*sp) / 1.5
            else:
                steering = 0

            self.myRobot.tankDrive(sp + steering, sp - steering)
           



       
if __name__ == '__main__':
    wpilib.run(MyRobot)
