package hr.fer.tel.rassus.sensorAndProducer;

import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;
import java.util.Scanner;

public class Produce {
    private static final String TOPIC = "Command";
    private static final String Stop = "Stop";
    private static final int End = 0;

    public static void main(String[] args) {
        Properties producerProperties = new Properties();
        producerProperties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        producerProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        producerProperties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

        Producer<String, String> producer = new org.apache.kafka.clients.producer.KafkaProducer<>(producerProperties);

        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("Write a message to send to consumer on topic " + TOPIC + "{Start, Stop}");
            String command = sc.nextLine();

            ProducerRecord<String, String> record = new ProducerRecord<>(TOPIC, null, command);

            producer.send(record);
            producer.flush();

            if (command.equals(Stop))
            {
                sc.close();

                System.exit(End);
            }
        }
    }
}