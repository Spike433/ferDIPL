package hr.fer.tel.rassus.agregacija;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.util.List;

@RestController
public class Controller {
    @Autowired
    Service service;

    @GetMapping("/")
    private List<Reading> reading() throws IOException {
        return service.currentReadings();
    }
}
