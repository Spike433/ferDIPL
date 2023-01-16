package hr.fer.tel.rassus.tlak;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@EnableDiscoveryClient
@SpringBootApplication
public class TlakApplication {

	public static void main(String[] args) {
		SpringApplication.run(TlakApplication.class, args);
	}

}
