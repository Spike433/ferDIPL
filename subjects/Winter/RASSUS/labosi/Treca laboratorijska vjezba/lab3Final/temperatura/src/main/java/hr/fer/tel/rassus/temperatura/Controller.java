package hr.fer.tel.rassus.temperatura;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Controller {
    @Autowired
    Service service;

    @GetMapping("/")
    private ReadingResponse reading() {
        return new ReadingResponse(service.currentReading());
    }
}
