__kernel void jacobistep(global float * in, global float * out, int n, int m) {
    // int id = get_global_id(0);
    // int numprocs = get_global_size(0);
    // int g = get_local_size(0);

    // int j = 0;

    

    int id = get_global_id(0);

    if(id >= (n + 1) * (m + 1))
        return;

    int j = id % (m + 1); 
    int i = id / (m + 1); 
        
    if(i == 0 || j == 0)
        return;

    out[i * (m + 2) + j] = 0.25 * (in[(i - 1) * (m + 2) + j] + in[(i + 1) * (m + 2) + j] + in[i * (m + 2) + j - 1] + in[i * (m + 2) + j + 1]);
    
    // int our_value = array[id];

}