using System.ComponentModel.DataAnnotations;

namespace SuperManager.Modeli
{
    public class Bodovi : IComparable
    {
        [Required]
        public string Ime { get; set; }

        public int Pobjede { get; set; }
        public int Izjednaceno { get; set; }

        public int SumaGolova { get; set; }
        public int SumaDobivenih { get; set; }
        
        public int Razlika { get; set; }
        public int Rezultat { get; set; }

        public int CompareTo(object? obj)
        {
            var other = obj as Bodovi;
            if(other == null)
                return 1;

            if(this.Rezultat == other.Rezultat)
                return this.Razlika.CompareTo(other.Razlika);

            return this.Rezultat.CompareTo(other.Rezultat);
        }
    }
}
