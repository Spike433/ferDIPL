package hr.fer.tel.rassus.agregacija;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.netflix.discovery.EurekaClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.context.annotation.Configuration;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.LinkedList;
import java.util.List;

@RefreshScope
@Configuration
@org.springframework.stereotype.Service
public class Service {
    @Value("${temperatura.jedinica}")
    String temperatureDefaultUnit = "C";

    @Autowired
    private EurekaClient discoveryClient;

    private void convert(Reading reading) {
        if (reading.getUnit().equals(temperatureDefaultUnit))
            return;

        if (reading.getUnit().equals("C") && temperatureDefaultUnit.equals("K")) {
            reading.setUnit("K");
            reading.setValue(reading.getValue() + 273.15);
        }

        if (reading.getUnit().equals("K") && temperatureDefaultUnit.equals("C")) {
            reading.setUnit("C");
            reading.setValue(reading.getValue() - 273.15);
        }
    }
    public List<Reading> currentReadings() throws IOException {
        Reading temperatura, tlak;
        try {
            HttpURLConnection connection = (HttpURLConnection) new URL(discoveryClient.getNextServerFromEureka("TEMPERATURA-MIKROSERVIS", false).getHomePageUrl()).openConnection();
            temperatura = new ObjectMapper().readValue(connection.getInputStream(), Reading.class);
            convert(temperatura);
        } catch (RuntimeException e) {
            temperatura = new Reading("Temperature", temperatureDefaultUnit, null);
        }

        try {
            HttpURLConnection connection = (HttpURLConnection) new URL(discoveryClient.getNextServerFromEureka("TLAK-MIKROSERVIS", false).getHomePageUrl()).openConnection();
            tlak = new ObjectMapper().readValue(connection.getInputStream(), Reading.class);
        } catch (RuntimeException e) {
            tlak = new Reading("Humidity", "%", null);
        }

        List<Reading> r = new LinkedList<>();
        r.add(temperatura);
        r.add(tlak);
        return r;
    }
}
