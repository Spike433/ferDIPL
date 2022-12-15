/*
 * This code has been developed at Departement of Telecommunications,
 * Faculty of Electrical Engineering and Computing, University of Zagreb.
 */

package hr.fer.tel.rassus.stupidudpTemplate.server;

import hr.fer.tel.rassus.readingSensorModel.ReadingModel;
import hr.fer.tel.rassus.readingSensorModel.SensorModel;
import hr.fer.tel.rassus.stupidudpTemplate.network.SimpleSimulatedDatagramSocket;
import org.springframework.util.SerializationUtils;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.List;

import static hr.fer.tel.rassus.sensorAndProducer.SensConstants.*;


/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */

public class StupidUDPServer {
    /**
     * @param args the command line arguments
     *
     *             receive msg from neighbours
     */

    //static final int PORT = 10001; // server port
    public static void RunSensSRV() throws IOException {

        String msg = new String();
        ReadingModel gotReadingModel;
        byte[] rcvBuf = new byte[256]; // received bytes
        byte[] sendBuffAck; // sent bytes

        // create a UDP socket and bind it to the specified port on the local
        // host
        DatagramSocket socket = new SimpleSimulatedDatagramSocket(Integer.parseInt(Port), 0.3, 1000); //SOCKET -> BIND

        // procces request

        while (StopProducer == false)
        {
            // chack if packet is repeated
            boolean packetIsRepeated = false;

            // create a DatagramPacket for receiving packets
            DatagramPacket packet = new DatagramPacket(rcvBuf, rcvBuf.length);
            // receive packet
            socket.receive(packet); //RECVFROM

            // construct a new String by decoding the specified subarray of
            // bytes
            // using the platform's default charset

            gotReadingModel = (ReadingModel) SerializationUtils.deserialize(packet.getData());
            System.out.println("Server received: " + gotReadingModel);

            for(ReadingModel read : gotReadingModels)
            {
                if (read.equals(gotReadingModel) == true)
                {
                    packetIsRepeated = true;
                    break;
                }
            }

            if (packetIsRepeated == false) {
                msg = "Ack is for: " + gotReadingModel;

                gotReadingModels.add(gotReadingModel);

                sensorModel.setVectorValue(sensorModel.getVectorValue() + 1);

                String bef = "Neighbours before --> : " + sensorModel.getNeighbours();
                System.out.println(bef);
                List<SensorModel> neighbours = sensorModel.getNeighbours();

                for (SensorModel sensorModel : neighbours){

                    if (gotReadingModel.getSensorId() == sensorModel.getId())
                    {
                        sensorModel.setVectorValue(gotReadingModel.getVectorTime());
                    }
                }

                String aft = "Neighbours after --> :" + sensorModel.getNeighbours();
                System.out.println(aft);
            }
            else
            {
                msg = "Ack for repeated -->  " + gotReadingModel;
            }


            // encode a String into a sequence of bytes using the platform's
            // default charset

            sendBuffAck = msg.getBytes();
            System.out.println("Server sends: " + msg);

            // create a DatagramPacket for sending packets
            DatagramPacket sendPacket = new DatagramPacket(sendBuffAck, sendBuffAck.length, packet.getAddress(), packet.getPort());

            socket.send(sendPacket); //SENDTO
        }
    }
}
