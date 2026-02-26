#define _CRT_SECURE_NO_WARNINGS // This line fixes the 'fopen' error in Visual Studio
#include <stdio.h>

//CVS file
void simulate(const char* filename, double k_v, double k_x) {
    //paramenter
    double m = 5.0;    
    double c = 2.0;     
    double k = 10.0;   

    //Initial
    double x = 0.1;     
    double v = 0.0;    
    double F = 0.0;    

    //Time 
    double t = 0.0;
    double dt = 0.001;  
    double t_end = 10.0; 

    FILE* fp = fopen(filename, "w");
    if (fp == NULL) {
        printf("Error opening file %s\n", filename);
        return;
    }

    fprintf(fp, "Time,Position,Velocity,Force\n");

    while (t <= t_end) {
        //Control Force
        F = -(k_v * v + k_x * x);

        //Euler
        double dv = (F - (c * v) - (k * x)) / m;
        double dx = v;

        v = v + dv * dt;
        x = x + dx * dt;
        t = t + dt;
        if ((int)(t * 1000) % 10 == 0) {
            fprintf(fp, "%.3f,%.6f,%.6f,%.6f\n", t, x, v, F);
        }
    }

    fclose(fp);
    printf("Successfully created: %s\n", filename);
}

int main() {
    printf("Starting Simulations...\n\n");

    simulate("response_F0.csv", 0.0, 0.0);

    simulate("response_K1.csv", 33.7, 490.0);  
    simulate("response_K2.csv", 497.1, 103.0); 
    simulate("response_K3.csv", 355.0, 439.4); 
    simulate("response_K4.csv", 4.90, 6.24);   

    printf("\nAll simulations complete. Use Excel to graph the .csv files.\n");
    return 0;

}
