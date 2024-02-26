#include <algorithm>
#include <iostream>

#define PI 3.141592654
#define g 9.81
#define k1 5000.0
#define k2 7000.0
#define I 5.0
#define R 1.0
#define r 0.2
#define m 100.0
#define e 0.0000000001
#define es 0.00001


double getM2(double P) {
    return -(m * g + P) * R;
}

double getM1(double angle) {
    return k1 * angle * PI * r * r / 180.0;
}

double getM(double angle, double P) {
    return getM1(angle) + getM2(P);
}

double getDeriative(double angle, double P) {
    return (getM(angle + e, P) - getM(angle, P)) / e;
}

double getDelta(double angle, double P) {
    return getM(angle, P) / getDeriative(angle, P);
}

struct result {
    double angle;
    bool succeed;
    double P;
};

result newton(double P) {
    double angle = 0;
    int c = 0;
    double delta = getDelta(angle, P);
    while (std::abs(getM(angle, P)) >= es && c < 100) {
        c++;
        angle -= delta;
        delta = getDelta(angle, P);
    }

    return (result) {angle, std::abs(getM(angle, P)) < es, P };   
}

int main() {
    double P = 0;
    double stepP = 100.0;

    while (stepP > es) {
        result res = newton(-P);
        
        std::cout << P << " " << res.angle << " " << res.succeed << std::endl;

        if (res.angle > 0)
            P += stepP;
        else {
            P -= stepP;
            stepP /= 2;
            P += stepP;
        } 
    }
}