from controller import Robot, Motion

class Nao(Robot):
    PHALANX_MAX = 8

    def loadMotionFiles(self):
        # Load motion files
        self.handWave = Motion('../../motions/HandWave.motion')
        self.LeftDive = Motion('../../motions/LeftDive.motion')
        self.RightDive = Motion('../../motions/RightDive.motion')
        self.Shoot = Motion('../../motions/Shoot.motion')

    def startMotion(self, motion):
        # Interrupt current motion
        if self.currentlyPlaying:
            self.currentlyPlaying.stop()

        # Start new motion
        motion.play()
        self.currentlyPlaying = motion
        self.isPlaying = True

    def detectBall(self):
        # Get sensor readings
        left_distance = self.us_left.getValue()
        right_distance = self.us_right.getValue()

        # Determine ball position based on sensor readings
        if left_distance < 0.5 and right_distance >= 0.5:  # Adjust threshold if needed
            return 'left'
        elif right_distance < 0.5 and left_distance >= 0.5:  # Adjust threshold if needed
            return 'right'
        elif left_distance < 0.5 and right_distance < 0.5:
            return 'center'
        else:
            return 'none'

    def senseAndReact(self):
        # Detect the ball position and react accordingly
        ball_position = self.detectBall()
        print("Ball Position:", ball_position)  # Print Current Ball Position
        if ball_position == 'left':
            self.diveLeft()
        elif ball_position == 'right':
            self.diveRight()
        elif ball_position == 'center':
            self.shoot()

    def diveLeft(self):
        self.startMotion(self.LeftDive)

    def diveRight(self):
        self.startMotion(self.RightDive)

    def shoot(self):
        self.startMotion(self.Shoot)

    def findAndEnableDevices(self, time_step):
        # Enable the ultrasound sensors
        self.us_left = self.getDevice("Sonar/Left")
        self.us_right = self.getDevice("Sonar/Right")
        self.us_left.enable(time_step)
        self.us_right.enable(time_step)

    def __init__(self):
        Robot.__init__(self)
        self.currentlyPlaying = False
        self.isPlaying = False
        self.time_step = 64  # Define the time step here

        # Initialize stuff
        self.findAndEnableDevices(self.time_step)
        self.loadMotionFiles()

    def run(self):
        print("\n'----------nao_robocup_goalkeeper----------'")
        print("I am a Nao GoalKeeper Robot, I can dive left and right to stop the goal. I can also shoot the ball to stop the goal.")
        # Perform hand waving animation
        self.startMotion(self.handWave)
        
        # Loop indefinitely to keep the robot running
        while self.step(self.time_step) != -1:
            # Sense the ball position and react accordingly
            ball_position = self.detectBall()
            if ball_position != 'none':
                self.senseAndReact()

# Create the Robot instance and run the main loop
robot = Nao()
robot.run()