#define _CRT_SECURE_NO_WARNINGS // This line fixes the 'fopen' error in Visual Studio
#include <stdio.h>

// Function to run the simulation and save to a CSV file
void simulate(const char* filename, double k_v, double k_x) {
    // Physical Parameters from the image
    double m = 5.0;     // mass [kg]
    double c = 2.0;     // damping [Ns/m]
    double k = 10.0;    // spring [N/m]

    // Initial Conditions (given in Q3: x = 0.1)
    double x = 0.1;     // position [m]
    double v = 0.0;     // velocity [m/s]
    double F = 0.0;     // force [N]

    // Time settings
    double t = 0.0;
    double dt = 0.001;  // Step size (smaller is more accurate)
    double t_end = 10.0; // Simulate for 10 seconds

    FILE* fp = fopen(filename, "w");
    if (fp == NULL) {
        printf("Error opening file %s\n", filename);
        return;
    }

    // Write Header
    fprintf(fp, "Time,Position,Velocity,Force\n");

    while (t <= t_end) {
        // 1. Calculate Control Force: F = -Kx = -(k_v * v + k_x * x)
        F = -(k_v * v + k_x * x);

        // 2. Physics Equations (Euler Method)
        // a = F_total / m = (F_input - F_damping - F_spring) / m
        double dv = (F - (c * v) - (k * x)) / m;
        double dx = v;

        // 3. Update states
        v = v + dv * dt;
        x = x + dx * dt;
        t = t + dt;

        // 4. Save data every 0.01 seconds to keep file small
        if ((int)(t * 1000) % 10 == 0) {
            fprintf(fp, "%.3f,%.6f,%.6f,%.6f\n", t, x, v, F);
        }
    }

    fclose(fp);
    printf("Successfully created: %s\n", filename);
}

int main() {
    printf("Starting Simulations...\n\n");

    // Case 1: F = 0 (No control)
    simulate("response_F0.csv", 0.0, 0.0);

    // NOTE: You must replace these K values with the results you get from 
    // MATLAB's lqr(A,B,Q,R) command in Question (2).
    // K = [k_velocity, k_position]

    // Example values (Replace these with your actual MATLAB results):
    simulate("response_K1.csv", 33.7, 490.0);  // K1 result
    simulate("response_K2.csv", 497.1, 103.0); // K2 result
    simulate("response_K3.csv", 355.0, 439.4); // K3 result
    simulate("response_K4.csv", 4.90, 6.24);   // K4 result

    printf("\nAll simulations complete. Use Excel to graph the .csv files.\n");
    return 0;
}