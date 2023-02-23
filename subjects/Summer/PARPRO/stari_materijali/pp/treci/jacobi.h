//#include <nvtx3/nvToolsExt.h>

void cleanup();

void compile_open_cl(int n, int m);

void jacobistep(float *psinew, float *psi, int m, int n);

double deltasq(float *newarr, float *oldarr, int m, int n);
