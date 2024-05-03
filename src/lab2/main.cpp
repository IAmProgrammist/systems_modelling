#include <iostream>

#define dt ((20.0) / (30000.0))
#define PI 3.141592654
#define g 9.81
#define k1 5000.0
#define k2 7000.0
#define I 1.0
#define R 1.0
#define r 0.2
#define m 10.0
#define es 0.000001

double getAngleAcc(double angle) {
    return -(
    // M1
    (k1 * angle * PI * r * r) / 180.0 +
        
    // M2
    - (m*g) * R) / I;
}

double getAngleVel(double w) {
    return w;
}

double getYAcc(double y, double angle) {
    return (m * g - k2 * (y - angle * PI * R / 180.0)) / m;
}

double getY(double v) {
    return v;
}

int main() {
    double angle = 0.0;
    double aV = 0.0;

    double y = 0.0;
    double yV = 0.0;

    for (double t = 0.0; t < 40; t += dt) {
        // Recalc aV
        double aVk1 = getAngleAcc(angle);
        double aVk2 = getAngleAcc(angle + (dt/2) * aVk1);
        double aVk3 = getAngleAcc(angle + (dt/2) * aVk2);
        double aVk4 = getAngleAcc(angle + dt * aVk3);
        aV += (dt/6) * (aVk1 + 2 * aVk2 + 2 * aVk3 + aVk4);
        
        // Recalc angle
        double ak1 = getAngleVel(aV);
        double ak2 = getAngleVel(aV + (dt/2) * ak1);
        double ak3 = getAngleVel(aV + (dt/2) * ak2);
        double ak4 = getAngleVel(aV + dt * ak3);
        angle += (dt/6) * (ak1 + 2 * ak2 + 2 * ak3 + ak4);
        
        // Recalc yV
        double yVk1 = getYAcc(y, angle);
        double yVk2 = getYAcc(y + (dt/2) * yVk1, angle + dt/2);
        double yVk3 = getYAcc(y + (dt/2) * yVk2, angle + dt/2);
        double yVk4 = getYAcc(y + dt * yVk3, angle + dt);
        yV += (dt/6) * (yVk1 + 2 * yVk2 + 2 * yVk3 + yVk4);
        
        // Recalc y
        double yk1 = getY(yV);
        double yk2 = getY(yV + (dt/2) * yk1);
        double yk3 = getY(yV + (dt/2) * yk2);
        double yk4 = getY(yV + dt * yk3);
        y += (dt/6) * (yk1 + 2 * yk2 + 2 * yk3 + yk4);

        std::cout << t << " " << angle << " " << y << std::endl;
    }
}