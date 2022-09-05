package hr.fer.rassus.firsthomework.server;

import hr.fer.rassus.firsthomework.server.model.Measurement;
import hr.fer.rassus.firsthomework.server.model.SensorDescription;
import hr.fer.rassus.firsthomework.server.model.UserAddress;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class SensorService {
    private List<SensorDescription> sensors = new ArrayList<>();
    private List<Measurement> measurements = new ArrayList<>();

    public boolean register(SensorDescription description) {
        if (sensors.stream().
                anyMatch(a -> a.getUsername().equals(description.getUsername())))
        {
            System.out.println("Failed to register given sensor, username is already registered!");
            return false;
        }
        else {
            sensors.add(description);
            System.out.println("Sensor " + description.getUsername() + " successfully registered!");
            return true;
        }
    }

    public UserAddress searchNeighbour(String username) {
        if (sensors.size() == 1)  {
            return null;
        }

        Map<UserAddress, Double> distances = new HashMap<>();
        SensorDescription givenSensor = sensors.stream()
                .filter(x -> x.getUsername().equals(username))
                .findFirst()
                .orElse(null);

        for (SensorDescription sensor : sensors) {
            if (!sensor.getUsername().equals(username)) {
                UserAddress userAddress = new UserAddress(sensor.getIpAddress(), sensor.getPort());
                double distance = calculateDistanceBetweenSensors(givenSensor, sensor);
                distances.put(userAddress, distance);
                System.out.println("Distance between " + givenSensor.getUsername() + " and " + sensor.getUsername() + " is " + distance);
            }
        }
        double shortestDistance = Collections.min(distances.values());
        UserAddress neighbourUserAddress = getKeysByValue(distances, shortestDistance);
        System.out.println("Shortest distance is " + shortestDistance);

        return neighbourUserAddress;
    }

    public void storeMeasurement(Measurement measurement) {
        measurements.add(measurement);
        System.out.println("Measurement " + measurement.toString() + " successfully stored!");
    }

    private Double calculateDistanceBetweenSensors(SensorDescription givenSensor, SensorDescription sensor) {
        double lon1 = givenSensor.getLongitude();
        double lon2 = sensor.getLongitude();
        double lat1 = givenSensor.getLatitude();
        double lat2 = sensor.getLatitude();

        double R = 6371;
        double dlon = lon2 - lon1;
        double dlat = lat2 - lat1;
        double a = Math.pow(Math.sin(dlat/2), 2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(dlon/2), 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        double d = R * c;

        return d;
    }

    public static <T, E> T getKeysByValue(Map<T, E> map, E value) {
        Set<T> keys = new HashSet<T>();
        for (Map.Entry<T, E> entry : map.entrySet()) {
            if (Objects.equals(value, entry.getValue())) {
                keys.add(entry.getKey());
            }
        }
        return keys.iterator().next();
    }
}
