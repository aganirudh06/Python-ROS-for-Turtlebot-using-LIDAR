########################################################################################################################

# Navigate the Turtlebot out of a maze

########################################################################################################################

from robot_control_class import RobotControl  # Importing Robot Control function to control the movement of turtlebot
rc = RobotControl()  # Referencing the Robot Control function into a variable for easy use

angleperline = 180 / 719  # Calculating the angle per line or laser of 720 LIDAR lasers ranging from 0 to 719 (Right to Left)
looo = rc.get_laser(360)  # Reading the laser value that points straight ahead to evaluate the distance of any obstacle in front

while looo != 0:  # Execute the below code infinitely
    laser = rc.get_laser_full()  # Read all the 720 laser readings of LIDAR
    nnn = laser[260:460]  # Taking values within the range of 260 to 460 in front of the turtlebot for collision avoidance
    i = min(nnn)  # Calculating the minimum laser reading in this range so that the robot is moved forward based on this minimum laser reading

    if i > 0.9:  # Execute the below code block if the distance from the robot to the minimum laser value in the range taken is more than 0.9
        rc.move_straight()  # Move turtlebot forward

    if i < 0.9:  # If turtlebot reaches within a distance of 0.9m of a wall, execute below code block

        rc.stop_robot()              # Stop turtlebot
        laser = rc.get_laser_full()  # Re-evaluating the laser readings for better accuracy over time

        max_laser = max(laser)  # Find the maximum laser reading among 719 readings
        print("Max laser value is ", max_laser)  # Printing the maximum laser reading to the terminal
        index = laser.index(max_laser)  # Index of this maximum laser reading to find the direction of this reading
        print("Index is ", index)       # Printing the Index of maximum laser reading to the terminal
        b = (360 - index)               # constant b
        angle = angleperline * b        # Converting the laser reading index into angle that the turtlebot needs to be rotated to point towards maximum laser reading
        print("Angle to turn is ", angle) # Printing Angle to turn to the terminal

        if index in range(260, 460) and i < 0.9: # This is used to overcome the turtlebot getting struck at corners of the walls while taking left of right.
        # If the maximum laser reading points to go forward and the robot is very near to a wall, the width of the turtlebot needs to be considered
        # to avoid hitting the wall or obstacle.
            new_laser = list(laser)      # Duplicating the full laser readings and converting them into a list for easy manipulation
            del new_laser[260:460]       # Delete the laser readings with indices between 260 and 460 to avoid turning towards the wall or hitting the wall
            max_laser = max(new_laser)   # Re-evaluate the new maximum laser reading which is not in between 260 and 460
            for n in range(260, 460):    # To avoid reading wrong indices of duplicate elements
                laser = list(laser)
                laser[n] = 0             # Replacing the laser readings between 260 and 460 with 0 so that they cannot be read for higher laser reading
                                         # again and again to avoid falling into an infinite loop

            index = laser.index(max_laser) # Finding the angle of new maximum laser reading
            b = (360 - index)
            angle = angleperline * b

        a = int(angle)
        rc.rotate(-a)                   # Rotate the turtlebot at above calculated angle