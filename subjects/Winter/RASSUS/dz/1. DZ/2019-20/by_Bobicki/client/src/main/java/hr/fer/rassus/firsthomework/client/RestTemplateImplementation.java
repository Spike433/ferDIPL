package hr.fer.rassus.firsthomework.client;

import hr.fer.rassus.firsthomework.client.model.Measurement;
import hr.fer.rassus.firsthomework.client.model.SensorDescription;
import hr.fer.rassus.firsthomework.client.model.UserAddress;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.web.client.RestTemplate;

public class RestTemplateImplementation implements RestInterface {
    private String baseURL;
    private RestTemplate restTemplate;

    public RestTemplateImplementation(String url) {
        this.baseURL = url;
        restTemplate = new RestTemplate();
        restTemplate.getMessageConverters().add(new MappingJackson2HttpMessageConverter());
    }

    @Override
    public ResponseEntity<String> register(SensorDescription description) {
        ResponseEntity<String> response = restTemplate.postForEntity(baseURL + "/register", description, String.class);
        return response;
    }

    @Override
    public UserAddress searchNeighbour(String username) {
        UserAddress neighbourAddress = restTemplate.getForObject(baseURL + "/searchNeighbour/" + username, UserAddress.class);
        return neighbourAddress;
    }

    @Override
    public ResponseEntity<String> storeMeasurement(Measurement measurement) {
        ResponseEntity<String> response = restTemplate.postForEntity(baseURL + "/storeMeasurement", measurement, String.class);
        return response;
    }
}
