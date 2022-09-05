/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.Network;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketException;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SimpleSimulatedDatagramSocket extends DatagramSocket {

    private double lossRate;
    private int averageDelay;
    private Random random;

    //use this constructor for the server side (no timeout)
    public SimpleSimulatedDatagramSocket(int port, double lossRate, int averageDelay) throws SocketException, IllegalArgumentException {
        super(port);
        random = new Random();

        this.lossRate = lossRate;
        this.averageDelay = averageDelay;

        //set time to wait for answer
        this.setSoTimeout(0);
    }

    //use this constructor for the client side (timeout = 4 * averageDelay)
    public SimpleSimulatedDatagramSocket(double lossRate, int averageDelay) throws SocketException, IllegalArgumentException {
        random = new Random();

        this.lossRate = lossRate;
        this.averageDelay = averageDelay;

        //set time to wait for answer
        this.setSoTimeout(4 * averageDelay);
    }

    @Override
    public void send(DatagramPacket packet) throws IOException {
        if (random.nextDouble() >= lossRate) {
            //delay is uniformely distributed between 0 and 2*averageDelay
            new Thread(new OutgoingDatagramPacket(packet, (long) (2 * averageDelay * random.nextDouble()))).start();
        }
    }

    /**
     * Inner class for internal use.
     */
    private class OutgoingDatagramPacket implements Runnable {

        private DatagramPacket packet;
        private long time;

        private OutgoingDatagramPacket(DatagramPacket packet, long time) {
            this.packet = packet;
            this.time = time;
        }

        public void run() {
            try {
                //simulate network delay
                Thread.sleep(time);
                SimpleSimulatedDatagramSocket.super.send(packet);
            } catch (InterruptedException e) {
                Thread.interrupted();
            } catch (IOException ex) {
                Logger.getLogger(SimulatedDatagramSocket.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
}

