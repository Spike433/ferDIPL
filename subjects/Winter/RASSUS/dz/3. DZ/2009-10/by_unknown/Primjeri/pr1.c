#include <stdio.h>
#include <math.h>
#include <PDQ_Lib.h>

main() {
  // Dijeljene varijable koje koristi okruzenje PDQ
  extern int nodes, streams;
	
  float L = 50;    // Ucestalost dolazaka zahtjeva u rep cekanja L = 50 z/s
  float S = 0.01;  // Prosjecno vrijeme posluzivanja zahtjeva S = 0.01 s/z

  // Postavljanje pocetnih postavi PDQ sustava
  PDQ_Init("Diskovni podsustav");

  // Stvaranje jednog posluzitelja koji provodi operacije prema
  // redoslijedu prispjeca
  nodes = PDQ_CreateNode("Posluzitelj", CEN, FCFS);

  // Stvaranje ulaznog toka zadataka
  streams = PDQ_CreateOpen("Operacije", L);

  // Povezivanje toka zadataka s posluziteljem i definiranje vremena posluzivanja
  PDQ_SetDemand("Posluzitelj", "Operacije", S);

  // Pokretanje izracuna
  PDQ_Solve(CANON);

  // Prikaz rezultata
  PDQ_Report();
}
