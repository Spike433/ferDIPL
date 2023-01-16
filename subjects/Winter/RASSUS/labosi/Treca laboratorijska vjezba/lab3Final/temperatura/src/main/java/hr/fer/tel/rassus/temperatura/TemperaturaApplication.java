package hr.fer.tel.rassus.temperatura;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@EnableDiscoveryClient
@SpringBootApplication
public class TemperaturaApplication {
	public static void main(String[] args) {
		SpringApplication.run(TemperaturaApplication.class, args);
	}

}
