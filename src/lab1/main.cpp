#include <algorithm>
#include <iostream>
#include <iomanip>

#define PI 3.141592654
#define g 9.81
#define k1 5000.0
#define k2 7000.0
#define I 5.0
#define R 1.0
#define r 0.2
#define m 10.0
#define es 0.00001

struct result {
    double angle;
    double P;
};

result getAngle(double P) {
    double angle = (180.0 * R * (m * g + P)) / (PI * r * r * k1);

    return (result) {angle, P };   
}

double getY(double angle, double P) {
    return (angle * PI * R) / 180.0 + (m * g + P) / k2;
}

int main() {
    double P = 0;
    double stepP = 100.0;

    std::cout << std::setw(15) << "P" << "    " << std::setw(15) << "angle" << "    " << std::setw(15) << "Y" << std::endl;
    while (stepP > es) {
        result res = getAngle(-P);
        
        std::cout << std::setw(15) << res.P << "    " << std::setw(15) << res.angle << "    " << std::setw(15) << getY(res.angle, res.P) << std::endl;

        if (res.angle > 0)
            P += stepP;
        else {
            P -= stepP;
            stepP /= 2;
            P += stepP;
        } 
    }
}