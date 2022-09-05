package udpclient;

import model.SensorReading;
import network.SimpleSimulatedDatagramSocket;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;

import static node.Main.sensorReadings;
import static node.Main.vectorClock;

public class StupidUDPClient {
    public void startClient(int port, long startTime, List<SensorReading> allReadings) throws IOException, InterruptedException {
        DatagramPacket packet = null;
        vectorClock.put(port, 0);

        while (true) {
            long currentTime = System.nanoTime() / 1000000000;
            long duration = currentTime - startTime;
            int readingsLine = (int) (duration % 100) + 2;
            int otherPort = 0;

            // CO
            String coMeasure = allReadings.get(readingsLine).getCo();
            if (coMeasure.isEmpty()) coMeasure = "0";

            byte[] rcvBuf = new byte[256];
            InetAddress address = InetAddress.getByName("localhost");
            DatagramSocket socket = new SimpleSimulatedDatagramSocket(0.2, 200); //SOCKET

            System.out.println("Client sends: " + coMeasure);
            sensorReadings.add(Integer.parseInt(coMeasure));

            byte[] sendBuf;
            sendBuf = coMeasure.getBytes();

            try (BufferedReader br = new BufferedReader(new FileReader("ports.txt"))) {
                String line;
                while ((line = br.readLine()) != null) {
                    if (!line.equals(Integer.toString(port))) {
                        otherPort = Integer.parseInt(line); // port from other node(s)
//                        vectorClock.put(otherPort, 0);
                        packet = new DatagramPacket(sendBuf, sendBuf.length, address, otherPort);
                        socket.send(packet);
                        vectorClock.put(port, vectorClock.get(port) + 1);
                    }
                }
            }

            String receiveString = "";
            DatagramPacket rcvPacket = new DatagramPacket(rcvBuf, rcvBuf.length);

            while (true) {
                try {
                    socket.receive(rcvPacket);
                    vectorClock.put(port, vectorClock.get(port) + 1);
                } catch (SocketTimeoutException e) {
                    Path path = Paths.get("./ports.txt");
                    long lineCount = Files.lines(path).count();

                    if (lineCount > 1) { // if lineCount = 1, there is only one sensor connected
                        System.out.println("Client sends: " + coMeasure + " (retransmission)");
                        packet = new DatagramPacket(sendBuf, sendBuf.length, address, otherPort);
                        socket.send(packet);
                        TimeUnit.SECONDS.sleep(1);
                        continue;
                    } else {
                        break;
                    }
                } catch (IOException ex) {
                    Logger.getLogger(StupidUDPClient.class.getName()).log(Level.SEVERE, null, ex);
                }
                receiveString = new String(rcvPacket.getData(), rcvPacket.getOffset(), rcvPacket.getLength());
                break;
            }
            if (receiveString.isEmpty()) {
                System.out.println("*** No other sensors are yet registered ***");
            } else {
                System.out.println("Client received: " + receiveString + " (" + rcvPacket.getPort() + ")");
            }
            TimeUnit.SECONDS.sleep(1);
        }
    }
}
