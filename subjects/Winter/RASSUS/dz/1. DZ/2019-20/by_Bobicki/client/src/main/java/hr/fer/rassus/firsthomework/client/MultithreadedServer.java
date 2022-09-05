package hr.fer.rassus.firsthomework.client;

import com.opencsv.bean.CsvToBeanBuilder;
import hr.fer.rassus.firsthomework.client.model.Measurement;
import hr.fer.rassus.firsthomework.client.model.SensorDescription;
import hr.fer.rassus.firsthomework.client.model.SensorReading;
import hr.fer.rassus.firsthomework.client.model.UserAddress;

import java.io.FileReader;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class MultithreadedServer implements ServerIf {

    private static final int PORT = 0; // server port
    private static final int NUMBER_OF_THREADS = 4;
    private static final int BACKLOG = 10;

    private final AtomicInteger activeConnections;
    private ServerSocket serverSocket;
    private final ExecutorService executor;
    private final AtomicBoolean runningFlag;
    private RestInterface rest;
    private UserAddress neighbourAddress = null;
    private long startTime = System.nanoTime() / 1000000000;

    public MultithreadedServer() {
        activeConnections = new AtomicInteger(0);
        executor = Executors.newFixedThreadPool(NUMBER_OF_THREADS);
        runningFlag = new AtomicBoolean(false);
        String url = "http://localhost:8080";
        rest = new RestTemplateImplementation(url);
    }

    // Starts all required server services.
    @Override
    public void startup() {
        // create a server socket, bind it to the specified port on the local host
        // and set the max backlog for client requests
        try {
            this.serverSocket = new ServerSocket(PORT, BACKLOG);/*SOCKET->BIND->LISTEN*/;

            // set socket timeout to avoid blocking when there are no new incoming connection requests
            serverSocket.setSoTimeout(500);
            runningFlag.set(true);
            List<SensorReading> sensorReadings = new CsvToBeanBuilder<SensorReading>(
                    new FileReader("mjerenja[3].csv"))
                    .withType(SensorReading.class).build().parse();

            Random rand = new Random();
            double longitude = 15.87 + (16.00 - 15.87) * rand.nextDouble();
            double latitude = 45.75 + (45.85 - 45.75) * rand.nextDouble();
            String ipAddress = serverSocket.getInetAddress().getHostAddress();
            int port = serverSocket.getLocalPort();

            SensorDescription sensor = new SensorDescription("sensor" + port, latitude, longitude, ipAddress, port);
            System.out.println("*** Registering " + sensor.getUsername() + " ***");
            TimeUnit.SECONDS.sleep(1);
            System.out.println(rest.register(sensor));
            System.out.println();
            TimeUnit.SECONDS.sleep(2);

            System.out.println("*** Searching for nearest neighbour ***");
            TimeUnit.SECONDS.sleep(1);
            do {
                neighbourAddress = rest.searchNeighbour(sensor.getUsername());
                if (neighbourAddress == null) {
                    System.out.println("There are currently no other sensors registered, sending own measures to server!");
                    TimeUnit.SECONDS.sleep(2);

                    long currentTime = System.nanoTime() / 1000000000;
                    long duration = currentTime - startTime;
                    int readingsLine = (int)(duration % 100) + 2;
                    int readingsLineToPrint = readingsLine + 2; // indexing in file is different than indexing in readings
                    System.out.println("Duration = " + duration + "s, line to read = " + readingsLineToPrint);
                    TimeUnit.SECONDS.sleep(1);
                    System.out.println("Sensor measured " + sensorReadings.get(readingsLine));
                    TimeUnit.SECONDS.sleep(2);
                    System.out.println();
                    System.out.println("Storing measures to server:");
                    TimeUnit.SECONDS.sleep(1);

                    // Temperature
                    String temperatureMeasure = sensorReadings.get(readingsLine).getTemperature();
                    if (temperatureMeasure.isEmpty()) temperatureMeasure = "0";
                    System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "Temperature", Integer.parseInt(temperatureMeasure))));
                    TimeUnit.SECONDS.sleep(1);

                    // Pressure
                    String pressureMeasure = sensorReadings.get(readingsLine).getPressure();
                    if (pressureMeasure.isEmpty()) pressureMeasure = "0";
                    System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "Pressure", Integer.parseInt(pressureMeasure))));
                    TimeUnit.SECONDS.sleep(1);

                    // Humidity
                    String humidityMeasure = sensorReadings.get(readingsLine).getHumidity();
                    if (humidityMeasure.isEmpty()) humidityMeasure = "0";
                    System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "Humidity", Integer.parseInt(humidityMeasure))));
                    TimeUnit.SECONDS.sleep(1);

                    // CO
                    String coMeasure = sensorReadings.get(readingsLine).getCo();
                    if (coMeasure.isEmpty()) coMeasure = "0";
                    System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "CO", Integer.parseInt(coMeasure))));
                    TimeUnit.SECONDS.sleep(1);

                    // NO2
                    String no2Measure = sensorReadings.get(readingsLine).getNo2();
                    if (no2Measure.isEmpty()) no2Measure = "0";
                    System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "NO2", Integer.parseInt(no2Measure))));
                    TimeUnit.SECONDS.sleep(1);

                    // SO2
                    String so2Measure = sensorReadings.get(readingsLine).getSo2();
                    if (so2Measure.isEmpty()) so2Measure = "0";
                    System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "SO2", Integer.parseInt(so2Measure))));

                    System.out.println();
                    TimeUnit.SECONDS.sleep(5);

                } else {
                    System.out.println("Neighbour found!");
                    TimeUnit.SECONDS.sleep(1);
                    System.out.println("Nearest neighbour is sensor" + neighbourAddress.getPort());
                    System.out.println();
                    TimeUnit.SECONDS.sleep(2);

                    System.out.println("*** Establishing TCP connection with sensor" + neighbourAddress.getPort() + " ***");
                    TimeUnit.SECONDS.sleep(1);
                    new Thread(() -> {
                            TCPClient.main(sensor, neighbourAddress.getPort(), rest, sensorReadings, startTime);
                    }).start();
                }
            } while (neighbourAddress == null);

        }
        catch (SocketException e1) {
            System.err.println("Exception caught when setting server socket timeout: " + e1);
        }
        catch (IOException ex) {
            System.err.println("Exception caught when opening or setting the server socket: " + ex);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void loop() {

        while (runningFlag.get()) {
            try {
                // listen for a connection to be made to server socket from a client
                // accept connection and create a new active socket which communicates with the client
                Socket clientSocket = serverSocket.accept();/*ACCEPT*/

                // execute a new request handler in a new thread
                Runnable worker = new Worker(clientSocket, runningFlag, activeConnections, startTime);
                executor.execute(worker);
                //increment the number of active connections
                activeConnections.getAndIncrement();
            } catch (SocketTimeoutException ste) {
                // do nothing, check the runningFlag flag
            } catch (IOException e) {
                System.err.println("Exception caught when waiting for a connection: " + e);
            }
        }
    }

    @Override
    public void shutdown() {
            System.out.println("Starting server shutdown.");
            try {
                serverSocket.close();
            } catch (IOException e) {
                System.err.println("Exception caught when closing the server socket: " + e);
            } finally {
                executor.shutdown();
            }

            System.out.println("Server has been shutdown.");
    }

    @Override
    public boolean getRunningFlag() {
        return runningFlag.get();
    }

    public static void main(String[] args) {
        ServerIf server = new MultithreadedServer();
        //start all required services
        server.startup();
        //run the main loop for accepting client requests
        server.loop();
        //initiate shutdown when such request is received
        server.shutdown();
    }
}