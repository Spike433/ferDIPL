package hr.fer.zkist.ppks.persons;

import java.io.IOException;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class CordinatesService {

    private final List<Cordinates> cordinates = CordinatesFactory.generate();

    public CordinatesService() throws IOException {
    }

    public List<Cordinates> get() {
        Collections.sort(cordinates, Comparator.comparing(Cordinates::getId));
        return cordinates;
    }

    public void insert(Cordinates cordinates) {
        this.cordinates.add(cordinates);
    }
    
    public Cordinates get(long id) {
        for (Cordinates cordinates : this.cordinates) {
            if (cordinates.getId() == id) {
                return cordinates;
            }
        }

        return null;
    }

    public boolean delete(long id) {
        Iterator<Cordinates> iterator = cordinates.iterator();

        while (iterator.hasNext()) {
            if (iterator.next().getId() == id) {
                iterator.remove();
                return true;
            }
        }

        return false;
    }

    public boolean update(Cordinates cordinates, long id) {
        Iterator<Cordinates> iterator = this.cordinates.iterator();

        boolean updated = false;
        while (iterator.hasNext()) {
            if (iterator.next().getId() == id) {
                iterator.remove();
                updated = true;
                break;
            }
        }
        if (updated)
            this.cordinates.add(cordinates);

        return updated;
    }
}

