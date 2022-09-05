#include <stdio.h>
#include <math.h>
#include <PDQ_Lib.h>

main() {
  // Dijeljene varijable koje koristi okruzenje PDQ
  extern int nodes, streams;
	
  float L = 0.5; // Ucestalost dolazaka zahtjeva u rep cekanja L = 0.5 z/s
  float S = 1.0; // Prosjecno vrijeme posluzivanja zahtjeva S = 1.0 s/z

  // Postavljanje pocetnih postavi PDQ sustava
  PDQ_Init("Posuzitelj s repom");

  // Stvaranje jednog posluzitelja koji zahtjeve posluzuje prema
  // redoslijedu prispjeca
  nodes = PDQ_CreateNode("Posluzitelj", CEN, FCFS);

  // Stvaranje ulaznog toka zadataka
  streams = PDQ_CreateOpen("Zadaci", L);

  // Povezivanje toka zadataka s posluziteljem i definiranje vremena posluzivanja
  PDQ_SetDemand("Posluzitelj", "Zadaci", S);

  // Pokretanje izracuna
  PDQ_Solve(CANON);

  // Prikaz rezultata
  PDQ_Report();
}
