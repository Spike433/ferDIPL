package hr.fer.rassus.firsthomework.server;

import hr.fer.rassus.firsthomework.server.model.Measurement;
import hr.fer.rassus.firsthomework.server.model.SensorDescription;
import hr.fer.rassus.firsthomework.server.model.UserAddress;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class SensorController {
    private SensorService sensorService;

    public SensorController(SensorService sensorService) {
        this.sensorService = sensorService;
    }

    @RequestMapping(value = "/register", method = RequestMethod.POST)
    public ResponseEntity<?> register(@RequestBody SensorDescription description) {
        if (sensorService.register(description)) {
            return ResponseEntity.ok()
                    .build();
        }
        else {
            return null;
        }
    }

    @RequestMapping(value = "/searchNeighbour/{username}", method = RequestMethod.GET)
    public UserAddress searchNeighbour(@PathVariable("username") String username) {
        return sensorService.searchNeighbour(username);
    }

    @RequestMapping(value = "/storeMeasurement", method = RequestMethod.POST)
    public ResponseEntity<?> storeMeasurement(@RequestBody Measurement measurement) {
        sensorService.storeMeasurement(measurement);

        return ResponseEntity.ok()
                .build();
    }
}
