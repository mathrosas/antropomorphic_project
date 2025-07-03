#!/usr/bin/env python3

import math

# Link lengths
r2 = 1.0
r3 = 1.0

# Joint limits
theta2_min, theta2_max = -math.pi/4, 3*math.pi/4
theta3_min, theta3_max = -3*math.pi/4, 3*math.pi/4


def normalize(angle):
    return math.atan2(math.sin(angle), math.cos(angle))


def main():
    # Prompt user for desired position
    Pee_x = float(input("Enter the value for Pee_x: "))
    Pee_y = float(input("Enter the value for Pee_y: "))
    Pee_z = float(input("Enter the value for Pee_z: "))

    # Precompute distances
    d_xy = math.hypot(Pee_x, Pee_y)
    D_sq = d_xy**2 + Pee_z**2

    # Compute cos(theta3)
    C3 = (D_sq - r2**2 - r3**2) / (2 * r2 * r3)

    # Header print
    print(f"Pee_x = {Pee_x}\nPee_y = {Pee_y}\nPee_z = {Pee_z}\nr2 = {r2}\nr3 = {r3}")

    if abs(C3) > 1.0:
        print("No real solutions: target is out of reach")
        return

    # Common angles
    phi = math.atan2(Pee_z, d_xy)
    theta1_base = math.atan2(Pee_y, Pee_x)
    theta1_flip = normalize(theta1_base - math.pi)

    # Four solution branches
    for config in ("plus", "minus"):
        for sign3 in (1, -1):
            S3 = sign3 * math.sqrt(1 - C3**2)
            theta3 = math.atan2(S3, C3)

            # Magnitude for delta2
            delta2 = math.atan2(abs(r3 * S3), r2 + r3 * C3)

            if config == "plus":
                theta2 = phi - sign3 * delta2
                theta1 = theta1_base
            else:
                raw = phi + sign3 * delta2
                theta2 = normalize(math.pi - raw)
                theta1 = theta1_flip

            # Wrap theta2
            theta2 = normalize(theta2)

            possible = (theta2_min <= theta2 <= theta2_max) and (theta3_min <= theta3 <= theta3_max)
            print(f"Angles thetas solved =[ {theta1}, {theta2}, {theta3}] , solution possible = {possible}")


if __name__ == '__main__':
    main()
