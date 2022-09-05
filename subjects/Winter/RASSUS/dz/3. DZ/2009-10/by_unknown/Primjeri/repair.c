#include <stdio.h>
#include <math.h>

main(int argc, char *argv[])
{
  double		L;   /* Srednji broj pokvarenih uredaja u liniji */
  double		Q;   /* Srednji broj pokvarenih uredaja u sustavu */
  double		R;   /* Srednje vrijeme zadrzavanja */
  double		S;   /* Srednje vrijeme popravka */
  double		U;   /* Ukupno srednja zaposlenost */
  double		rho; /* Zaposlenost po jednom spoluzitelju */
  double		W;   /* Srednje vrijeme cekanja u repu */
  double		X;   /* Srednja propusnost u sustavu */
  double		Z;   /* Srednje vrijeme izmedu nastanka kvarova */
  double		p;   /* Privremena varijabla za racunanje vjerojatnosti */
  double		p0;  /* Vjerojatnost da nema kvarova */

  long		m;
  long		N;
  long		k;

  if (argc < 5) {
    printf("Uporaba: %s m S N Z\n", *argv);
    printf(" m - Broj posluzitelja \n");
    printf(" S - Srednje vrijeme posluzivanja \n");
    printf(" N - Broj uredaja \n");
    printf(" Z - Srednje vrijeme izmedu nastanka kvarova \n");

    exit(1);
  }

  m	= atol(*++argv);
  S	= atol(*++argv);
  N	= atol(*++argv);
  Z	= atol(*++argv);

  p = p0 = 1;
  L = 0;

  for( k=1; k<=N; k++) {
    p *= (N - k + 1) * S / Z;
    if (k <= m) {
      p /= k;
    } else {
      p /= m;
    }

    p0 += p;

    if (k > m) {
      L += p * (k - m);
    }
  }

  p0 = 1.0 / p0;

  L *= p0;
  W = L * (S + Z) / (N - L);
  R = W + S;
  X = N / (R + Z);
  U = X * S;
  rho = U/m;
  Q = X*R;

  printf ("\n");
  printf ("M/M/%ld/%ld/%ld Model\n", m, N, N);
  printf ("---------------------------------------\n");
  printf ("  Broj uredaja:		%5.0ld\n", N);
  printf ("  Vrijeme rada uredaja:	%5.4lf\n", Z);
  printf ("  Vrijeme posluzivanja:	%5.4lf\n", S);
  printf ("  Ucestalost kvarova:	%5.4lf\n", 1 / Z);
  printf ("  Ucestalost posluzivanja:	%5.4lf\n", 1 / S);
  printf ("  Zaposlenost sustava:	%5.4lf\n", U);
  printf ("  Zaposlenost po pos.:	%5.4lf\n", rho);
  printf ("\n");
  printf ("  Broj uredaja u sustavu:	%5.4lf\n", Q);
  printf ("  Broj popravaka: 		%5.4lf\n", U);
  printf ("  Broj uredaja u repu:	%5.4lf\n", Q - U);
  printf ("  Vrijeme cekanja:		%5.4lf\n", R - S);
  printf ("  Propusnost:		%5.4lf\n", X);
  printf ("  Vrijeme odziva:		%5.4lf\n", R);
  printf ("  Norm. vrijeme cek.:	%5.4lf\n", R / S);
  printf ("\n");
}
