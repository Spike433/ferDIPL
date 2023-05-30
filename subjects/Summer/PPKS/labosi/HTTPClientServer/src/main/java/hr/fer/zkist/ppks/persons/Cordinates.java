package hr.fer.zkist.ppks.persons;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.List;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class Cordinates {

    private static final Gson gson = new Gson();

    private final long id;
    private double lat, lng, time;

    public Cordinates(long id, double lat, double lng, double time) {
        this.id = id;
        this.lat = lat;
        this.lng = lng;
        this.time = time;
    }

    public long getId() {
        return id;
    }

    public double getLat() {
        return lat;
    }

    public void setLat(double lat) {
        this.lat = lat;
    }

    public double getLng() {
        return lng;
    }

    public void setLng(double lng) {
        this.lng = lng;
    }

    public String toJson() {
        return gson.toJson(this);
    }

    public static Cordinates fromJson(String json) {
        return (Cordinates) gson.fromJson(json, Cordinates.class);
    }
    
    public static String listToJson(List<Cordinates> list) {
        return gson.toJson(list);
    }
    public static List<Cordinates> listFromJson(String json) {
        Type listOfPerson = new TypeToken<List<Cordinates>>() {}.getType();
        List<Cordinates> list = gson.fromJson(json, listOfPerson);
        return list;
    }
}
