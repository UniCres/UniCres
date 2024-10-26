import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Environment Constants
rho0 = 1.293  # kg/m^3 - air density at sea level
Re = 6378137  # m - radius of Earth
hscale = 8400  # m - scale height
g0 = 9.8  # m/s^2 - gravitational acceleration at Earth's surface
deg = np.pi / 180  # Conversion factor for degrees to radians
omega = 7.2921159e-5  # rad/s - Earth's rotation rate


class Rocket():
    def __init__(self):
        self.diameter = 3.05 # m
        self.frontArea = (np.pi / 4) * diam**2 # m^2
        self.dragCoefficient = 0.3
        self.propellantMass = 111130 # kg
        self.payloadMass = 32000 # kg
        self.structureMass = 6736 # kg
        self.m0 = self.propellantMass + self.payloadMass + self.structureMass # kg
        self.burnTime = 350 # kg
        self. massFlowRate = self.propellantMass / self.burnTime # kg/s
        self.thrust = 1900000 # N
        self.pitchoverAltitude = 1000 # m

# Rocket Inputs
diam = 3.05  # m - rocket diameter
A = (np.pi / 4) * diam**2  # m^2 - front area
CD = 0.3  # drag coefficient
mprop = 111130  # kg - propellant mass
mpl = 32000  # kg - payload mass
mstruc = 6736  # kg - structure mass
m0 = mprop + mpl + mstruc  # kg - liftoff mass
tburn = 356  # s - burn time
m_dot = mprop / tburn  # kg/s - mass flow rate
Thrust = 1900000  # N - thrust
hturn = 1000  # m - pitchover height

# Initial Conditions
t_max = 1400  # s - max simulation time
v0 = 0  # m/s - initial velocity
psi0 = 0.3 * deg  # radians - initial flight path angle
theta0 = 0  # radians
h0 = 0  # m - initial height

# Differential equation function
def derivatives(t, y):
    v = y[0]  # velocity
    psi = y[1]  # flight path angle
    theta = y[2]  # downrange angle
    h = y[3]  # altitude

    # Update gravity based on altitude
    g = g0 * (Re / (Re + h))**2

    # Calculate air density based on altitude
    rho = rho0 * np.exp(-h / hscale)
    rho = max(rho, 1e-5)  # Avoid rho going to zero

    # Calculate drag force
    D = 0.5 * rho * v**2 * A * CD

    # Update thrust and mass based on burn time
    if t < tburn:
        m = m0 - m_dot * t
        T = Thrust
    else:
        m = m0 - m_dot * tburn
        T = 0

    # Define differential equations
    if h <= hturn:
        psi_dot = 0
        v_dot = T / m - D / m - g
        theta_dot = 0
        h_dot = v
    else:
        phi_dot = g * np.sin(psi) / v
        v_dot = T / m - D / m - g * np.cos(psi)
        h_dot = v * np.cos(psi)
        theta_dot = v * np.sin(psi) / (Re + h)
        psi_dot = phi_dot - theta_dot

    return [v_dot, psi_dot, theta_dot, h_dot]

# Time evaluation points
t = np.linspace(0, t_max, 100000)

# Solve the differential equation
sol = solve_ivp(derivatives, [t[0], t[-1]], [v0, psi0, theta0, h0], t_eval=t)

# Extract results
vrel = sol.y[0] / 1000  # Convert velocity to km/s
vabs = vrel + Re * omega / 1000  # Absolute velocity considering Earth's rotation
psi = sol.y[1]
psideg = psi / deg  # Convert flight path angle to degrees
theta = sol.y[2]
theta_km = theta * Re / 1000  # Convert downrange distance to kilometers
altitude = sol.y[3] / 1000  # Convert altitude to kilometers


# Plotting
plt.figure(figsize=(12, 8))

# Velocity Plot
plt.subplot(4, 1, 1)
plt.plot(sol.t, vrel, label="Relative Velocity (km/s)")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (km/s)")
plt.legend()

    # Altitude Plot
plt.subplot(4, 1, 2)
plt.plot(sol.t, altitude, label="Altitude (km)", color="orange")
plt.xlabel("Time (s)")
plt.ylabel("Altitude (km)")
plt.legend()

    # Downrange Distance Plot
plt.subplot(4, 1, 3)
plt.plot(sol.t, theta_km, label="Downrange Distance (km)", color="purple")
plt.xlabel("Time (s)")
plt.ylabel("Distance (km)")
plt.legend()

    # Flight Path Angle Plot
plt.subplot(4, 1, 4)
plt.plot(sol.t, psideg, label="Flight Path Angle (degrees)", color="green")
plt.xlabel("Time (s)")
plt.ylabel("Angle (degrees)")
plt.legend()

plt.tight_layout()
print()
#plt.show()