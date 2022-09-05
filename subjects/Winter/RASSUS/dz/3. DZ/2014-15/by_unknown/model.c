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

  float L     = 0.0;
  float L_inc = 0.1;
  float L_max = 2.0;

  printf("L");

  for( i=0; i<nAES; i++ )
	{
	  sprintf(name, "AES%d", i);
	  printf("\t%s", name);
  }

  for( i=0; i<nBPE; i++ )
	{
	  sprintf(name, "BPE%d", i);
	  printf("\t%s", name);
  }

  for( i=0; i<nALS; i++ )
	{
	  sprintf(name, "ALS%d", i);
	  printf("\t%s", name);
  }
  for( i=0; i<nAWS; i++ )
	{
	  sprintf(name, "AWS%d", i);
	  printf("\t%s", name);
  }
  for( i=0; i<nBPW; i++ )
	{
	  sprintf(name, "BPW%d", i);
	  printf("\t%s", name);
  }

  printf("\tZZ");
  printf("\tPO");
  printf("\tT\n");


  L = L_inc;
  while (L < L_max) {
		PDQ_Init("Web portal");

	  streams = PDQ_CreateOpen("Zahtjevi", L);

		nodes = PDQ_CreateNode("ZZ", CEN, FCFS);
		nodes = PDQ_CreateNode("PO", CEN, FCFS);

		for( i=0; i<nAES; i++ )
		{
			nodes = PDQ_CreateNode("AES"+i, CEN, FCFS);
		}

	  for( i=0; i<nBPE; i++ )
	  {
	    nodes = PDQ_CreateNode("BPE"+i, CEN, FCFS);
	  }

	  for( i=0; i<nALS; i++ )
	  {
	    nodes = PDQ_CreateNode("ALS"+i, CEN, FCFS);
	  }
	  for( i=0; i<nAWS; i++ )
	  {
	    nodes = PDQ_CreateNode("AWS"+i, CEN, FCFS);
	  }
	  for( i=0; i<nBPW; i++ )
	  {
	    nodes = PDQ_CreateNode("BPW"+i, CEN, FCFS);
	  }

	  PDQ_SetVisits("ZZ", "Zahtjevi", 1.0, sZZ);
	  PDQ_SetVisits("PO", "Zahtjevi", 1.0, sPO);

	  for( i=0; i<nAES; i++ )
	  {
	    PDQ_SetVisits("AES"+i, "Zahtjevi", (pAES/(1-pBPE))/nAES, sAES);
	  }

	  for( i=0; i<nBPE; i++ )
	  {
	    PDQ_SetVisits("BPE"+i,   "Zahtjevi", (pAES*pBPE/(1-pBPE))/nBPE, sBPE);
	  }

	  for( i=0; i<nALS; i++ )
	  {
	    PDQ_SetVisits("ALS"+i, "Zahtjevi", (1-pAES-pAWS)/nALS, sALS);
	  }
    for( i=0; i<nAWS; i++ )
	  {
	    PDQ_SetVisits("AWS"+i, "Zahtjevi", (pAWS/(1-pBPW))/nAWS, sAWS);
	  }
    for( i=0; i<nBPW; i++ )
	  {
	    PDQ_SetVisits("BPW"+i, "Zahtjevi", (pBPW*pAWS/(1-pBPW))/nBPW, sBPW);
	  }


    PDQ_Solve(CANON);

	  printf("%f ", L);

		for(i = 0; i < nAES; i++)
			printf("%f ", PDQ_GetResidenceTime("AES"+i,"Zahtjevi",TRANS));
		for(i = 0; i < nBPE; i++)
			printf("%f ", PDQ_GetResidenceTime("BPE"+i,"Zahtjevi",TRANS));
		for(i = 0; i < nALS; i++)
			printf("%f ", PDQ_GetResidenceTime("ALS"+i,"Zahtjevi",TRANS));
		for(i = 0; i < nAWS; i++)
			printf("%f ", PDQ_GetResidenceTime("AWS"+i,"Zahtjevi",TRANS));
        for(i = 0; i < nBPW; i++)
			printf("%f ", PDQ_GetResidenceTime("BPW"+i,"Zahtjevi",TRANS));

		printf("%f ", PDQ_GetResidenceTime("ZZ", "Zahtjevi", TRANS));
		printf("%f ", PDQ_GetResidenceTime("PO", "Zahtjevi", TRANS));
		printf("%f\n", PDQ_GetResponse(TRANS, "Zahtjevi"));

		L+=L_inc;
	}
}
