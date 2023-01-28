using SuperManager.CuvarPodataka;
using SuperManager.Modeli;

namespace SuperManager.Pogledi
{
    public class GenerirajBodove
    {
        public List<Bodovi> StvoriBodove()
        {
            var bodovi = new List<Bodovi>();

            for (int i = 0; i < Cuvar.Mecevi.Count; i++)
            {
                var mec = Cuvar.Mecevi[i];

                LijevaStrana(bodovi, mec);

                DesnaSrana(bodovi, mec);
            }

            return bodovi;
        }

        private static void DesnaSrana(List<Bodovi> bodovi, Mec mec)
        {
            var pronaden = bodovi.FirstOrDefault<Bodovi>(m => m.Ime == mec.Protivnik2);
            bodovi.Remove(pronaden);

            int pobjede = 0;
            int izjednaceno = 0;
            int daniGolovi = 0;
            int dobiveni = 0;

            if (pronaden == null)
            {
                pobjede = mec.Rezultat1 < mec.Rezultat2 ? 1 : 0;
                izjednaceno = mec.Rezultat1 == mec.Rezultat2 ? 1 : 0;
                daniGolovi = mec.Rezultat2;
                dobiveni = mec.Rezultat1;
            }
            else
            {
                var pobjede1 = mec.Rezultat1 < mec.Rezultat2 ? 1 : 0;
                var izjednaceno1 = mec.Rezultat1 == mec.Rezultat2 ? 1 : 0;
                pobjede = pronaden.Pobjede + pobjede1;
                izjednaceno = pronaden.Izjednaceno + izjednaceno1;

                daniGolovi = pronaden.SumaGolova + mec.Rezultat2;
                dobiveni = pronaden.SumaDobivenih + mec.Rezultat1;
            }

            var b =
            new Bodovi
            {
                Ime = mec.Protivnik2,
                Pobjede = pobjede,
                Izjednaceno = izjednaceno,
                SumaGolova = daniGolovi,
                SumaDobivenih = dobiveni
            };

            b.Razlika = b.SumaGolova - b.SumaDobivenih;
            b.Rezultat = b.Pobjede * 3 + b.Izjednaceno;
            bodovi.Add
            (
                b
            );
        }

        private static void LijevaStrana(List<Bodovi> bodovi, Mec mec)
        {
            var pronaden = bodovi.FirstOrDefault<Bodovi>(m => m.Ime == mec.Protivnik1);
            bodovi.Remove(pronaden);

            int pobjede = 0;
            int izjednaceno = 0;
            int daniGolovi = 0;
            int dobiveni = 0;

            if (pronaden == null)
            {
                pobjede = mec.Rezultat1 > mec.Rezultat2 ? 1 : 0;
                izjednaceno = mec.Rezultat1 == mec.Rezultat2 ? 1 : 0;
                daniGolovi = mec.Rezultat1;
                dobiveni = mec.Rezultat2;
            }
            else
            {
                var pobjede1 = mec.Rezultat1 > mec.Rezultat2 ? 1 : 0;
                var izjednaceno1 = mec.Rezultat1 == mec.Rezultat2 ? 1 : 0;
                pobjede = pronaden.Pobjede + pobjede1;
                izjednaceno = pronaden.Izjednaceno + izjednaceno1;

                daniGolovi = pronaden.SumaGolova + mec.Rezultat1;
                dobiveni = pronaden.SumaDobivenih + mec.Rezultat2;
            }

            var b =
            new Bodovi
            {
                Ime = mec.Protivnik1,
                Pobjede = pobjede,
                Izjednaceno = izjednaceno,
                SumaGolova = daniGolovi,
                SumaDobivenih = dobiveni
            };

            b.Razlika = b.SumaGolova - b.SumaDobivenih;
            b.Rezultat = b.Pobjede * 3 + b.Izjednaceno;

            bodovi.Add(
                b
            );
        }
    }
}
