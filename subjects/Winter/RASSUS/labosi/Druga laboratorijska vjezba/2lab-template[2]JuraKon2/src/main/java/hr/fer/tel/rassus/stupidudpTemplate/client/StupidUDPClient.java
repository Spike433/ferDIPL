/*
 * This code has been developed at Departement of Telecommunications,
 * Faculty of Electrical Eengineering and Computing, University of Zagreb.
 */

package hr.fer.tel.rassus.stupidudpTemplate.client;

import com.opencsv.bean.CsvToBeanBuilder;
import hr.fer.tel.rassus.readingSensorModel.ReadingModel;
import hr.fer.tel.rassus.readingSensorModel.SensorModel;
import hr.fer.tel.rassus.stupidudpTemplate.network.*;
import org.springframework.util.SerializationUtils;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import static hr.fer.tel.rassus.sensorAndProducer.SensConstants.*;
import static hr.fer.tel.rassus.sensorAndProducer.Sense.sensorStartTime;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 *
 *     update all neighbours
 */
public class StupidUDPClient {

        static final int PORT = 10001; // server port

    public static ReadingModel ReadFromCSV(int getReading) throws FileNotFoundException
    {
        List<ReadingModel> readings = new CsvToBeanBuilder<ReadingModel>(new FileReader("readings.csv"))
                .withType(ReadingModel.class).build().parse();
        ReadingModel readingModel = new ReadingModel();
        readingModel.setNO2(readings.get(getReading).getNO2());
        return readingModel;
    }

    public static void main(String args[]) throws IOException {

//        String sendString = "Any string...";
//
//        byte[] rcvBuf = new byte[256]; // received bytes
//
//        // encode this String into a sequence of bytes using the platform's
//        // default charset and store it into a new byte array
//
//        // determine the IP address of a host, given the host's name
//        InetAddress address = InetAddress.getByName("localhost");
//
//        // create a datagram socket and bind it to any available
//        // port on the local host
//        //DatagramSocket socket = new SimulatedDatagramSocket(0.2, 1, 200, 50); //SOCKET
//        DatagramSocket socket = new SimpleSimulatedDatagramSocket(0.2, 200); //SOCKET
//
//        System.out.print("Client sends: ");
//        // send each character as a separate datagram packet
//        for (int i = 0; i < sendString.length(); i++) {
//            byte[] sendBuf = new byte[1];// sent bytes
//            sendBuf[0] = (byte) sendString.charAt(i);
//
//            // create a datagram packet for sending data
//            DatagramPacket packet = new DatagramPacket(sendBuf, sendBuf.length,
//                    address, PORT);
//
//            // send a datagram packet from this socket
//            socket.send(packet); //SENDTO
//            System.out.print(new String(sendBuf));
//        }
//        System.out.println("");
//
//        StringBuffer receiveString = new StringBuffer();
//
//        while (true) {
//            // create a datagram packet for receiving data
//            DatagramPacket rcvPacket = new DatagramPacket(rcvBuf, rcvBuf.length);
//
//            try {
//                // receive a datagram packet from this socket
//                socket.receive(rcvPacket); //RECVFROM
//            } catch (SocketTimeoutException e) {
//                break;
//            } catch (IOException ex) {
//                Logger.getLogger(StupidUDPClient.class.getName()).log(Level.SEVERE, null, ex);
//            }
//
//            // construct a new String by decoding the specified subarray of bytes
//            // using the platform's default charset
//            receiveString.append(new String(rcvPacket.getData(), rcvPacket.getOffset(), rcvPacket.getLength()));
//
//        }
//        System.out.println("Client received: " + receiveString);
//
//        // close the datagram socket
//        socket.close(); //CLOSE
    }
       public static void RunSensCli() throws IOException, InterruptedException {

       long currentTime;

       ReadingModel generatedReadingModel;

       // create a datagram socket and bind it to any available
       // port on the local host

       // simualte 30% loss with 1s delay
       DatagramSocket socket = new SimpleSimulatedDatagramSocket(0.3, 1000); //SOCKET

        while (StopProducer == false)
        {
            Thread.sleep(2200);

            currentTime = emulatedSystemClock.currentTimeMillis();
            generatedReadingModel = ReadFromCSV((int) ((currentTime - sensorStartTime) / 1000) % 100+1);

            int increase = sensorModel.getVectorValue() + 1;
            sensorModel.setVectorValue(increase);

            generatedReadingModel.setSensorId(sensorModel.getId());
            generatedReadingModel.setVectorTime(sensorModel.getVectorValue());
            generatedReadingModel.setScalarTime(currentTime);

            mySensorReadingModels.add(generatedReadingModel);

            // encode this String into a sequence of bytes using the platform's
            // default charset and store it into a new byte array


            // determine the IP address of a host, given the host's name
            InetAddress address = InetAddress.getByName("localhost");

            System.out.println("Client sends: " + generatedReadingModel);
            // send each character as a separate datagram packet

            byte[] sendBuf = SerializationUtils.serialize(generatedReadingModel);
            byte [] confirm = new byte[256];

            DatagramPacket packetAck = new DatagramPacket(confirm, confirm.length);;

            List<SensorModel> neighbours = sensorModel.getNeighbours();
            for (SensorModel neighbour : neighbours){

                // create a datagram packet for sending data
                DatagramPacket packet = new DatagramPacket(sendBuf, sendBuf.length, address, Integer.parseInt(neighbour.getPort()));

                while (true)
                {
                    // send a datagram packet from this socket
                    socket.send(packet); //SENDTO
                    try
                    {
                        // ack is on its way

                        socket.receive(packetAck);

                        String receiveString = new String(packetAck.getData(), packetAck.getOffset(), packetAck.getLength());

                        String ack = "Ack recevided --> " + receiveString;
                        System.out.println(ack);

                        break;
                    } catch (SocketTimeoutException e)
                    {
                        String lost = "I lost packet, sending again \n";
                        System.out.println(lost);
                    } catch (Exception exception) // todo add IoEx if needed
                    {
                        Logger.getLogger(StupidUDPClient.class.getClass().getName()).log(Level.ALL, "Something went wrong", exception);
                    }
                }
            }

            System.out.print("\n");
        }

        // close the datagram socket
        socket.close(); //CLOSE
    }

    private static String path = "/home/osboxes/Desktop/2lab-templateJura/src/main/java/hr/fer/tel/rassus/data/readings.csv";

}
