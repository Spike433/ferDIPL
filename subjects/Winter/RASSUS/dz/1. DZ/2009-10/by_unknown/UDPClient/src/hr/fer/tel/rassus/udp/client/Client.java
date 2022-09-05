/*
 * This code has been developed at Departement of Telecommunications,
 * Faculty of Electrical Eengineering and Computing, University of Zagreb.
 */
package hr.fer.tel.rassus.udp.client;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class Client {

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) throws IOException {

        String sendString = new String("Any string...");

        byte[] rcvBuf = new byte[256]; // received bytes
        byte[] sendBuf = new byte[256];// sent bytes

        // encode this String into a sequence of bytes using the platform's
        // default charset and store it into a new byte array
        sendBuf = sendString.getBytes();

        // determine the IP address of a host, given the host's name
        InetAddress address = InetAddress.getByName("localhost");

        // create a datagram socket and bind it to any available
        // port on the local host
        DatagramSocket socket = new DatagramSocket(); //SOCKET

        // create a datagram packet for sending data
        DatagramPacket packet = new DatagramPacket(sendBuf, sendBuf.length,
                address, 10001);

        // send a datagram packet from this socket
        socket.send(packet); //SENDTO
        System.out.println("Client sends: " + sendString);

        // create a datagram packet for receiving data
        DatagramPacket rcvPacket = new DatagramPacket(rcvBuf, rcvBuf.length);

        // receive a datagram packet from this socket
        socket.receive(rcvPacket); //RECVFROM

        // construct a new String by decoding the specified subarray of bytes
        // using the platform's default charset
        String rcvString = new String(rcvPacket.getData(), rcvPacket.getOffset(), rcvPacket.getLength());
        System.out.println("Client received: " + rcvString);

        // close the datagram socket
        socket.close(); //CLOSE
    }
}
