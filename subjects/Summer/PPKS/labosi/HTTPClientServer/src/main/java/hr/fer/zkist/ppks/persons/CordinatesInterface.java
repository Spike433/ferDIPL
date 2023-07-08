package hr.fer.zkist.ppks.persons;

import java.util.List;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public interface CordinatesInterface {

    boolean delete(long id);

    List<Cordinates> get();

    Cordinates get(long id);

    void insert(Cordinates cordinates);

    boolean update(Cordinates cordinates, long id);
    
}
