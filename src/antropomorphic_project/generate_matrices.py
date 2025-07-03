#!/usr/bin/env python3

from sympy import Matrix, cos, sin, Symbol, simplify, trigsimp, preview, pi
from sympy.interactive import printing

# To make display pretty
printing.init_printing(use_latex=True)

class GenerateMatrices:
    def __init__(self):
        # Define generic DH symbols
        self.theta_i = Symbol("theta_i")
        self.alpha_i = Symbol("alpha_i")
        self.r_i = Symbol("r_i")
        self.d_i = Symbol("d_i")

        # Define the generic DH matrix
        self.DH_generic = Matrix([
            [cos(self.theta_i), -sin(self.theta_i)*cos(self.alpha_i),  sin(self.theta_i)*sin(self.alpha_i), self.r_i*cos(self.theta_i)],
            [sin(self.theta_i),  cos(self.theta_i)*cos(self.alpha_i), -cos(self.theta_i)*sin(self.alpha_i), self.r_i*sin(self.theta_i)],
            [0,                  sin(self.alpha_i),                   cos(self.alpha_i),                  self.d_i],
            [0,                  0,                                   0,                                  1]
        ])
        # Simplified generic DH matrix
        self.DH_simplified = simplify(self.DH_generic)

    def preview_matrix(self, matrix, filename, dvioptions=['-D', '300']):
        preview(matrix, viewer='file', filename=filename, dvioptions=dvioptions)

    def compute(self, thetas, alphas, rs, ds):
        A_mats = []
        for theta, alpha, r, d in zip(thetas, alphas, rs, ds):
            A = self.DH_generic.subs({
                self.theta_i: theta,
                self.alpha_i: alpha,
                self.r_i: r,
                self.d_i: d
            })
            A_mats.append(A)

        # Compute raw overall transform A0_n
        A_total = A_mats[0]
        for mat in A_mats[1:]:
            A_total = A_total * mat
        # Simplified overall transform
        A_total_simplified = trigsimp(A_total)

        return A_mats, A_total, A_total_simplified

if __name__ == "__main__":
    # Instantiate the calculator
    calc = GenerateMatrices()

    # Preview the generic simplified DH matrix
    calc.preview_matrix(calc.DH_simplified, "out.png")

    # Define specific parameters for a 3-joint planar robot
    theta_values = [Symbol("theta_1"), Symbol("theta_2"), Symbol("theta_3")]
    alpha_values = [pi/2, 0, 0]
    r_values     = [0, Symbol("r_2"), Symbol("r_3")]
    d_values     = [0, 0, 0]

    # Compute A0_1, A1_2, A2_3, A0_3 and its simplified form
    A_mats, A0_3, A0_3_simplified = calc.compute(theta_values, alpha_values, r_values, d_values)
    A0_1, A1_2, A2_3 = A_mats

    # Preview individual A matrices
    calc.preview_matrix(A0_1, "A0_1.png")
    calc.preview_matrix(A1_2, "A1_2.png")
    calc.preview_matrix(A2_3, "A2_3.png")

    # Preview overall transforms
    calc.preview_matrix(A0_3, "A0_3.png")
    calc.preview_matrix(A0_3_simplified, "A0_3_simplified.png")
