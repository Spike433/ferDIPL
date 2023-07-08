package hr.fer.zkist.ppks.persons;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.LinkedList;
import java.util.List;
import  java.io.*;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class CordinatesFactory {

    public static List<Cordinates> generate() throws IOException {
        List<Cordinates> list = new LinkedList<>();

        try ( BufferedReader reader = new BufferedReader(new InputStreamReader(
                new BufferedInputStream(new FileInputStream("lat_lon_time_ISS[1].txt")), "UTF-8"))) {
            String reding;
            while ((reding = reader.readLine()) != null) {
                String[] parts = reding.split(",");
                list.add(new Cordinates(0, Double.parseDouble(parts[0]),Double.parseDouble(parts[1]), Double.parseDouble(parts[2])));
            }
        }

        return list;
    }
}
