#!/usr/bin/env python3

import rospy
from planar_3dof_control.msg import EndEffector
from geometry_msgs.msg import Vector3
from antropomorphic_project.ik_antropomorphic_arm import IKAntropomorphicArm
from antropomorphic_project.move_joints         import JointMover
from antropomorphic_project.rviz_marker         import MarkerBasics

class AntropomorphicEndEffectorMover:
    def __init__(self):
        # IK solver instance
        self.ik_solver   = IKAntropomorphicArm()
        # Joint mover for commanding the arm
        self.robot_mover = JointMover()
        # Marker helper to visualize target points as spheres
        self.marker      = MarkerBasics()
        self.marker_id   = 0

        # Subscribe to commanded ellipsoidal trajectory
        rospy.Subscriber('/ee_pose_commands', EndEffector, self.ee_pose_callback)
        # Subscribe to real end-effector pose for monitoring
        rospy.Subscriber('/end_effector_real_pose', Vector3, self.real_pose_callback)

        rospy.loginfo('AntropomorphicEndEffectorMover initialized, waiting for commands...')

    def real_pose_callback(self, msg: Vector3):
        # Log actual position reached by the robot
        rospy.loginfo("Real EE pose -> x: %.3f, y: %.3f, z: %.3f",
                      msg.x, msg.y, msg.z)

    def ee_pose_callback(self, msg: EndEffector):
        # Extract commanded target and elbow policy ('up' or 'down')
        x      = msg.ee_xy_theta.x
        y      = msg.ee_xy_theta.y
        z      = msg.ee_xy_theta.z
        policy = msg.elbow_policy.data  # should be 'up' or 'down'

        # Compute all 4 IK solutions via your existing method
        solutions = self.ik_solver.calculate_ik(Pee_x=x, Pee_y=y, Pee_z=z)
        if not solutions:
            rospy.logerr("No IK solutions at (%.3f, %.3f, %.3f)", x, y, z)
            return

        # Choose the two branches based on elbow policy
        if policy == 'down':
            candidates = solutions[0:2]  # elbow-down branches
        else:
            candidates = solutions[2:4]  # elbow-up branches

        # Pick the first feasible (within limits) in that group
        selected = None
        for t1, t2, t3, ok in candidates:
            if ok:
                selected = (t1, t2, t3)
                break

        # Fallback to the first raw if none within limits
        if selected is None:
            rospy.logwarn("No %s-elbow solution within limits; using first raw", policy)
            t1, t2, t3, _ = candidates[0]
        else:
            t1, t2, t3 = selected

        # Command the joints
        self.robot_mover.move_all_joints(t1, t2, t3)
        rospy.loginfo("Moving (elbow-%s) to thetas = [%.3f, %.3f, %.3f]",
                      policy, t1, t2, t3)

        # Publish a sphere marker at the goal
        self.marker.publish_point(x, y, z, self.marker_id)
        self.marker_id += 1

def main():
    rospy.init_node('antropomorphic_end_effector_mover')
    AntropomorphicEndEffectorMover()
    rospy.spin()

if __name__ == '__main__':
    main()
