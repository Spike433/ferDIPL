#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "arraymalloc.h"
#include "boundary.h"
#include "jacobi.h"
#include "cfdio.h"

int main(int argc, char **argv)
{
	int printfreq = 1000; // output frequency
	double error, bnorm;
	double tolerance = 0.0; // tolerance for convergence. <=0 means do not check

	// main arrays
	float *psi;
	// temporary versions of main arrays
	float *psitmp;

	// command line arguments
	int scalefactor, numiter;

	// simulation sizes
	int bbase = 10;
	int hbase = 15;
	int wbase = 5;
	int mbase = 32;
	int nbase = 32;

	int irrotational = 1, checkerr = 0;

	int m, n, b, h, w;
	int iter;
	int i, j;

	double tstart, tstop, ttot, titer;

	// do we stop because of tolerance?
	if (tolerance > 0)
	{
		checkerr = 1;
	}

	// check command line parameters and parse them

	if (argc < 3 || argc > 4)
	{
		printf("Usage: cfd <scale> <numiter>\n");
		return 0;
	}

	scalefactor = atoi(argv[1]);
	numiter = atoi(argv[2]);

	if (!checkerr)
	{
		printf("Scale Factor = %i, iterations = %i\n", scalefactor, numiter);
	}
	else
	{
		printf("Scale Factor = %i, iterations = %i, tolerance= %g\n", scalefactor, numiter, tolerance);
	}

	printf("Irrotational flow\n");

	// Calculate b, h & w and m & n
	b = bbase * scalefactor;
	h = hbase * scalefactor;
	w = wbase * scalefactor;
	m = mbase * scalefactor;
	n = nbase * scalefactor;

	printf("Running CFD on %d x %d grid in serial\n", m, n);

	// allocate arrays
	psi = (float *)malloc((m + 2) * (n + 2) * sizeof(float));
	psitmp = (float *)malloc((m + 2) * (n + 2) * sizeof(float));

	// zero the psi array
	for (i = 0; i < m + 2; i++)
	{
		for (j = 0; j < n + 2; j++)
		{
			psi[i * (m + 2) + j] = 0.0;
		}
	}

	// set the psi boundary conditions
	boundarypsi(psi, m, n, b, h, w);

	// compute normalisation factor for error
	bnorm = 0.0;

	for (i = 0; i < m + 2; i++)
	{
		for (j = 0; j < n + 2; j++)
		{
			bnorm += psi[i * (m + 2) + j] * psi[i * (m + 2) + j];
		}
	}
	bnorm = sqrt(bnorm);

	printf("\nCompiling opencl...\n\n");

	compile_open_cl(n, m);

	// begin iterative Jacobi loop
	printf("\nStarting main loop...\n\n");
	tstart = gettime();

	for (iter = 1; iter <= numiter; iter++)
	{

		// calculate psi for next iteration
		jacobistep(psitmp, psi, m, n);

		// calculate current error if required
		if (checkerr || iter == numiter)
		{
			error = deltasq(psitmp, psi, m, n);

			error = sqrt(error);
			error = error / bnorm;
		}

		// quit early if we have reached required tolerance
		if (checkerr)
		{
			if (error < tolerance)
			{
				printf("Converged on iteration %d\n", iter);
				break;
			}
		}

		// copy back
		for (i = 1; i <= m; i++)
		{
			for (j = 1; j <= n; j++)
			{
				psi[i * (m + 2) + j] = psitmp[i * (m + 2) + j];
			}
		}

		// print loop information
		if (iter % printfreq == 0)
		{
			if (!checkerr)
			{
				printf("Completed iteration %d\n", iter);
			}
			else
			{
				printf("Completed iteration %d, error = %g\n", iter, error);
			}
		}
	} // iter

	if (iter > numiter)
		iter = numiter;

	tstop = gettime();

	ttot = tstop - tstart;
	titer = ttot / (double)iter;

	// print out some stats
	printf("\n... finished\n");
	printf("After %d iterations, the error is %g\n", iter, error);
	printf("Time for %d iterations was %g seconds\n", iter, ttot);
	printf("Each iteration took %g seconds\n", titer);

	// output results
	// writedatafiles(psi,m,n, scalefactor);
	// writeplotfile(m,n,scalefactor);

	// free un-needed arrays
	free(psi);
	free(psitmp);
	printf("... finished\n");

	return 0;
}
