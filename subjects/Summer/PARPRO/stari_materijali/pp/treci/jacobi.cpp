#include <stdio.h>

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

#include "jacobi.h"

#define MAX_SOURCE_SIZE (0x100000)

cl_platform_id platform_id = NULL;
cl_device_id device_id = NULL;
cl_uint ret_num_devices;
cl_uint ret_num_platforms;

cl_context context;
cl_command_queue command_queue;

cl_program program;
cl_kernel kernel;
cl_mem device_array_in;
cl_mem device_array_out;

void compile_open_cl(int n, int m)
{
	FILE *fp;
	char *source_str;
	size_t source_size;

	fp = fopen("jacobistep.cl", "r");
	if (!fp)
	{
		fprintf(stderr, "Failed to load kernel.\n");
		exit(1);
	}

	source_str = (char *)malloc(MAX_SOURCE_SIZE);
	source_size = fread(source_str, 1, MAX_SOURCE_SIZE, fp);
	fclose(fp);

	cl_int ret = clGetPlatformIDs(1, &platform_id, &ret_num_platforms);
	ret = clGetDeviceIDs(platform_id, CL_DEVICE_TYPE_DEFAULT, 1,
						 &device_id, &ret_num_devices);

	// printf("%d aaa %d\n", ret, ret_num_devices);

	context = clCreateContext(NULL, 1, &device_id, NULL, NULL, &ret);

	command_queue = clCreateCommandQueue(context, device_id, 0, &ret);

	program = clCreateProgramWithSource(context, 1,
										(const char **)&source_str,
										(const size_t *)&source_size,
										&ret);

	ret = clBuildProgram(program, 1, &device_id, NULL, NULL, NULL);

	kernel = clCreateKernel(program, "jacobistep", &ret);
}

void cleanup()
{
	// Clean up
	cl_int ret = clFlush(command_queue);
	ret = clFinish(command_queue);
	ret = clReleaseKernel(kernel);
	ret = clReleaseProgram(program);
	ret = clReleaseMemObject(device_array_in);
	ret = clReleaseMemObject(device_array_out);
	ret = clReleaseCommandQueue(command_queue);
	ret = clReleaseContext(context);
}

void jacobistep(float *psinew, float *psi, int m, int n)
{
	cl_int ret;

	float *ptr_to_array_data = psi;
	device_array_in = clCreateBuffer(context,
									 CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR,
									 m * n * sizeof(float),
									 ptr_to_array_data,
									 &ret);
	device_array_out = clCreateBuffer(context,
									  CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR,
									  m * n * sizeof(float),
									  ptr_to_array_data,
									  &ret);

	clSetKernelArg(kernel, 0, sizeof(cl_mem), &device_array_in);
	clSetKernelArg(kernel, 1, sizeof(cl_mem), &device_array_out);
	clSetKernelArg(kernel, 2, sizeof(cl_int), &n);
	clSetKernelArg(kernel, 3, sizeof(cl_int), &m);

	size_t global_item_size = (n + 1) * (m + 1) + (64 - (n + 1) * (m + 1) % 64); // lose al radi
	size_t local_item_size = 64;

	ret = clEnqueueWriteBuffer(command_queue,
							   device_array_in,
							   CL_TRUE,
							   0,
							   (n + 1) * (m + 1) * sizeof(cl_float),
							   ptr_to_array_data,
							   0,
							   NULL,
							   NULL);

	ret = clEnqueueNDRangeKernel(command_queue,
								 kernel,
								 1,
								 NULL,
								 &global_item_size,
								 &local_item_size,
								 0,
								 NULL,
								 NULL);

	ptr_to_array_data = psinew;

	ret = clEnqueueReadBuffer(command_queue,
							  device_array_out,
							  CL_TRUE,
							  0,
							  (n + 1) * (m + 1) * sizeof(cl_float),
							  ptr_to_array_data,
							  0,
							  NULL,
							  NULL);

	// 0.00125535

	// int i, j;

	// for (i = 1; i <= m; i++)
	// {
	// 	for (j = 1; j <= n; j++)
	// 	{
	// 		psinew[i * (m + 2) + j] = 0.25 * (psi[(i - 1) * (m + 2) + j] + psi[(i + 1) * (m + 2) + j] + psi[i * (m + 2) + j - 1] + psi[i * (m + 2) + j + 1]);
	// 	}
	// }
}

double deltasq(float *newarr, float *oldarr, int m, int n)
{
	int i, j;

	double dsq = 0.0;
	double tmp;

	for (i = 1; i <= m; i++)
	{
		for (j = 1; j <= n; j++)
		{
			tmp = newarr[i * (m + 2) + j] - oldarr[i * (m + 2) + j];
			dsq += tmp * tmp;
		}
	}

	return dsq;
}
