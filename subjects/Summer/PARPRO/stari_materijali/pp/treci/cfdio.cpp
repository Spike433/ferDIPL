#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "cfdio.h"
#include "arraymalloc.h"

#pragma warning(disable : 4996)


// time in seconds
#ifdef _WIN32 
#include <windows.h>
double gettime(void)
{
	LARGE_INTEGER fr, t;
	QueryPerformanceFrequency(&fr);
	QueryPerformanceCounter(&t);
	double t_sec = (t.QuadPart) / (double)fr.QuadPart;
	return t_sec;
}
#else 
#include <sys/time.h>
double gettime(void)
{
  struct timeval tp;
  gettimeofday (&tp, NULL);
  return tp.tv_sec + tp.tv_usec/(double)1.0e6;
}
#endif