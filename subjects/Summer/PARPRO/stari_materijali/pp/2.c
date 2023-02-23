#include <stdio.h>
#include <stdlib.h>

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

const int N = 1024;
// int A[N], B[N], C[N];

#define MAX_SOURCE_SIZE (0x100000)

// https://www.eriksmistad.no/getting-started-with-opencl-and-gpu-computing/ korišten

int main(void)
{
    float *C = (float *)malloc(sizeof(float) * N);

    for (int i = 0; i < N; i++)
        C[0] = 0.;

    FILE *fp;
    char *source_str;
    size_t source_size;

    fp = fopen("pi.cl", "r");
    if (!fp)
    {
        fprintf(stderr, "Failed to load kernel.\n");
        exit(1);
    }

    source_str = (char *)malloc(MAX_SOURCE_SIZE);
    source_size = fread(source_str, 1, MAX_SOURCE_SIZE, fp);
    fclose(fp);

    cl_platform_id platform_id = NULL;
    cl_device_id device_id = NULL;
    cl_uint ret_num_devices;
    cl_uint ret_num_platforms;

    cl_int ret = clGetPlatformIDs(1, &platform_id, &ret_num_platforms);
    ret = clGetDeviceIDs(platform_id, CL_DEVICE_TYPE_DEFAULT, 1,
                         &device_id, &ret_num_devices);

    // printf("%d aaa %d\n", ret, ret_num_devices);

    cl_context context = clCreateContext(NULL, 1, &device_id, NULL, NULL, &ret);

    cl_command_queue command_queue = clCreateCommandQueue(context, device_id, 0, &ret);

    cl_mem c_mem_obj = clCreateBuffer(context, CL_MEM_WRITE_ONLY,
                                      N * sizeof(float), NULL, &ret);

    cl_program program = clCreateProgramWithSource(context, 1,
                                                   (const char **)&source_str,
                                                   (const size_t *)&source_size,
                                                   &ret);

    ret = clBuildProgram(program, 1, &device_id, NULL, NULL, NULL);

    cl_kernel kernel = clCreateKernel(program, "pi", &ret);

    cl_int n = 100000000;

    ret = clSetKernelArg(kernel, 0, sizeof(cl_mem), (void *)&c_mem_obj);
    ret = clSetKernelArg(kernel, 1, sizeof(cl_int), (void *)&n);

    size_t global_item_size = N;
    size_t G = 64;

    ret = clEnqueueNDRangeKernel(command_queue, kernel, 1, NULL,
                                 &global_item_size, &G, 0, NULL, NULL);
    // printf("aaa %d\n", ret);

    ret = clEnqueueReadBuffer(command_queue, c_mem_obj, CL_TRUE, 0,
                              N * sizeof(float), C, 0, NULL, NULL);

    double sum = 0;
    for (int i = 0; i < N; i++)
        sum += C[i];

    printf("%f\n", sum);

    // Clean up
    ret = clFlush(command_queue);
    ret = clFinish(command_queue);
    ret = clReleaseKernel(kernel);
    ret = clReleaseProgram(program);
    ret = clReleaseMemObject(c_mem_obj);
    ret = clReleaseCommandQueue(command_queue);
    ret = clReleaseContext(context);

    free(C);

    return 0;
}