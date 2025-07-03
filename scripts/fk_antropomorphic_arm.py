#!/usr/bin/env python3

from generate_matrices import DHCalculator
from sympy import pi, Float


def main():
    # Prompt user for joint angles in radians
    theta1 = Float(input("Enter the value for theta_1: "))
    theta2 = Float(input("Enter the value for theta_2: "))
    theta3 = Float(input("Enter the value for theta_3: "))

    # Link lengths (modify as needed)
    r1, r2, r3 = 0.0, 1.0, 1.0

    # Assemble DH parameter lists
    thetas = [theta1, theta2, theta3]
    alphas = [pi/2, 0, 0]
    rs     = [r1,    r2,  r3]
    ds     = [0,     0,   0]

    # Compute both raw and simplified A0_3
    fk_calc = DHCalculator()
    A_list, A0_3, A0_3_simplified = fk_calc.compute(thetas, alphas, rs, ds)

    # Extract position (3×1) and orientation (3×3)
    pos_vec = A0_3_simplified[:3, 3]
    ori_mat = A0_3_simplified[:3, :3]

    # Print results
    print("Position Matrix:")
    print(pos_vec)
    print("\nOrientation Matrix:")
    print(ori_mat)

    # Save image of fully evaluated, simplified matrix
    fk_calc.preview_matrix(A0_3_simplified, "A03_simplify_evaluated.png")
    print("\nSaved A03_simplify_evaluated.png")


if __name__ == "__main__":
    main()
