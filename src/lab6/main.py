import numpy as np
import scipy.integrate as si
import matplotlib.pyplot as plt

def func(y, t):
    C1 = 5e-6
    C2 = 5e-6
    C3 = 4e-6
    C4 = 6e-6

    L1 = 1e-2
    L2 = 2e-2
    L3 = 2e-2

    R1 = 7
    R2 = 7
    R3 = 8
    R4 = 9

    U = 10

    Q1, Q2, Q3, I1, I2, I3 = y

    return [
        I1,
        I2,
        I3,
        (U + (I3 - I1) * R3 - Q1 / C1 - I1 * R1) / L2,
        (U - Q2 / C3 - Q2 / C4) / L3,
        (I3 * R1 + Q3 / C2 + I3 * R2 + (I3 - I1) * R3) / -L1
    ]

def main():
    t = np.arange(0, 0.015, 0.00001)
    y0 = [0, 0, 0, 0, 0, 0]
    solution = si.odeint(func, y0, t)

    plt.plot(t, solution[:, 3], 'r', label='I1(t)')
    plt.plot(t, solution[:, 4], 'g', label='I2(t)')
    plt.plot(t, solution[:, 5], 'b', label='I3(t)')

    plt.legend(loc='best')
    plt.xlabel('t')
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()

