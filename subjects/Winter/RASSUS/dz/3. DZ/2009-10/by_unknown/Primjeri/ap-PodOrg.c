#include <stdio.h>
#include <math.h>
#include <PDQ_Lib.h>

#define BROJ_AP_POSLUZITELJA    1.0
#define BROJ_BP_POSLUZITELJA   10.0
#define BROJ_IM_POSLUZITELJA    1.0

main() {
  extern int nodes, streams;

  int  i;
  char name[30];

  int broj_ap_posluzitelja  = BROJ_AP_POSLUZITELJA;
  int broj_bp_posluzitelja  = BROJ_BP_POSLUZITELJA;
  int broj_im_posluzitelja  = BROJ_IM_POSLUZITELJA;

  float p_im  = 0.1;
  float p_bp  = 0.15;
  
  float S_ZZ = 0.001;
  float S_PO = 0.001;  

  float S_AP   = 0.3;
  float S_BP   = 2.5/BROJ_BP_POSLUZITELJA;
  float S_IM   = 0.5;

  float Util  = 0.0;
  float Res   = 0.0;

  float L     = 0.0;
  float L_inc = 0.1;
  float L_max = 2.0;

  printf("L");
  
  for( i=0; i<broj_ap_posluzitelja; i++ )
	{
	  sprintf(name, "AP%d", i);
	  printf("\t%s", name);
  }  

  for( i=0; i<broj_bp_posluzitelja; i++ )
	{
	  sprintf(name, "BP%d", i);
	  printf("\t%s", name);
  }

  for( i=0; i<broj_im_posluzitelja; i++ )
	{
	  sprintf(name, "IM%d", i);
	  printf("\t%s", name);
  }

  printf("\tZZ");
  printf("\tPO");
  printf("\tR\n");


  L = L_inc;
  while (L < L_max + L_inc) {
		PDQ_Init("Web aplikacija");
	
	  streams = PDQ_CreateOpen("Zahtjevi", L);
	
		nodes = PDQ_CreateNode("ZZ", CEN, FCFS);
		nodes = PDQ_CreateNode("PO", CEN, FCFS);
	
		for( i=0; i<broj_ap_posluzitelja; i++ )
		{
			sprintf(name, "AP%d", i);
			nodes = PDQ_CreateNode(name, CEN, FCFS);
		}
	
	  for( i=0; i<broj_bp_posluzitelja; i++ )
	  {
	    sprintf(name, "BP%d", i);
	    nodes = PDQ_CreateNode(name, CEN, FCFS);
	  }
	  
	  for( i=0; i<broj_im_posluzitelja; i++ )
	  {
	    sprintf(name, "IM%d", i);
	    nodes = PDQ_CreateNode(name, CEN, FCFS);
	  }
	
	
	  PDQ_SetVisits("ZZ", "Zahtjevi", 1.0, S_ZZ);
	  PDQ_SetVisits("PO", "Zahtjevi", 1.0, S_PO);
	
	  for( i=0; i<broj_ap_posluzitelja; i++ )
	  {
	    sprintf(name, "AP%d", i);
	    PDQ_SetVisits(name, "Zahtjevi", ((1 - p_im) / (1 - p_bp)) / BROJ_AP_POSLUZITELJA, S_AP);
	  }
	
	  for( i=0; i<broj_bp_posluzitelja; i++ )
	  {
	    sprintf(name, "BP%d", i);
	    PDQ_SetVisits(name,   "Zahtjevi", (p_bp * (1 - p_im) / (1 - p_bp)) / BROJ_BP_POSLUZITELJA, S_BP);
	  }
	
	  for( i=0; i<broj_im_posluzitelja; i++ )
	  {
	    sprintf(name, "IM%d", i);
	    PDQ_SetVisits(name, "Zahtjevi", p_im / BROJ_IM_POSLUZITELJA, S_IM);
	  }

    PDQ_Solve(CANON);
	  
	  Util = 0.0;
	  
	  for( i=0; i<broj_ap_posluzitelja; i++ )
	  {
	    sprintf(name, "AP%d", i);
			Util += PDQ_GetUtilization(name, "Zahtjevi", TRANS);	
	  }

	  for( i=0; i<broj_bp_posluzitelja; i++ )
	  {
	    sprintf(name, "BP%d", i);
			Util += PDQ_GetUtilization(name, "Zahtjevi", TRANS);
	  }  

	  for( i=0; i<broj_im_posluzitelja; i++ )
	  {
	    sprintf(name, "IM%d", i);
			Util += PDQ_GetUtilization(name, "Zahtjevi", TRANS);
	  }
	  
		Util += PDQ_GetUtilization("ZZ", "Zahtjevi", TRANS);
		Util += PDQ_GetUtilization("PO", "Zahtjevi", TRANS);
	
		Util = (100 * Util)/(broj_ap_posluzitelja + broj_bp_posluzitelja + broj_im_posluzitelja + 2);
		
		printf("%f\t", L);
		
	  for( i=0; i<broj_ap_posluzitelja; i++ )
	  {
	    sprintf(name, "AP%d", i);
		  printf("%f\t", PDQ_GetResidenceTime(name, "Zahtjevi", TRANS));
	  }

	  for( i=0; i<broj_bp_posluzitelja; i++ )
	  {
	    sprintf(name, "BP%d", i);
		  printf("%f\t", PDQ_GetResidenceTime(name, "Zahtjevi", TRANS));
	  }

	  for( i=0; i<broj_im_posluzitelja; i++ )
	  {
	    sprintf(name, "IM%d", i);
		  printf("%f\t", PDQ_GetResidenceTime(name, "Zahtjevi", TRANS));
	  }

		printf("%f\t", PDQ_GetResidenceTime(name, "ZZ", TRANS));

		printf("%f\t", PDQ_GetResidenceTime(name, "PO", TRANS));

		printf("%f\n", PDQ_GetResponse(TRANS, "Zahtjevi"));

		L += L_inc;
	}
}
