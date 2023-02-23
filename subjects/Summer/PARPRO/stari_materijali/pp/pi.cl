__kernel void pi(__global float *C, int n) {
    int id = get_global_id(0);
    int numprocs = get_global_size(0);
    // int g = get_local_size(0);

    // int j = 0;

    if(id == 0)
        return;

    double h = 1.0 / (double)n, x;
    C[id] = 0.0;
    for (int i = id + 1; i <= n; i += numprocs)
    {
        x = h * ((double)i - 0.5);
        C[id] += 4.0 / (1.0 + x * x);
    }
    C[id] *= h;
}