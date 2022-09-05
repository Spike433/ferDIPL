package udpserver;

import network.SimpleSimulatedDatagramSocket;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

import static node.Main.sensorReadings;
import static node.Main.vectorClock;

public class StupidUDPServer {
    public void startServer(int port) throws IOException, InterruptedException {

        byte[] rcvBuf = new byte[256];
        byte[] sendBuf = new byte[256];
        String rcvStr;
        DatagramSocket socket = new SimpleSimulatedDatagramSocket(port, 0.2, 200);

        while (true) {
            DatagramPacket packet = new DatagramPacket(rcvBuf, rcvBuf.length);
            socket.receive(packet);
            vectorClock.put(port, vectorClock.get(port) + 1);

            rcvStr = new String(packet.getData(), packet.getOffset(), packet.getLength());
            System.out.println("Server received: " + rcvStr);
            sensorReadings.add(Integer.parseInt(rcvStr));

            sendBuf = rcvStr.getBytes();
            System.out.println("Server sends: " + rcvStr);

            DatagramPacket sendPacket = new DatagramPacket(sendBuf, sendBuf.length, packet.getAddress(), packet.getPort());
            socket.send(sendPacket);
            vectorClock.put(port, vectorClock.get(port) + 1);
        }
    }
}
