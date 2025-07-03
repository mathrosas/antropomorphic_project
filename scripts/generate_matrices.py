#!/usr/bin/env python3

from sympy import Matrix, cos, sin, Symbol, simplify, trigsimp, preview, pi
from sympy.interactive import printing


# To make display prety
printing.init_printing(use_latex = True)

theta_i = Symbol("theta_i")
alpha_i = Symbol("alpha_i")
r_i = Symbol("r_i")
d_i = Symbol("d_i")

DH_Matrix_Generic = Matrix([[cos(theta_i), -sin(theta_i)*cos(alpha_i), sin(theta_i)*sin(alpha_i), r_i*cos(theta_i)],
                            [sin(theta_i), cos(theta_i)*cos(alpha_i), -cos(theta_i)*sin(alpha_i), r_i*sin(theta_i)],
                            [0,            sin(alpha_i),               cos(alpha_i),              d_i],
                            [0,            0,                          0,                         1]])

result_simpl = simplify(DH_Matrix_Generic)

# Save to local file
preview(result_simpl, viewer='file', filename="out.png", dvioptions=['-D','300'])


# Now create A01, A12, A23

theta_1 = Symbol("theta_1")
theta_2 = Symbol("theta_2")
theta_3 = Symbol("theta_3")


alpha_planar = 0.0

alpha_1 = pi / 2
alpha_2 = alpha_planar
alpha_3 = alpha_planar

r_planar = 0.0

r_1 = r_planar
r_2 = Symbol("r_2")
r_3 = Symbol("r_3")

d_planar = 0.0

d_1 = d_planar
d_2 = d_planar
d_3 = d_planar

A0_1 = DH_Matrix_Generic.subs(r_i,r_1).subs(alpha_i,alpha_1).subs(d_i,d_1).subs(theta_i, theta_1)
A1_2 = DH_Matrix_Generic.subs(r_i,r_2).subs(alpha_i,alpha_2).subs(d_i,d_2).subs(theta_i, theta_2)
A2_3 = DH_Matrix_Generic.subs(r_i,r_3).subs(alpha_i,alpha_3).subs(d_i,d_3).subs(theta_i, theta_3)

A0_3 = A0_1 * A1_2 * A2_3
A0_3_simplified = trigsimp(A0_3)

# We save

preview(A0_1, viewer='file', filename="A0_1.png", dvioptions=['-D','300'])
preview(A1_2, viewer='file', filename="A1_2.png", dvioptions=['-D','300'])
preview(A2_3, viewer='file', filename="A2_3.png", dvioptions=['-D','300'])
preview(A0_3, viewer='file', filename="A0_3.png", dvioptions=['-D','300'])
preview(A0_3_simplified, viewer='file', filename="A0_3_simplified.png", dvioptions=['-D','300'])

# A0_2 = A0_1 * A1_2
# A0_2_simplified = trigsimp(A0_2)
# preview(A0_2, viewer='file', filename="A0_2.png", dvioptions=['-D','300'])
# preview(A0_2_simplified, viewer='file', filename="A0_2_simplified.png", dvioptions=['-D','300'])

# Added for IK
# A0_2 = A0_1 * A1_2
# A0_2_simplified = trigsimp(A0_2)
# preview(A02, viewer='file', filename="A0_2.png", dvioptions=['-D','300'])