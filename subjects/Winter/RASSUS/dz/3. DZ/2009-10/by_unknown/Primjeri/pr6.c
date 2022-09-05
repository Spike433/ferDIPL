#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <PDQ_Lib.h>

main()
{
    extern int      nodes;
    extern int      streams;

    double          L = 3; // Ucestalost dolazaka zahtjeva u rep cekanja L = 3 upit/min
    double          S = 2; // Prosjecno vrijeme posluzivanja zahtjeva S = 2 min/upit

    // Pomocne varijable za odredivanje imena cvorova i repova u PDQ mrezi
    char            nName[30];
    char            cName[30]; 

    int             i;
    int             count = 18; // Broj paralelnih posluzitelja s privatnim repom

    // Postavljanje pocetnih postavi PDQ sustava
    PDQ_Init("Aplikacija korisnicke podrske");


    // Za svaki posluzitelj izgradi cvor i rep cekanja
    for( i=0; i<count; i++ )
    {
      sprintf(nName, "Serv %2d", i);
      sprintf(cName, "Clnt %2d", i);

      // Stvaranje jednog posluzitelja koji zahtjeve posluzuje prema
      // redoslijedu prispjeca
      nodes = PDQ_CreateNode(nName, CEN, FCFS);

      // Stvaranje ulaznog toka zadataka za svaki rep cekanja
      // U svaki od "count" repova cekanja dolazi "L/count" korisnika/min
      streams = PDQ_CreateOpen(cName, L/count);
    }


    // Povezi repove cekanja s posluziteljima i definiraj vrijeme posluzivanja
    for( i=0; i<count; i++ )
    {

      sprintf(nName, "Serv %2d", i);
      sprintf(cName, "Clnt %2d", i);

      PDQ_SetDemand(nName, cName, S);
    }


    // Pokretanje izracuna
    PDQ_Solve(CANON);

    // Prikaz rezultata
    PDQ_Report();
}
