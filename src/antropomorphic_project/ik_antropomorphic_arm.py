#!/usr/bin/env python3

import math

class IKAntropomorphicArm:
    def __init__(self,
                 r2=1.0,
                 r3=1.0,
                 theta2_limits=(-math.pi/4, 3*math.pi/4),
                 theta3_limits=(-3*math.pi/4, 3*math.pi/4)):
        # Link lengths
        self.r2 = r2
        self.r3 = r3
        # Joint limits
        self.theta2_min, self.theta2_max = theta2_limits
        self.theta3_min, self.theta3_max = theta3_limits

    def normalize(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    def calculate_ik(self, Pee_x, Pee_y, Pee_z):
        # Distances in XY plane and total
        d_xy = math.hypot(Pee_x, Pee_y)
        D_sq = d_xy**2 + Pee_z**2

        # Cosine of joint 3 via law of cosines
        C3 = (D_sq - self.r2**2 - self.r3**2) / (2 * self.r2 * self.r3)
        if abs(C3) > 1.0:
            return []  # target out of reach

        # Common angles
        phi = math.atan2(Pee_z, d_xy)
        theta1_base = math.atan2(Pee_y, Pee_x)
        theta1_flip = self.normalize(theta1_base - math.pi)

        solutions = []
        # Four branches: config "plus"/"minus" × sign3 +1/-1
        for config in ("plus", "minus"):
            for sign3 in (1, -1):
                S3 = sign3 * math.sqrt(1 - C3**2)
                theta3 = math.atan2(S3, C3)
                # Auxiliary shoulder offset
                delta2 = math.atan2(abs(self.r3 * S3), self.r2 + self.r3 * C3)

                if config == "plus":
                    theta2 = phi - sign3 * delta2
                    theta1 = theta1_base
                else:
                    raw = phi + sign3 * delta2
                    theta2 = self.normalize(math.pi - raw)
                    theta1 = theta1_flip

                theta2 = self.normalize(theta2)
                # Check joint limits
                possible = (self.theta2_min <= theta2 <= self.theta2_max) and \
                           (self.theta3_min <= theta3 <= self.theta3_max)
                solutions.append((theta1, theta2, theta3, possible))

        return solutions

    def interactive(self):
        """
        Prompt the user for Pee_x, Pee_y, Pee_z and display solutions.
        """
        Pee_x = float(input("Enter the value for Pee_x: "))
        Pee_y = float(input("Enter the value for Pee_y: "))
        Pee_z = float(input("Enter the value for Pee_z: "))

        print(f"Pee_x = {Pee_x}\nPee_y = {Pee_y}\nPee_z = {Pee_z}\nr2 = {self.r2}\nr3 = {self.r3}")
        sols = self.calculate_ik(Pee_x, Pee_y, Pee_z)
        if not sols:
            print("No real solutions: target is out of reach")
            return

        for theta1, theta2, theta3, possible in sols:
            print(f"Angles thetas solved =[ {theta1}, {theta2}, {theta3}] , solution possible = {possible}")

if __name__ == '__main__':
    IKAntropomorphicArm().interactive()
