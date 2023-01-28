using System;
using System.ComponentModel.DataAnnotations;

namespace SuperManager.Modeli
{
    public class Mec
    {
        [Required]
        public int Runda { get; set; }

        [StringLength(1, MinimumLength = 1, ErrorMessage = "Minimalno jedan znak.")]
        public string Protivnik1 { get; set; }
        [StringLength(1, MinimumLength = 1, ErrorMessage = "Minimalno jedan znak.")]
        public string Protivnik2 { get; set; }

        [Required]
        public int Rezultat1 { get; set; }
        [Required]
        public int Rezultat2 { get; set; }

        [StringLength(1, MinimumLength = 1, ErrorMessage = "The Gender must be 1 characters.")]
        public string Prognoza { get; set; }

        public DateTime Datum { get; set; }
        
        public static string dohvatiVrijeme()
        {
            var lista = new List<string>()
                {
                    "Suncano","Kisno","Oblacno"
                };

            return lista[new Random().Next(lista.Count)];
        }
    }

}
