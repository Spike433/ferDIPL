package hr.fer.rassus.firsthomework.client;

import hr.fer.rassus.firsthomework.client.model.Measurement;
import hr.fer.rassus.firsthomework.client.model.SensorDescription;
import hr.fer.rassus.firsthomework.client.model.UserAddress;
import org.springframework.http.ResponseEntity;

public interface RestInterface {
    ResponseEntity<String> register(SensorDescription description);
    UserAddress searchNeighbour(String username);
    ResponseEntity<String> storeMeasurement(Measurement measurement);
}
