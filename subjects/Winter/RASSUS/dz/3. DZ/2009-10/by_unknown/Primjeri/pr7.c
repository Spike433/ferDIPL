#include <stdio.h>
#include <math.h>
#include <PDQ_Lib.h>

main() {
  extern int nodes, streams;
	
  float p_err = 0.30; // vjerojatnost retransmisije
  float L     = 0.50; // Ucestalost dolazaka zahtjeva u rep cekanja L = 0.50 z/s
  float S     = 0.75; // Prosjecno vrijeme posluzivanja zahtjeva S = 0.75 s/z

  // Odredivanje faktora prosjecnog broja posjeta
  float V     = 1.0 / ( 1.0 - p_err );

  // Postavljanje pocetnih postavi PDQ sustava
  PDQ_Init("Posluzitelj s repom i povratnom vezom");

  // Stvaranje jednog posluzitelja koji zahtjeve posluzuje prema
  // redoslijedu prispjeca
  nodes = PDQ_CreateNode("Kanal", CEN, FCFS);

  // Stvaranje ulaznog toka zadataka
  streams = PDQ_CreateOpen("Poruka", L);

  // Povezivanje toka zadataka s posluziteljem s definiranje prosjecnog broja posjeta i vremena posluzivanja
  PDQ_SetVisits("Kanal", "Poruka", V, S);

  // Pokretanje izracuna
  PDQ_Solve(CANON);

  // Prikaz rezultata
  PDQ_Report();
}
