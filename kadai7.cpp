#define _CRT_SECURE_NO_WARNINGS 
#include <stdio.h>

int main() {
    FILE* fp = fopen("data_q5.csv", "w");
    if (fp == NULL) {
        printf("Error: Could not create data_q5.csv.\n");
        return 1;
    }
    double m = 5.0;
    double C = 2.0;
    double K_spring = 10.0;

    //acurator
    double T = 0.1;

    double natural_len = 0.2;
    double K1 = 40.0;  
    double K2 = 10.0;  
    double K3 = 20.0;  

    //simulation variables 
    double t = 0.0;
    double dt = 0.01;
    double time_end = 40.0;

    double xp = 0.2;
    double v = 0.0;
    double F = 0.0;

    double target = 0.3;
    double u = 0.0;
    double ep = 0.0;
    double ei = 0.0;

    fprintf(fp, "Time,u,xp\n");
    printf("Simulation Q5 (Fast Actuator) started.\n");
    printf("Gains: K1=%.1f, K2=%.1f, K3=%.1f, T=%.1f\n", K1, K2, K3, T);

    while (t <= time_end) {
        //PID
        ep = target - xp;
        ei = ei + ep * dt;
        u = K1 * ep + K2 * ei - K3 * v;

        //Actuator 
        double dF = (u - F) / T * dt;
        F = F + dF;

        //System 
        double f_spring = K_spring * (xp - natural_len);
        double f_damping = C * v;
        double a = (F - f_spring - f_damping) / m;

        v = v + a * dt;
        xp = xp + v * dt;

        if ((int)((t / dt) + 0.001) % 10 == 0) {
            fprintf(fp, "%.2f,%.4f,%.4f\n", t, u, xp);
        }

        t = t + dt;
    }

    fclose(fp);
    printf("Finished. Check data_q5.csv\n");
    return 0;

}
