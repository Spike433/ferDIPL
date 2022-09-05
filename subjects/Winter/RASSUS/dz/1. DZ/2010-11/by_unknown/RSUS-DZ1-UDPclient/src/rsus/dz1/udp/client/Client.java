package rsus.dz1.udp.client;

import com.sun.org.apache.xml.internal.security.exceptions.Base64DecodingException;
import com.sun.org.apache.xml.internal.security.utils.Base64;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.DatagramPacket;
import java.net.SocketTimeoutException;
import java.util.LinkedList;
import rsus.dz1.udp.network.*;

/**
 *
 * @author Kristijan Bambir <kristijan.bambir@fer.hr>
 */
public class Client {

    public static void main(String[] args) throws IOException, Base64DecodingException {
        String sendString = "Download: File.pdf";

        byte[] rcvBuf = new byte[400];
        byte[] sndBuf = new byte[256];

        sndBuf = sendString.getBytes();

        //Determines the IP adress of a host, given the host's name
        InetAddress adress = InetAddress.getLocalHost();

        //Create a datagram socket and bind it to any available port on
        //the local host
        SimpleSimulatedDatagramSocket socket = new SimpleSimulatedDatagramSocket(0.2, 200);

        //Create a datagram packet for sending data
        DatagramPacket sndPacket = new DatagramPacket(sndBuf, sndBuf.length,
                adress, 50001);

        socket.send(sndPacket);
        
        socket.setSoTimeout(10000);

        LinkedList<String> receivedPacketsList = new LinkedList<String>();
        
        while (true) {
            try
            {
                //receiving packet
                DatagramPacket rcvPacket = new DatagramPacket(rcvBuf, rcvBuf.length);
                socket.receive(rcvPacket);
                String rcvString = new String(rcvPacket.getData(),
                    rcvPacket.getOffset(), rcvPacket.getLength());

                receivedPacketsList.add(rcvString);

                //sending confirmation upon receival
                String packetNumber = rcvString.substring(0, rcvString.indexOf("#"));

                System.out.println("Client receives packet number: "
                        + packetNumber);

                String confirmation = packetNumber;
                sndBuf = confirmation.getBytes();
                DatagramPacket confirmationPacket = new DatagramPacket(sndBuf, sndBuf.length,
                adress, 50001);
                socket.send(confirmationPacket);
                System.out.println("Client sends confirmation of packet number: "
                        + packetNumber);
            } catch (SocketTimeoutException s) {
                break;
            }
        }

        socket.close();

        String tempPacket = receivedPacketsList.get(0);
        tempPacket = tempPacket.substring(receivedPacketsList.get(0).indexOf("#") + 1);
        int numberOfPackets = Integer.parseInt(tempPacket.substring(0,
                receivedPacketsList.get(0).indexOf("#")));
        String[] packetsStringArray = new String[numberOfPackets];

        for (int i = 0; i < receivedPacketsList.size(); i++) {
            int packetNumber = Integer.parseInt(receivedPacketsList.get(i).substring(0,
                    receivedPacketsList.get(i).indexOf("#")));
            String packetString = receivedPacketsList.get(i).substring(
                    receivedPacketsList.get(i).indexOf("#") + 1);
            packetString = packetString.substring(packetString.indexOf("#") + 1);
            packetsStringArray[packetNumber-1] = packetString;
        }

        FileOutputStream fos = new FileOutputStream("src/rsus/dz1/udp/client/Primljeno.doc");
        for (int i = 0; i < packetsStringArray.length; i++) {
            fos.write(Base64.decode(packetsStringArray[i]));
        }

    }

}
