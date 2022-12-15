package hr.fer.tel.rassus.sensorAndProducer;

import com.fasterxml.jackson.databind.ObjectMapper;
import hr.fer.tel.rassus.readingSensorModel.ReadingModel;
import hr.fer.tel.rassus.readingSensorModel.SensorModel;
import hr.fer.tel.rassus.stupidudpTemplate.client.StupidUDPClient;
import hr.fer.tel.rassus.stupidudpTemplate.server.StupidUDPServer;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;


import java.io.FileNotFoundException;
import java.io.IOException;
import java.time.Duration;
import java.util.*;

import static hr.fer.tel.rassus.sensorAndProducer.SensConstants.*;

// 5 sec delay after sorting, No2 not working, where are scalar values

public class Sense {

    public static Long sensorStartTime = 0L;
    private static SensorModel findNeigbour(String val) throws IOException
    {
        SensorModel sensorModel1 = new ObjectMapper().readValue(val, SensorModel.class);
        return sensorModel1;
    }

    private static void runSortThread() throws FileNotFoundException {

        new Thread(() -> {
            try {
                while (true){
                    int second = 10000;
                    Thread.sleep(second);

                    String sortMsg = "\nApply sort every 5 sec";
                    System.out.println(sortMsg);
                    ArrayList<ReadingModel> readingModelsForSort = new ArrayList<>();

                    readingModelsForSort.addAll(gotReadingModels);
                    readingModelsForSort.addAll(mySensorReadingModels);

                    applySortAndPrint(readingModelsForSort);
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();

        runStupidUDPClientThread();
        runStupidUDPServer();
    }

    private static void applySortAndPrint(ArrayList<ReadingModel> readingModelsForSort) {
        String before = "\nBefore CSV sort --> " + readingModelsForSort;
        System.out.println(before);
        Collections.sort(readingModelsForSort, new CustomScalarComparator());
        String after = "\nAfter CSV sort --> " + readingModelsForSort;

        Double avg = readingModelsForSort
                .stream()
                .mapToDouble(a -> a.getNO2())
                .average().orElse(0.0);

        System.out.println(after);

        System.out.println("AVG NO2 --> "+avg);
    }

    private static void runStupidUDPServer() {
        new Thread(() -> {
            try {
                StupidUDPServer.RunSensSRV();
            } catch (Exception exception) {
                exception.printStackTrace();
            }
        }).start();
    }

    private static void runStupidUDPClientThread() {
        new Thread(() -> {
            try {
                StupidUDPClient.RunSensCli();
            } catch (Exception exception) {
                exception.printStackTrace();
            }
        }).start();
    }

    private  static String id = "";
    private  static String address = "";

    public static void main(String[] args){
        Properties producerProperties = new Properties();
        producerProperties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        producerProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        producerProperties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

        Producer<String, String> producer = new org.apache.kafka.clients.producer.KafkaProducer<>(producerProperties);

        enterSensorData();

        sensorModel = new SensorModel(Integer.parseInt(id), address, Port);
        StartingTime = emulatedSystemClock.currentTimeMillis();

        ProducerRecord<String, String> record = new ProducerRecord<>(SensConstants.RegosterTopic, null, sensorModel.generateJsonData());

        producer.send(record);
        producer.flush();

        Properties consumerProperties = setupConsumerTemplateProperties();
        Consumer<String, String> consumerCommand = new org.apache.kafka.clients.consumer.KafkaConsumer<>(consumerProperties);
        consumerCommand.subscribe(Collections.singleton(CommandTopic));

        System.out.println("Waiting for messaged to arrive on topic " + CommandTopic);

        Consumer<String, String> consumerRegister = new org.apache.kafka.clients.consumer.KafkaConsumer<>(consumerProperties);
        consumerRegister.subscribe(Collections.singleton(RegosterTopic));
        
        readRegisterUntilStartPressed(consumerRegister);

        runThreadUntilStopPressed(consumerCommand);
    }

    private static void readRegisterUntilStartPressed(Consumer<String, String> consumerRegister) {
        new Thread(() -> {
            printActivatedThread();

            consumerRegister.seekToBeginning(consumerRegister.assignment());

            while (StartProducer == false) {

                ConsumerRecords<String, String> consumerRecords = consumerRegister.poll(Duration.ofMillis(1000));

                for(ConsumerRecord<String,String> messageForRegistration : consumerRecords)
                {
                    try {
                        SensorModel neighbour = findNeigbour(messageForRegistration.value());
                        if (Objects.equals(neighbour.getId(), sensorModel.getId()) == false)
                        {
                            sensorModel.addNeighbour(neighbour);
                            String n = "Show new neighbour --> "+neighbour;
                            System.out.println(n);
                            String neighbours = "My current neighbours: " + sensorModel.getNeighbours();
                            System.out.println(neighbours);
                        }
                    } catch (IOException exception) {
                        exception.printStackTrace();
                    }
                }

                consumerRegister.commitAsync();
            }
            try {
                sensorModel.setVectorValue(0);

                SensConstants.sensVect.put(sensorModel, sensorModel.getNeighbours());
                runSortThread();

            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        }).start();
    }

    private static void runThreadUntilStopPressed(Consumer<String, String> consumerCommand) {
        new Thread(() -> {
            printActivatedThread();

            consumerCommand.seekToBeginning(consumerCommand.assignment());

            while (StopProducer == false) {

                ConsumerRecords<String, String> consumerRecords = consumerCommand.poll(Duration.ofMillis(1000));

                for(ConsumerRecord<String,String> commandForProducer : consumerRecords){
                    String got = "Received --> " + commandForProducer.value();

                    System.out.println(got);

                    if (commandForProducer.value().equals("Stop"))
                    {
                        StopProducer = true;
                    }
                    else if (commandForProducer.value().equals("Start"))
                    {
                        StartProducer = true;
                    }
                }

                consumerCommand.commitAsync();
            }

            System.exit(0);
        }).start();
    }

    private static Properties setupConsumerTemplateProperties() {
        Properties consumerProperties = new Properties();
        consumerProperties.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        consumerProperties.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        consumerProperties.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        consumerProperties.put(ConsumerConfig.GROUP_ID_CONFIG, UUID.randomUUID().toString());
        consumerProperties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        consumerProperties.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        return consumerProperties;
    }

    private static void printActivatedThread() {

    }

    private static void enterSensorData()
    {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Sensor Id -->");
        id = scanner.nextLine(); //"1234";
                //

        System.out.println("Sensor Adreess (localhost) -->");
        address = "localhost";// scanner.nextLine();

        System.out.println("Sensor Port -->");
        Port = scanner.nextLine(); //"3333";
        // scanner.nextLine();
        scanner.close();
    }
}
