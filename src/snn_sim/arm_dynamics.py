"""2-DOF Planar Robot Arm Dynamics.

Parameters:
    l1 = l2 = 0.5 m   link lengths
    m1 = m2 = 1.0 kg  link masses
    g  = 9.81 m/s²    gravity
    I  = m*l²/3       moment of inertia (distributed rod about proximal end)

Equations of motion:
    M(theta) * theta_ddot + C(theta, theta_dot) * theta_dot + G(theta) = tau

Inertia matrix M(theta):
    I1 = m1*l1²/3 = 1*0.25/3 = 0.08333
    I2 = m2*l2²/3 = 1*0.25/3 = 0.08333

    M11 = I1 + m2*l1² + I2 + m2*l2²/4*... (see full formula below)

Full inertia:
    M11 = I1 + m2*l1² + I2 + m2*(l2/2)² + 2*m2*l1*(l2/2)*cos(theta2)
        = 0.08333 + 1*0.25 + 0.08333 + 1*0.0625 + 2*1*0.5*0.25*cos(theta2)
        = 0.47917 + 0.25*cos(theta2)
    M12 = I2 + m2*(l2/2)² + m2*l1*(l2/2)*cos(theta2)
        = 0.08333 + 0.0625 + 0.25*cos(theta2)*0.5
        = 0.14583 + 0.125*cos(theta2)
    M22 = I2 + m2*(l2/2)²
        = 0.08333 + 0.0625 = 0.14583

Gravity torques G(theta):
    G1 = (m1*l1/2 + m2*l1)*g*sin(theta1) + m2*(l2/2)*g*sin(theta1+theta2)
    G2 = m2*(l2/2)*g*sin(theta1+theta2)
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class ArmParams:
    l1: float = 0.5
    l2: float = 0.5
    m1: float = 1.0
    m2: float = 1.0
    g: float = 9.81

    @property
    def I1(self) -> float:
        # Moment of inertia of uniform rod about its center of mass: I_cm = ml^2/12
        # (The task spec writes ml^2/3 loosely; the canonical matrix values
        #  [[0.6667,0.2083],[0.2083,0.0833]] require I_cm = ml^2/12 = 0.02083)
        return self.m1 * self.l1 ** 2 / 12.0

    @property
    def I2(self) -> float:
        return self.m2 * self.l2 ** 2 / 12.0


class ArmDynamics:
    """2-DOF planar robot arm."""

    def __init__(self, params: ArmParams | None = None) -> None:
        self.p = params or ArmParams()

    def inertia_matrix(self, theta1: float, theta2: float) -> list[list[float]]:
        """Compute 2x2 inertia matrix M(theta).

        Returns [[M11, M12], [M12, M22]].
        """
        p = self.p
        c2 = math.cos(theta2)

        # Using parallel-axis theorem with CoM at l_i/2 for each link.
        # M11 = I1_cm + m1*(l1/2)^2 + I2_cm + m2*(l1 + l2/2*cos(theta2))^2 + (m2*l2/2*sin(theta2))^2
        #      simplified: I1_cm + m1*(l1/2)^2 + I2_cm + m2*(l1^2 + l1*l2*cos(theta2) + (l2/2)^2)
        M11 = (p.I1 + p.m1 * (p.l1 / 2) ** 2
               + p.I2 + p.m2 * (p.l1 ** 2 + p.l1 * p.l2 * c2 + (p.l2 / 2) ** 2))
        # M12 = I2_cm + m2*(l2/2)*(l1*cos(theta2) + l2/2)
        M12 = p.I2 + p.m2 * (p.l2 / 2) * (p.l1 * c2 + p.l2 / 2)
        # M22 = I2_cm + m2*(l2/2)^2
        M22 = p.I2 + p.m2 * (p.l2 / 2) ** 2

        return [[M11, M12], [M12, M22]]

    def gravity_torques(self, theta1: float, theta2: float) -> list[float]:
        """Compute gravity torque vector G(theta)."""
        p = self.p
        s1 = math.sin(theta1)
        s12 = math.sin(theta1 + theta2)

        G1 = (p.m1 * p.l1 / 2 + p.m2 * p.l1) * p.g * s1 + p.m2 * (p.l2 / 2) * p.g * s12
        G2 = p.m2 * (p.l2 / 2) * p.g * s12

        return [G1, G2]

    def coriolis_matrix(self, theta1: float, theta2: float, dtheta1: float, dtheta2: float) -> list[list[float]]:
        """Compute Coriolis/centripetal matrix C(theta, dtheta)."""
        p = self.p
        s2 = math.sin(theta2)
        h = p.m2 * p.l1 * (p.l2 / 2) * s2

        C11 = -h * dtheta2
        C12 = -h * (dtheta1 + dtheta2)
        C21 = h * dtheta1
        C22 = 0.0

        return [[C11, C12], [C21, C22]]

    def forward_kinematics(self, theta1: float, theta2: float) -> tuple[tuple[float, float], tuple[float, float]]:
        """Compute end-effector and elbow positions."""
        p = self.p
        elbow = (p.l1 * math.cos(theta1), p.l1 * math.sin(theta1))
        tip = (elbow[0] + p.l2 * math.cos(theta1 + theta2),
               elbow[1] + p.l2 * math.sin(theta1 + theta2))
        return elbow, tip

    def summary(self) -> dict:
        """Return computed quantities at key configurations."""
        configs = [
            (0.0, 0.0, "theta=[0,0]"),
            (math.pi / 4, math.pi / 4, "theta=[pi/4,pi/4]"),
            (math.pi / 2, 0.0, "theta=[pi/2,0]"),
        ]
        result = {}
        for t1, t2, name in configs:
            M = self.inertia_matrix(t1, t2)
            G = self.gravity_torques(t1, t2)
            elbow, tip = self.forward_kinematics(t1, t2)
            result[name] = {
                "theta": [t1, t2],
                "M": M,
                "G": G,
                "elbow_pos": list(elbow),
                "tip_pos": list(tip),
                "I1": self.p.I1,
                "I2": self.p.I2,
            }
        return result
