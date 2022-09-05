package rsus.dz1.rmi.server;

import java.util.LinkedList;

/**
 *
 * @author Kristijan Bambir <kristijan.bambir@fer.hr>
 */
public class Container {

    private LinkedList<Knjiga> knjigaList;

    public Container() {
        knjigaList = new LinkedList<Knjiga>();
    }

    public void addKnjiga(Knjiga knjiga) {
        knjigaList.add(knjiga);
    }

    public void removeKnjiga(Knjiga knjiga) {
        knjigaList.remove(knjiga);
    }

    public LinkedList<Knjiga> getKnjige() {
        return this.knjigaList;
    }

}
