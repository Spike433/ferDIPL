namespace SuperManager.Modeli
{
    public class Komentar 
    {
        public string Autor { get; set; }
        public DateTime Datum { get; set; }
        public string? Tekst { get; set; }
    }

    public class UpravljacKomentarima 
    {
        public int RundaId { get; set; }
        
        public string Autor { get; set; }
        public DateTime Datum { get; set; }
        public string? Tekst { get; set; }
        
        public override bool Equals(object? obj)
        {
            var other = obj as UpravljacKomentarima;
            if (other == null) return false;

            return this.RundaId == other.RundaId;
        }
    }
}
