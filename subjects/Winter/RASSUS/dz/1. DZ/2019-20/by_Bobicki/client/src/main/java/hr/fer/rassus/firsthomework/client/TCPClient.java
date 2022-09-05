package hr.fer.rassus.firsthomework.client;

import hr.fer.rassus.firsthomework.client.model.Measurement;
import hr.fer.rassus.firsthomework.client.model.SensorDescription;
import hr.fer.rassus.firsthomework.client.model.SensorReading;

import java.io.*;
import java.net.Socket;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class TCPClient {
    final static String SERVER_NAME = "localhost"; // server name

    public static void main(SensorDescription sensor, int port, RestInterface rest, List<SensorReading> sensorReadings, long startTime) {

        // create a client socket and connect it to the name server on the specified port number
        try (Socket clientSocket = new Socket(SERVER_NAME, port)/*SOCKET->CONNECT*/) {

            // get the socket's output stream and open a PrintWriter on it
            PrintWriter outToServer = new PrintWriter(new OutputStreamWriter(
                    clientSocket.getOutputStream()), true);

            // get the socket's input stream and open a BufferedReader on it
            BufferedReader inFromServer = new BufferedReader(new InputStreamReader(
                    clientSocket.getInputStream()));

            BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
            String inputString;
            System.out.println("Type in \"measure\" to start the measuring process (to stop the measuring process, press Enter key and wait): ");

            while ((inputString = in.readLine()) != null && inputString.length() != 0) {
                System.out.println();
                if (inputString.equals("measure")) {
                    while (System.in.available() == 0) { // loop until keypress
                        // send a String then terminate the line and flush
                        outToServer.println(inputString);//WRITE
                        System.out.println("TCPClient sent: " + inputString);
                        TimeUnit.SECONDS.sleep(1);
                        // read a line of text received from server
                        String rcvString = inFromServer.readLine();//READ
                        System.out.println("TCPClient received: " + rcvString + " (duration + line to read)");
                        System.out.println();
                        TimeUnit.SECONDS.sleep(2);

                        long currentTime = System.nanoTime() / 1000000000;
                        long homeDuration = currentTime - startTime;
                        int homeReadingsLine = (int)(homeDuration % 100) + 2;
                        int homeReadingsLineToPrint = homeReadingsLine + 2; // indexing in file is different than indexing in readings

                        String[] tokens = rcvString.split("\\+");
                        long neighbourDuration = Long.parseLong(tokens[0]);
                        int neighbourReadingsLine = Integer.parseInt(tokens[1]);
                        int neighbourReadingsLineToPrint = neighbourReadingsLine + 2; // indexing in file is different than indexing in readings

                        System.out.println("Home sensor, duration = " + homeDuration + "s, line to read = " + homeReadingsLineToPrint);
                        TimeUnit.SECONDS.sleep(1);
                        System.out.println("Home sensor measured " + sensorReadings.get(homeReadingsLine));
                        TimeUnit.SECONDS.sleep(2);
                        System.out.println();
                        System.out.println("Neighbour sensor, duration = " + neighbourDuration + "s, line to read = " + neighbourReadingsLineToPrint);
                        TimeUnit.SECONDS.sleep(1);
                        System.out.println("Neighbour sensor measured " + sensorReadings.get(neighbourReadingsLine));
                        System.out.println();
                        TimeUnit.SECONDS.sleep(2);

                        float averageValue;

                        System.out.println("Storing measures to server:");
                        TimeUnit.SECONDS.sleep(1);

                        // Temperature
                        String temperatureHomeMeasure = sensorReadings.get(homeReadingsLine).getTemperature();
                        if (temperatureHomeMeasure.isEmpty()) temperatureHomeMeasure = "0";
                        String temperatureNeighbourMeasure = sensorReadings.get(neighbourReadingsLine).getTemperature();
                        if (temperatureNeighbourMeasure.isEmpty()) temperatureNeighbourMeasure = "0";
                        averageValue = calculateAverageValue(temperatureHomeMeasure, temperatureNeighbourMeasure);
                        System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "Temperature", averageValue)));
                        TimeUnit.SECONDS.sleep(1);

                        // Pressure
                        String pressureHomeMeasure = sensorReadings.get(homeReadingsLine).getPressure();
                        if (pressureHomeMeasure.isEmpty()) pressureHomeMeasure = "0";
                        String pressureNeighbourMeasure = sensorReadings.get(neighbourReadingsLine).getPressure();
                        if (pressureNeighbourMeasure.isEmpty()) pressureNeighbourMeasure = "0";
                        averageValue = calculateAverageValue(pressureHomeMeasure, pressureNeighbourMeasure);
                        System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "Pressure", averageValue)));
                        TimeUnit.SECONDS.sleep(1);

                        // Humidity
                        String humidityHomeMeasure = sensorReadings.get(homeReadingsLine).getHumidity();
                        if (humidityHomeMeasure.isEmpty()) humidityHomeMeasure = "0";
                        String humidityNeighbourMeasure = sensorReadings.get(neighbourReadingsLine).getHumidity();
                        if (humidityNeighbourMeasure.isEmpty()) humidityNeighbourMeasure = "0";
                        averageValue = calculateAverageValue(humidityHomeMeasure, humidityNeighbourMeasure);
                        System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "Humidity", averageValue)));
                        TimeUnit.SECONDS.sleep(1);

                        // CO
                        String coHomeMeasure = sensorReadings.get(homeReadingsLine).getCo();
                        if (coHomeMeasure.isEmpty()) coHomeMeasure = "0";
                        String coNeighbourMeasure = sensorReadings.get(neighbourReadingsLine).getCo();
                        if (coNeighbourMeasure.isEmpty()) coNeighbourMeasure = "0";
                        averageValue = calculateAverageValue(coHomeMeasure, coNeighbourMeasure);
                        System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "CO", averageValue)));
                        TimeUnit.SECONDS.sleep(1);

                        // NO2
                        String no2HomeMeasure = sensorReadings.get(homeReadingsLine).getNo2();
                        if (no2HomeMeasure.isEmpty()) no2HomeMeasure = "0";
                        String no2NeighbourMeasure = sensorReadings.get(neighbourReadingsLine).getNo2();
                        if (no2NeighbourMeasure.isEmpty()) no2NeighbourMeasure = "0";
                        averageValue = calculateAverageValue(no2HomeMeasure, no2NeighbourMeasure);
                        System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "NO2", averageValue)));
                        TimeUnit.SECONDS.sleep(1);

                        // SO2
                        String so2HomeMeasure = sensorReadings.get(homeReadingsLine).getSo2();
                        if (so2HomeMeasure.isEmpty()) so2HomeMeasure = "0";
                        String so2NeighbourMeasure = sensorReadings.get(neighbourReadingsLine).getSo2();
                        if (so2NeighbourMeasure.isEmpty()) so2NeighbourMeasure = "0";
                        averageValue = calculateAverageValue(so2HomeMeasure, so2NeighbourMeasure);
                        System.out.println(rest.storeMeasurement(new Measurement(sensor.getUsername(), "SO2", averageValue)));

                        System.out.println();
                        TimeUnit.SECONDS.sleep(5);
                    }
                }
                else {
                    System.out.println("Invalid command, please type in \"measure\" to start the measuring process!");
                    continue;
                }
                System.out.println("Getting measures from neighbour stopped, shutting down server!");
                outToServer.println("shutdown");
                System.out.println("TCPClient received: " + inFromServer.readLine());
                break;
            }
        }
        catch (IOException ex) {
            System.err.println("Exception caught when opening the socket or trying to read data: " + ex);
            System.exit(1);
        }
        catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private static float calculateAverageValue(String homeMeasure, String neighbourMeasure) {
        float averageValue;
        if (homeMeasure.equals("0") || neighbourMeasure.equals("0")) {
            averageValue = (Integer.parseInt(homeMeasure) + (float)Integer.parseInt(neighbourMeasure));
        }
        else {
            averageValue = (Integer.parseInt(homeMeasure) + (float)Integer.parseInt(neighbourMeasure)) / 2;
        }
        return averageValue;
    }
}