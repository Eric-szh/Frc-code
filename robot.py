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

        self.gyro = wpilib.AnalogGyro(0)




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
        global firstTime, fD, fastD, fastV, slowV, error
        if firstTime:
            sD = self.gyro.getAngle()
            fD = sD - 90
            firstTime = False
            fastV = 0.78
            slowV = 0.64
            fastD = 75
            error = 0

        cD = self.gyro.getAngle()
        # left smaller right bigger
        if cD > fD - error:
            cD = self.gyro.getAngle()
            needD  = cD - fD # getting smaller as turing left
            if needD >= 90 - fastD:
                speed_turn = fastV
                print('fast')
            else:
                speed_turn = slowV
                print('slow')
            
            self.myRobot.tankDrive(-speed_turn, speed_turn)
            print(cD)
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
        self.gyro.setDeadband(0.1)
        self.gyro.calibrate()
        print('calibrated')


        


    def teleopPeriodic(self):
        if self.isOperatorControl() and self.isEnabled():
            threshold = 0.4#机器人能开的速度
            slow = 0.7#将这个以下的速度精细控制
            current_speed = 0
            deadband_forward = 0.1#向前的deadband
            deadband_steering = 0.1#转弯的deadband
            stering_mutiplier = 1.3#越大，转弯越慢

            
            forward = self.Stick1.getTriggerAxis(1)
            backward = self.Stick1.getTriggerAxis(0)
            sum_speed = forward - backward

            if abs(sum_speed) > deadband_forward:#如果开的话转弯变慢
                stering_mutiplier = 2.0
            else:
                stering_mutiplier = 1.3

            steering = (self.Stick1.getX(0)) / stering_mutiplier#算转弯
            
            if abs(steering) < deadband_steering:#转弯的deadband
                steering = 0
            
            if sum_speed >= 0:#算前进方向
                direct = 1
            elif sum_speed < 0: 
                direct = -1

            if ((abs(sum_speed) < slow) and (abs(sum_speed) > deadband_forward)): #多档控制
                calculated_speed = sum_speed*((slow - threshold) / slow) + threshold*direct
            elif abs(sum_speed) > slow:
                calculated_speed = sum_speed
            else:
                calculated_speed = 0
            
            print(self.gyro.getAngle())
            self.myRobot.tankDrive(calculated_speed + steering, calculated_speed - steering)

        def testInit(self):
            pass

        def testPeriodic(self):
            pass



       
if __name__ == '__main__':
    wpilib.run(MyRobot)
