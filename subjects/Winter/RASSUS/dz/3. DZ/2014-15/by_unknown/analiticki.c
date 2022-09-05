#include <stdio.h>
#include <math.h>
#include "PDQ_Lib.h"


main() {
  extern int nodes, streams;

  int  i;
  char name[30];

  int nAES=1;
  int nBPE=1;
  int nALS=1;
  int nAWS=1;
  int nBPW=1;

  float pAES=0.3;
  float pAWS=0.65;
  float pBPE=0.1;
  float pBPW=0.5;

  float sZZ=0.001;
  float sPO=0.001;
  float sAES=0.5;
  float sBPE=3;
  float sALS=1;
  float sAWS=0.02;
  float sBPW=0.5;

  float dAES=pAES*sAES/(1-pBPE);
  float dBPE=pAES*pBPE*sBPE/(1-pBPE);
  float dALS=(1-pAES-pAWS)*sALS;
  float dZZ=sZZ;
  float dPO=sPO;
  float dAWS=pAWS*sAWS/(1-pBPW);
  float dBPW=pBPW*pAWS*sBPW/(1-pBPW);

  float L     = 0.0;
  float L_inc = 0.1;
  float L_max = 2.0;

  printf("L\t\tT\n");


  L = L_inc;
  while (L < L_max) {
		float T=dAES/(1-L*dAES)+dBPE/(1-L*dBPE)+dALS/(1-L*dALS)+dAWS/(1-L*dAWS)+dBPW/(1-L*dBPW)+dPO/(1-L*dPO)+dZZ/(1-L*dZZ);
		printf("%f\t%f\n\n", L,T);

		L+=L_inc;
	}
}
