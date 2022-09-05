#include <stdio.h>
#include <math.h>
#include <PDQ_Lib.h>

#define BROJ_POSLUZITELJA              1
#define BROJ_PROGRAMERA              230
#define VRIJEME_IZMEDU_KOMPILACIJA   300
#define VRIJEME_KOMPILACIJE         0.63

main() {
  extern int nodes, streams;

  int   n, i, j;
  float sm_x[BROJ_PROGRAMERA];
  float pq[BROJ_PROGRAMERA + 1][BROJ_PROGRAMERA + 1];
  float R, h, qLength;

  float x, xn;
  
  for( i=1; i <= BROJ_PROGRAMERA; i++) {
    if ( i <= BROJ_POSLUZITELJA ) {
      PDQ_Init("multibus");

      streams = PDQ_CreateClosed("reqs", TERM, (float)i, 0.0);
      nodes   = PDQ_CreateNode("bus", CEN, FCFS);

      PDQ_SetDemand("bus", "reqs", VRIJEME_KOMPILACIJE);

      PDQ_Solve(EXACT);

      x = PDQ_GetThruput(TERM, "reqs");

      sm_x[i] = x;
    } else {
      sm_x[i] = x;
    }
  } 

  pq[0][0] = 1.0;

  for (n=1; n <= BROJ_PROGRAMERA; n++) {
    R = 0.0;

    for (j = 1; j <= n; j++) {
      R += (j / sm_x[j]) * pq[j - 1][n - 1];
    }
  
  	xn = n / (VRIJEME_IZMEDU_KOMPILACIJA + R);
  	qLength = xn * R;

  	for (j=1; j <= n; j++) {
   	 pq[j][n] = (xn / sm_x[j]) * pq[j - 1][n - 1];
  	}
  	pq[0][n] = 1.0;
  
  	for(j=1; j <= n; j++) {
    	pq[0][n] -= pq[j][n];
	  }
	}
  
  printf("Posluzitelja: %2d, Programera %2d\n", BROJ_POSLUZITELJA, BROJ_PROGRAMERA);
  printf("Opterecenje: %3.4f\n", VRIJEME_KOMPILACIJE / VRIJEME_IZMEDU_KOMPILACIJA);
  printf("X %3.4f\n", xn);  
  printf("P %3.4f\n", xn * VRIJEME_IZMEDU_KOMPILACIJA);
  printf("Q %3.4f\n", BROJ_PROGRAMERA - xn * VRIJEME_IZMEDU_KOMPILACIJA);
  printf("R %3.4f\n", BROJ_PROGRAMERA / xn - VRIJEME_IZMEDU_KOMPILACIJA);
  
}
