package hr.fer.zkist.ppks.readings;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class ReadingWriterReader {

    public static void main(String[] args) throws IOException {
        try ( BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(
                new BufferedOutputStream(new FileOutputStream("readings.json")), "UTF-8"))) {
            writer.write(new Reading("id_1", "temperature", 30.2, "C").toJson());
            writer.newLine();
            writer.write(new Reading("id_1", "temperature", 31.4, "C").toJson());
            writer.newLine();
            writer.write(new Reading("id_1", "temperature", 27.8, "C").toJson());
            writer.newLine();
            writer.write(new Reading("id_2", "temperature", 22.1, "C").toJson());
            writer.newLine();
            writer.write(new Reading("id_2", "temperature", 23.4, "C").toJson());
            writer.newLine();
        }

        try ( BufferedReader reader = new BufferedReader(new InputStreamReader(
                new BufferedInputStream(new FileInputStream("readings.json")), "UTF-8"))) {
            String jsonReading;
            while ((jsonReading = reader.readLine()) != null) {
                System.out.println(Reading.fromJson(jsonReading));
            }
        }
    }
}
