import math
import matplotlib.pyplot as plt

dt = 0.00001
PI = 3.141592654
g = 9.81
k1 = 10000.0
k2 = 20000.0
I = 2
m1 = 5
m2 = 15
L = 1

a = 1
C1 = 2e-6
C2 = 1e-5
R1 = 200
R2 = 100
E = 10
I0 = 0
L0 = 5e-2
qDelta = 0.05

def getdldx(x):
    return a if x < 0 else -a

def getlx(x):
    return L0 - a * math.fabs(x) if math.fabs(x) <= qDelta else 0

# Нелианеризованная версия функции
# def getAngleAcc(angle, angleV, x, xV):
#    return (k2 * L * math.cos(angle) * (L * math.sin(angle) - x) + (g * L * m1 * math.cos(angle)) / 2) / -I

def getAngleAcc(angle, angleV, x, xV):
    return (k2 * L * (L * (angle) - x) + (g * L * m1) / 2) / -I

def getAngleVel(w):
    return w

# Нелианеризованная версия функции
#def getXAcc(x, xV, angle, angleV):
#    return (k1 * x - k2 * (L * math.sin(angle) - x)) / -m2

def getXAcc(x, xV, angle, angleV):
    return (k1 * x - k2 * (L * (angle) - x)) / -m2

def getX(v):
    return v

def getQ1V(Q1, I2):
    return (E + I2 * R1 - Q1/C2) / (R2 + R1)

def getQ2Acc(I1, I2, Q2, x, xV):
    return (Q2 / C1 + getdldx(x) * xV * (I0 + I2) + (I2 - I1) * R1) / (-getlx(x))

def getQ2V(I2):
    return I2

x_c_plot = list([0])
x_plot = list([0.03])
xV_plot = list([0.0])
a_plot = list([0.0])
aV_plot = list([0.0])
I1_plot = list([0.0])
Q1_plot = list([0.0])
I2_plot = list([0.0])
Q2_plot = list([0.0])
U_plot = list([0.0])

t = dt
while t < 2:
    # Recalc I2V
    I2k1 = getQ2Acc(I1_plot[-1],          I2_plot[-1],                   Q2_plot[-1],          x_plot[-1],          xV_plot[-1])
    I2k2 = getQ2Acc(I1_plot[-1] + dt / 2, I2_plot[-1] + (dt / 2) * I2k1, Q2_plot[-1] + dt / 2, x_plot[-1] + dt / 2, xV_plot[-1] + dt / 2)
    I2k3 = getQ2Acc(I1_plot[-1] + dt / 2, I2_plot[-1] + (dt / 2) * I2k2, Q2_plot[-1] + dt / 2, x_plot[-1] + dt / 2, xV_plot[-1] + dt / 2)
    I2k4 = getQ2Acc(I1_plot[-1] + dt,     I2_plot[-1] + dt * I2k3,       Q2_plot[-1] + dt,     x_plot[-1] + dt,     xV_plot[-1] + dt)
    I2 = I2_plot[-1] + (dt / 6) * (I2k1 + 2 * I2k2 + 2 * I2k3 + I2k4)

    # Recalc I2
    Q2k1 = getQ2V(I2_plot[-1])
    Q2k2 = getQ2V(I2_plot[-1] + (dt / 2) * Q2k1)
    Q2k3 = getQ2V(I2_plot[-1] + (dt / 2) * Q2k2)
    Q2k4 = getQ2V(I2_plot[-1] + dt * Q2k3)
    Q2 = Q2_plot[-1] + (dt / 6) * (Q2k1 + 2 * Q2k2 + 2 * Q2k3 + Q2k4)

    # Recalc I1
    I1 = getQ1V(Q1_plot[-1], I2_plot[-1])

    # Recalc Q1
    Q1k1 = getQ1V(Q1_plot[-1],          I2_plot[-1])
    Q1k2 = getQ1V(Q1_plot[-1] + dt / 2, I2_plot[-1] + dt / 2)
    Q1k3 = getQ1V(Q1_plot[-1] + dt / 2, I2_plot[-1] + dt / 2)
    Q1k4 = getQ1V(Q1_plot[-1] + dt,     I2_plot[-1] + dt)
    Q1 = Q1_plot[-1] + (dt / 6) * (Q1k1 + 2 * Q1k2 + 2 * Q1k3 + Q1k4)

    # Recalc aV
    aVk1 = getAngleAcc(a_plot[-1],                   aV_plot[-1], x_plot[-1], xV_plot[-1])
    aVk2 = getAngleAcc(a_plot[-1] + (dt / 2) * aVk1, aV_plot[-1], x_plot[-1] + dt / 2, xV_plot[-1])
    aVk3 = getAngleAcc(a_plot[-1] + (dt / 2) * aVk2, aV_plot[-1], x_plot[-1] + dt / 2, xV_plot[-1])
    aVk4 = getAngleAcc(a_plot[-1] + dt * aVk3,       aV_plot[-1], x_plot[-1] + dt, xV_plot[-1])
    aV = aV_plot[-1] + (dt/6) * (aVk1 + 2 * aVk2 + 2 * aVk3 + aVk4)

    # Recalc angle
    ak1 = getAngleVel(aV_plot[-1])
    ak2 = getAngleVel(aV_plot[-1] + (dt/2) * ak1)
    ak3 = getAngleVel(aV_plot[-1] + (dt/2) * ak2)
    ak4 = getAngleVel(aV_plot[-1] + dt * ak3)
    angle = a_plot[-1] + (dt / 6) * (ak1 + 2 * ak2 + 2 * ak3 + ak4)

    # Recalc yV
    xVk1 = getXAcc(x_plot[-1], xV_plot[-1], a_plot[-1], aV_plot[-1])
    xVk2 = getXAcc(x_plot[-1] + (dt / 2) * xVk1, xV_plot[-1], a_plot[-1] + dt / 2, aV_plot[-1])
    xVk3 = getXAcc(x_plot[-1] + (dt / 2) * xVk2, xV_plot[-1], a_plot[-1] + dt / 2, aV_plot[-1])
    xVk4 = getXAcc(x_plot[-1] + dt * xVk3, xV_plot[-1], a_plot[-1] + dt, aV_plot[-1])
    xV = xV_plot[-1] + (dt / 6) * (xVk1 + 2 * xVk2 + 2 * xVk3 + xVk4)

    # Recalc y
    xk1 = getX(xV_plot[-1])
    xk2 = getX(xV_plot[-1] + (dt / 2) * xk1)
    xk3 = getX(xV_plot[-1] + (dt / 2) * xk2)
    xk4 = getX(xV_plot[-1] + dt * xk3)
    x = x_plot[-1] + (dt / 6) * (xk1 + 2 * xk2 + 2 * xk3 + xk4)

    x_c_plot.append(t)
    x_plot.append(x)
    xV_plot.append(xV)
    a_plot.append(angle)
    aV_plot.append(aV)
    I1_plot.append(I1)
    Q1_plot.append(Q1)
    I2_plot.append(I2)
    Q2_plot.append(Q2)
    U_plot.append(I1 * R2)
    t += dt

x_c_plot = x_c_plot[int(.1 / dt):]
a_plot = a_plot[int(.1 / dt):]
x_plot = x_plot[int(.1 / dt):]
I1_plot = I1_plot[int(.1 / dt):]
I2_plot = I2_plot[int(.1 / dt):]
U_plot = U_plot[int(.1 / dt):]

# Визуализация

fig, (angle, y, I1_p, I2_p, U_p) = plt.subplots(5)
y.plot(x_c_plot, x_plot, 'r-', label='Отклонение')
angle.plot(x_c_plot, a_plot, 'g-', label='Угол')
I1_p.plot(x_c_plot, I1_plot, 'b-', label='I1')
I2_p.plot(x_c_plot, I2_plot, 'r-', label='I2')
U_p.plot(x_c_plot, U_plot, 'g-', label='U')
y.set_title('Координата x')
angle.set_title('Угол')
I1_p.set_title('Ток I1')
I2_p.set_title('Ток I2')
U_p.set_title('Вольтметр')
y.grid(True)
angle.grid(True)
I1_p.grid(True)
I2_p.grid(True)
U_p.grid(True)
plt.show()

