using SuperManager.Modeli;

namespace SuperManager.Pogledi
{
    public class UcitajMeceve
    {
        public List<Mec> StvoriMeceve()
        {
            var mecevi = new List<Mec>();

            mecevi.Add(
                new Mec
                {
                    Runda = 1,
                    Protivnik1 = "Crvena zvezda",
                    Protivnik2 = "Partizan",

                    Rezultat1 = 3,
                    Rezultat2 = 2,

                    Prognoza = Mec.dohvatiVrijeme(),

                    Datum = DateTime.Now.AddDays(-5) 
                }
            );

            mecevi.Add(
                new Mec
                {
                    Runda = 2,

                    Protivnik1 = "Crvena zvezda",
                    Protivnik2 = "Partizan",

                    Rezultat1 = 1,
                    Rezultat2 = 5,

                    Prognoza = Mec.dohvatiVrijeme(),

                    Datum = DateTime.Now.AddDays(-5)
                }
            );

            return mecevi;
        }
    }
}
