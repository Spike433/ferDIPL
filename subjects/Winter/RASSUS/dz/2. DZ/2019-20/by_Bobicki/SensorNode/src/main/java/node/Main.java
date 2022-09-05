package node;

import com.opencsv.bean.CsvToBeanBuilder;
import model.SensorReading;
import udpclient.StupidUDPClient;
import udpserver.StupidUDPServer;

import java.io.*;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;

public class Main {
    private static final int PORT = ThreadLocalRandom.current().nextInt(10000, 10100); // server port
    private static long startTime = System.nanoTime() / 1000000000;
    private static List<SensorReading> allReadings;
    public static List<Integer> sensorReadings = new ArrayList<>();
    public static Map<Integer, Integer> vectorClock = new HashMap<>();
    private static long scalarClock = new EmulatedSystemClock().currentTimeMillis();

    public static void main(String[] args) {
        try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("ports.txt", true)))) {
            out.println(PORT);
        } catch (IOException e) {
            System.err.println(e);
        }

        try {
            allReadings = new CsvToBeanBuilder<SensorReading>(
                    new FileReader("mjerenja.csv"))
                    .withType(SensorReading.class).build().parse();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        StupidUDPClient udpClient = new StupidUDPClient();
        StupidUDPServer udpServer = new StupidUDPServer();
        Vector node = new Vector();
        node.add(udpClient);
        node.add(udpServer);
        node.add(vectorClock);
        node.add(scalarClock);
        registerSensor(node, sensorReadings);
    }

    private static void registerSensor(Vector node, List<Integer> sensorReadings) {
        System.out.println("*** SENSOR REGISTERED ON PORT: " + PORT + " ***");
        System.out.println();

        new Thread(() -> {
            try {
                StupidUDPClient udpClient = (StupidUDPClient) node.get(0);
                udpClient.startClient(PORT, startTime, allReadings);
            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
        }).start();

        new Thread(() -> {
            try {
                StupidUDPServer udpServer = (StupidUDPServer) node.get(1);
                udpServer.startServer(PORT);
            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
        }).start();

        new Thread(() -> {
            try {
                while (true) {
                    TimeUnit.SECONDS.sleep(5);
                    System.out.println("*** MEASURES IN LAST 5 SECONDS ***");
                    sensorReadings.forEach(System.out::println);
                    double averageMeasure = sensorReadings.stream()
                            .mapToInt(Integer::intValue)
                            .average()
                            .orElse(0.0);
                    averageMeasure = (double)Math.round(averageMeasure * 100d) / 100d;
                    System.out.println("Average measure: " + averageMeasure);
                    System.out.println();
                    sensorReadings.clear();
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
    }
}
