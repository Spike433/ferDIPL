#include <stdio.h>
#include <math.h>
#include <PDQ_Lib.h>

main() {
  extern int nodes, streams;
	
  float L  = 0.1; // Ucestalost dolazaka zahtjeva u rep cekanja L = 0.1 z/s
  float S1 = 1.0; // Prosjecno vrijeme posluzivanja zahtjeva S1 = 1.0 s/z
  float S2 = 2.0; // Prosjecno vrijeme posluzivanja zahtjeva S2 = 2.0 s/z
  float S3 = 3.0; // Prosjecno vrijeme posluzivanja zahtjeva S3 = 3.0 s/z

  // Postavljanje pocetnih postavi PDQ sustava
  PDQ_Init("Serija tri posluzitelja");

  // Stvaranje ulaznog toka zadataka
  streams = PDQ_CreateOpen("Zadaci", L);

  // Stvaranje tri posluzitelja koji zahtjeve posluzuju prema
  // redoslijedu prispjeca
  nodes = PDQ_CreateNode("Posluzitelj1", CEN, FCFS);
  nodes = PDQ_CreateNode("Posluzitelj2", CEN, FCFS);
  nodes = PDQ_CreateNode("Posluzitelj3", CEN, FCFS);

  // Povezivanje toka zadataka s posluziteljem
  PDQ_SetDemand("Posluzitelj1", "Zadaci", S1);
  PDQ_SetDemand("Posluzitelj2", "Zadaci", S2);
  PDQ_SetDemand("Posluzitelj3", "Zadaci", S3);

  // Pokretanje izracuna
  PDQ_Solve(CANON);

  // Prikaz rezultata
  PDQ_Report();
}
