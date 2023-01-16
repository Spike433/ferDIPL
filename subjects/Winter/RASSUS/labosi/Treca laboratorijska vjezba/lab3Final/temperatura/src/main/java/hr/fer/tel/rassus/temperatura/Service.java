package hr.fer.tel.rassus.temperatura;

import com.opencsv.CSVReader;
import org.springframework.beans.factory.annotation.Autowired;
import java.io.InputStreamReader;

@org.springframework.stereotype.Service
public class Service {
    public static long startTime = System.currentTimeMillis();

    @Autowired
    ReadingRepository readingRepository;

    private void fillReadings() {
        try (var is = getClass().getClassLoader().getResourceAsStream("readings.csv");
             var fr = new InputStreamReader(is);
             var reader = new CSVReader(fr)) {

            String[] nextLine;
            int index = 0;

            reader.readNext();

            while ((nextLine = reader.readNext()) != null) {
                readingRepository.save(new Reading(index, Integer.parseInt(nextLine[0])));
                index += 1;
            }
        } catch (Exception ignored) {

        }

    }

    public Reading currentReading() {
        if (readingRepository.count() == 0)
            fillReadings();

        return readingRepository.findById((int) ((System.currentTimeMillis() - startTime) / 1000 % 100)).get();
    }
}
