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
    int *A = (int *)malloc(sizeof(int) * N);
    int *C = (int *)malloc(sizeof(int) * N);

    for (int i = 0; i < N; i++)
    {
        A[i] = i;
        C[0] = 0;
    }

    FILE *fp;
    char *source_str;
    size_t source_size;

    fp = fopen("vector_add_kernel.cl", "r");
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

    printf("%d\n", ret);

    // printf("%d aaa %d\n", ret, ret_num_devices);

    cl_context context = clCreateContext(NULL, 1, &device_id, NULL, NULL, &ret);

    cl_command_queue command_queue = clCreateCommandQueue(context, device_id, 0, &ret);

    cl_mem a_mem_obj = clCreateBuffer(context, CL_MEM_READ_ONLY,
                                      N * sizeof(int), NULL, &ret);
    cl_mem c_mem_obj = clCreateBuffer(context, CL_MEM_WRITE_ONLY,
                                      N * sizeof(int), NULL, &ret);

    ret = clEnqueueWriteBuffer(command_queue, a_mem_obj, CL_TRUE, 0,
                               N * sizeof(int), A, 0, NULL, NULL);
    printf("%d\n", ret);

    cl_program program = clCreateProgramWithSource(context, 1,
                                                   (const char **)&source_str,
                                                   (const size_t *)&source_size,
                                                   &ret);

    ret = clBuildProgram(program, 1, &device_id, NULL, NULL, NULL);
    printf("%d\n", ret);

    cl_kernel kernel = clCreateKernel(program, "vector_add", &ret);

    ret = clSetKernelArg(kernel, 0, sizeof(cl_mem), (void *)&a_mem_obj);
    printf("%d\n", ret);

    ret = clSetKernelArg(kernel, 1, sizeof(cl_mem), (void *)&c_mem_obj);
    printf("%d\n", ret);

    int *cnt = (int *)malloc(sizeof(int));

    *cnt = 0;

    cl_mem cnt_buf = clCreateBuffer(context,
                                    CL_MEM_READ_WRITE | CL_MEM_USE_HOST_PTR,
                                    sizeof(int),
                                    (void *)&cnt,
                                    &ret);

    printf("aa%d\n", ret);

    ret = clSetKernelArg(kernel, 2, sizeof(cl_mem), (void *)&cnt_buf);
    printf("aa%d\n", ret);

    size_t global_item_size = N;
    size_t G = 64;
    ret = clEnqueueNDRangeKernel(command_queue, kernel, 1, NULL,
                                 &global_item_size, &G, 0, NULL, NULL);
    printf("%d\n", ret);
    // printf("aaa %d\n", ret);

    ret = clEnqueueReadBuffer(command_queue, c_mem_obj, CL_TRUE, 0,
                              N * sizeof(int), C, 0, NULL, NULL);
    ret = clEnqueueReadBuffer(command_queue, cnt_buf, CL_TRUE, 0,
                              sizeof(int), cnt, 0, NULL, NULL);
    printf("asds%d\n", ret);

    for (int i = 0; i < N; i++)
        printf("%d => %d\n", A[i], C[i]);

    printf("GPU cnt = %d\n", *cnt);

    // Clean up
    ret = clFlush(command_queue);
    ret = clFinish(command_queue);
    ret = clReleaseKernel(kernel);
    ret = clReleaseProgram(program);
    ret = clReleaseMemObject(a_mem_obj);
    ret = clReleaseMemObject(c_mem_obj);
    ret = clReleaseCommandQueue(command_queue);
    ret = clReleaseContext(context);

    free(A);
    free(C);

    return 0;
}