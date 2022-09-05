package rsus.dz1.udp.server;

import com.sun.org.apache.xml.internal.security.utils.Base64;
import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.SocketTimeoutException;
import java.util.LinkedList;
import rsus.dz1.udp.network.*;

/**
 *
 * @author Kristijan Bambir <kristijan.bambir@fer.hr>
 */
public class Server {

    public static void main(String[] args) throws IOException {
        int port = 50001; //server port
        byte[] rcvBuf = new byte[256]; //received bytes
        String rcvString;

        //create an UDP socket and bind it to the specified port on the
        //local host
        SimpleSimulatedDatagramSocket socket = new SimpleSimulatedDatagramSocket(port, 0.2, 200);

        while (true) {
            socket.setSoTimeout(0);

            //create a DataGram packet for receiving packets
            DatagramPacket rcvPacket = new DatagramPacket(rcvBuf, rcvBuf.length);
            //receive packet
            socket.receive(rcvPacket);
            rcvString = new String(rcvPacket.getData(), rcvPacket.getOffset(),
                    rcvPacket.getLength());

            LinkedList<Packet> packetList = new LinkedList<Packet>();

            FileInputStream fis = new FileInputStream("src/rsus/dz1/udp/server/File.doc");
            int size = 256;
            byte[] buffer = new byte[size];
            while (true) {
                int i = fis.read(buffer, 0, size);
                if (i == -1) {
                    break;
                }
                packetList.add(new Packet(Base64.encode(buffer)));
            }

            socket.setSoTimeout(5000);

            try {
                while (true) {
                    sendPackets(packetList, socket, rcvPacket);
                    receivePacketConfirmations(packetList, socket);
                    boolean bool = true;
                    for (int i = 0; i < packetList.size(); i++) {
                        if (packetList.get(i).getIsReceived() == false) {
                            bool = false;
                        }
                    }
                    if (bool == true) break;
                }
            } catch (SocketTimeoutException e) {
                continue;
            }

            System.out.println("File transfer completed!");
        }
    }

    private static String readFileAsString(String filePath) throws java.io.IOException {
        byte[] buffer = new byte[(int) new File(filePath).length()];
        BufferedInputStream f = null;
        try {
            f = new BufferedInputStream(new FileInputStream(filePath));
            f.read(buffer);
        } finally {
            if (f != null) try { f.close(); } catch (IOException ignored) { }
        }
        return new String(buffer);
    }

    private static void sendPackets(LinkedList<Packet> packetList,
            SimpleSimulatedDatagramSocket socket, DatagramPacket rcvPacket) throws IOException {
        for (int j = 0; j < packetList.size(); j++) {
            if (!packetList.get(j).getIsReceived()) {
                int sizeCharacters = (int) Math.floor((double) Math.log10(packetList.size())) + 1;
                byte[] sndBuf = new byte[sizeCharacters + 1 + sizeCharacters + 1 + 256];
                String sequenceNumber = String.format("%0" + sizeCharacters + "d", j + 1);
                String tempString = sequenceNumber + "#" + Integer.toString(packetList.size()) +
                        "#" + packetList.get(j).getPacketData();

                System.out.println("Server sends packet number: " + sequenceNumber);

                sndBuf = tempString.getBytes();
                DatagramPacket sndPacket = new DatagramPacket(sndBuf, sndBuf.length,
                    rcvPacket.getAddress(), rcvPacket.getPort());
                //send packet
                socket.send(sndPacket);
            }
        }
    }

    private static void receivePacketConfirmations(LinkedList<Packet> packetList,
            SimpleSimulatedDatagramSocket socket) throws IOException {
        byte[] rcvBuf = new byte[256];
        while (true) {
            try
            {
                DatagramPacket rcvPacket = new DatagramPacket(rcvBuf, rcvBuf.length);
                socket.receive(rcvPacket);
                String rcvString = new String(rcvPacket.getData(),
                    rcvPacket.getOffset(), rcvPacket.getLength());

                String packetNumber = rcvString;
                System.out.println("Server receives confirmation of packet number: "
                        + packetNumber);

                packetList.get(Integer.parseInt(rcvString) - 1).setIsReceived(true);
            } catch (SocketTimeoutException s) {
                break;
            }
        }
    }

}
