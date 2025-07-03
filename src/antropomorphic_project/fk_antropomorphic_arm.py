#!/usr/bin/env python3

from generate_matrices import GenerateMatrices
from sympy import pi, Float

class FKAntropomorphicArm:
    def __init__(self, r1=0.0, r2=1.0, r3=1.0):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self._fk_calc = GenerateMatrices()

    def compute(self, theta1, theta2, theta3):
        thetas = [theta1, theta2, theta3]
        alphas = [pi/2, 0, 0]
        rs     = [self.r1, self.r2, self.r3]
        ds     = [0,     0,     0]

        # Compute transforms
        A_mats, A0_3_raw, A0_3_simpl = self._fk_calc.compute(thetas, alphas, rs, ds)
        # Extract position and orientation
        position = A0_3_simpl[:3, 3]
        orientation = A0_3_simpl[:3, :3]
        return position, orientation, A0_3_simpl

    def interactive(self):
        theta1 = Float(input("Enter the value for theta_1: "))
        theta2 = Float(input("Enter the value for theta_2: "))
        theta3 = Float(input("Enter the value for theta_3: "))

        # Compute forward kinematics
        pos_vec, ori_mat, full_tf = self.compute(theta1, theta2, theta3)

        # Display
        print("Position Matrix:")
        print(pos_vec)
        print("\nOrientation Matrix:")
        print(ori_mat)

        # Save image
        self._fk_calc.preview_matrix(full_tf, "A03_simplify_evaluated.png")
        print("\nSaved A03_simplify_evaluated.png")

if __name__ == "__main__":
    FKAntropomorphicArm().interactive()
