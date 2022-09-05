#include <stdio.h>
#include <math.h>
#include <PDQ_Lib.h>

main() {
	extern int nodes, streams;
	
	int N_APV = 1;
	int N_APE = 1;
	int N_BPV = 1;
	int N_BPE = 1;
	
	float p_APV = 0.30;
	float p_BPV = 0.30;
	float p_BPE = 0.20;

	float S_APV = 0.3;
	float S_APE = 0.2;
	float S_BPV = 3.5;
	float S_BPE = 2.8;
	float S_ZZ = 0.001;
	float S_PO = 0.001;
	
	float L_MIN = 0.1f;
	float L_MAX = 2.0f;
	float L_STEP = 0.1f;
	
	int i;
	float L;
	
	printf("L\t");

	for(i = 0; i < N_APV; i++)
		printf("APV%d\t", i);
	for(i = 0; i < N_APE; i++)
		printf("APE%d\t", i);
	for(i = 0; i < N_BPV; i++)
		printf("BPV%d\t", i);
	for(i = 0; i < N_BPE; i++)
		printf("BPE%d\t", i);
	
	printf("ZZ\tPO\tR\n");
	
	for (L = L_MIN; L <= L_MAX + L_MIN; L += L_STEP) {
	
		PDQ_Init("Raspodijeljena aplikacija");
		streams = PDQ_CreateOpen("Zahtjevi", L);
		
		nodes = PDQ_CreateNode("ZZ", CEN, FCFS);
		nodes = PDQ_CreateNode("PO", CEN, FCFS);
		
		for(i = 0; i < N_APV; i++)
			nodes = PDQ_CreateNode("APV" + i, CEN, FCFS);
		for(i = 0; i < N_APE; i++)
			nodes = PDQ_CreateNode("APE" + i, CEN, FCFS);
		for(i = 0; i < N_BPV; i++)
			nodes = PDQ_CreateNode("BPV" + i, CEN, FCFS);
		for(i = 0; i < N_BPE; i++)
			nodes = PDQ_CreateNode("BPE" + i, CEN, FCFS);
	
		PDQ_SetVisits("ZZ", "Zahtjevi", 1.0f, S_ZZ);
		PDQ_SetVisits("PO", "Zahtjevi", 1.0f, S_PO);
		
		for(i = 0; i < N_APV; i++)
			PDQ_SetVisits("APV" + i, "Zahtjevi", p_APV/(1-p_BPV)/N_APV, S_APV);
		for(i = 0; i < N_APE; i++)
			PDQ_SetVisits("APE" + i, "Zahtjevi", (1-p_APV)/(1-p_BPE)/N_APE, S_APE);
		for(i = 0; i < N_BPV; i++)
			PDQ_SetVisits("BPV" + i, "Zahtjevi", p_BPV*p_APV/(1-p_BPV)/N_BPV, S_BPV);
		for(i = 0; i < N_BPE; i++)
			PDQ_SetVisits("BPE" + i, "Zahtjevi", p_BPE*(1-p_APV)/(1-p_BPE)/N_BPE, S_BPE);
	
		PDQ_Solve(CANON);
	
		//PDQ_Report();
		
		printf("%f ", L);
	
		for(i = 0; i < N_APV; i++)
			printf("%f ", PDQ_GetResidenceTime("APV" + i, "Zahtjevi", TRANS));
		for(i = 0; i < N_APE; i++)
			printf("%f ", PDQ_GetResidenceTime("APE" + i, "Zahtjevi", TRANS));
		for(i = 0; i < N_BPV; i++)
			printf("%f ", PDQ_GetResidenceTime("BPV" + i, "Zahtjevi", TRANS));
		for(i = 0; i < N_BPE; i++)
			printf("%f ", PDQ_GetResidenceTime("BPE" + i, "Zahtjevi", TRANS));
	
		printf("%f ", PDQ_GetResidenceTime("ZZ", "Zahtjevi", TRANS));
		printf("%f ", PDQ_GetResidenceTime("PO", "Zahtjevi", TRANS));
		printf("%f\n", PDQ_GetResponse(TRANS, "Zahtjevi"));
	}
}
