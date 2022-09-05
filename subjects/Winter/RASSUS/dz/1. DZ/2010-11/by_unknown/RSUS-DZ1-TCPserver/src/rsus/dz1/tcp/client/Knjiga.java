package rsus.dz1.tcp.client;

/**
 *
 * @author Kristijan Bambir <kristijan.bambir@fer.hr>
 */
public class Knjiga {

    private String naslov;
    private int godinaIzdanja;
    private String izdavac;
    private Autor autor;

    public Knjiga(String naslov, int godinaIzdanja, String izdavac, Autor autor) {
        this.naslov = naslov;
        this.godinaIzdanja = godinaIzdanja;
        this.izdavac = izdavac;
        this.autor = autor;
    }

    public Autor getAutor() {
        return autor;
    }

    public void setAutor(Autor autor) {
        this.autor = autor;
    }

    public int getGodinaIzdanja() {
        return godinaIzdanja;
    }

    public void setGodinaIzdanja(int godinaIzdanja) {
        this.godinaIzdanja = godinaIzdanja;
    }

    public String getIzdavac() {
        return izdavac;
    }

    public void setIzdavac(String izdavac) {
        this.izdavac = izdavac;
    }

    public String getNaslov() {
        return naslov;
    }

    public void setNaslov(String naslov) {
        this.naslov = naslov;
    }

}
