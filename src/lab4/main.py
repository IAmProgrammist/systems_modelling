import math
import matplotlib.pyplot as plt

dt = ((20.0) / (30000.0))
PI = 3.141592654
g = 9.81
k1 = 5000.0
k2 = 7000.0
I = 5.0
R = 1.0
r = 0.2
m = 10

'''
Ну привет, путешественник на пути к сдаче сисмода. Если хочешь получить ахахахашки здесь, попробуй поставить вот 
такие значения: 

k1 = 50000.0
k2 = 7.0
m = 20

Возможно я уже просто сошёл с ума к тому моменту, но меня нехило пробрало на шепот в голосину с этого
'''

def degreeToRadians(angle):
    return angle * (PI / 180.0)

def getAngleAcc(angle, y):
    return ((PI * PI * k1 * r * r * angle) / 32400.0 - (PI * k2 * R * (y - (angle * PI * R) / 180.0)) / 180.0) / -I

def getAngleVel(w):
    return w

def getYAcc(y, angle):
    return g + (k2 * (y - angle * PI * R / 180)) / -m

def getY(v):
    return v

angle = 0
aV = 0.0

y = 0.0
yV = 0.0

x_plot = list()
y_plot = list()
angle_plot = list()

t = 0.0
while t < 100:
    aVk1 = getAngleAcc(angle, y)
    aVk2 = getAngleAcc(angle + (dt/2) * aVk1, y + dt/2)
    aVk3 = getAngleAcc(angle + (dt/2) * aVk2, y + dt/2)
    aVk4 = getAngleAcc(angle + dt * aVk3, y + dt)
    aV += (dt/6) * (aVk1 + 2 * aVk2 + 2 * aVk3 + aVk4)
    
    # Recalc angle
    ak1 = getAngleVel(aV)
    ak2 = getAngleVel(aV + (dt/2) * ak1)
    ak3 = getAngleVel(aV + (dt/2) * ak2)
    ak4 = getAngleVel(aV + dt * ak3)
    angle += (dt/6) * (ak1 + 2 * ak2 + 2 * ak3 + ak4)
    
    # Recalc yV
    yVk1 = getYAcc(y, angle)
    yVk2 = getYAcc(y + (dt/2) * yVk1, angle + dt/2)
    yVk3 = getYAcc(y + (dt/2) * yVk2, angle + dt/2)
    yVk4 = getYAcc(y + dt * yVk3, angle + dt)
    yV += (dt/6) * (yVk1 + 2 * yVk2 + 2 * yVk3 + yVk4)
    
    # Recalc y
    yk1 = getY(yV)
    yk2 = getY(yV + (dt/2) * yk1)
    yk3 = getY(yV + (dt/2) * yk2)
    yk4 = getY(yV + dt * yk3)
    y += (dt/6) * (yk1 + 2 * yk2 + 2 * yk3 + yk4)

    x_plot.append(t)
    y_plot.append(y)
    angle_plot.append(angle)
    t += dt

# Визуализация
fig, (angle, y) = plt.subplots(2)
y.plot(x_plot, y_plot, 'r-', label='Отклонение')
angle.plot(x_plot, angle_plot, 'g-', label='Угол')
y.set_title('Координата y')
angle.set_title('Угол')
y.grid(True)
angle.grid(True)
plt.show()