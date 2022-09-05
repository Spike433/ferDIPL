/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.Client;

import DZ1.Network.SimpleSimulatedDatagramSocket;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Marko
 */
public class UdpSender implements Runnable{

    private final int indexPeer;
    private final SimpleSimulatedDatagramSocket socket;

    public UdpSender(SimpleSimulatedDatagramSocket socket, int indexPeer) {
        this.indexPeer = indexPeer;
        this.socket = socket; 
    }

    @Override
    @SuppressWarnings("SleepWhileInLoop")
    public void run() {
        Client.msg("UdpSender-"+this.indexPeer, "Pokrenut.");
        
        boolean sentAll = false;
        while(sentAll == false)
        {
            sentAll = true;
            
            for (int i=0;i<Client.dh.udpFile[indexPeer].length;i++) {
                
                if (Client.dh.udpFile[indexPeer][i].getIsReceived() != true) {
                    sentAll = false;
                    DatagramPacket sndPacket = null;
                    try {
                        sndPacket = new DatagramPacket(Client.dh.udpFile[indexPeer][i].getPacketData(), Client.dh.udpFile[indexPeer][i].getPacketData().length, InetAddress.getByName(Client.ch.ua[indexPeer].getAddress()),Client.ch.ua[indexPeer].getPort());
                    } catch (UnknownHostException ex) {
                        Logger.getLogger(UdpSender.class.getName()).log(Level.SEVERE, null, ex);
                    }
                    try {
                        socket.send(sndPacket);
                    } catch (IOException ex) {
                        Logger.getLogger(UdpSender.class.getName()).log(Level.SEVERE, null, ex);
                    }
                    Client.msg("UdpSender-"+this.indexPeer, "Šaljem paket ->"+i);
                }

            }
            try {
                Thread.sleep(2000);
            } catch (InterruptedException ex) {
                Logger.getLogger(UdpSender.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        Client.msg("UdpSender-"+this.indexPeer, "Prijenos datoteke završen.");
        Client.dh.udpFile[this.indexPeer] = null;
    }
}