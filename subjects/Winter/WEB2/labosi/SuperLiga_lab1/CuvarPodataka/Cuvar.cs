using SuperManager.Modeli;
using SuperManager.Pogledi;

namespace SuperManager.CuvarPodataka
{
    public static class Cuvar
    {
        public static List<Mec> Mecevi { get; set; }
        public static List<UpravljacKomentarima> UpravljacKomentarima { get; set; }


        public static void GenerirajPocetnePodatke()
        {
            Mecevi = new UcitajMeceve().StvoriMeceve();
            UpravljacKomentarima = new List<UpravljacKomentarima>();
        }
    }
}
