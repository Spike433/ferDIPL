/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.Client;

import DZ1.Network.SimpleSimulatedDatagramSocket;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.SocketException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Marko
 * 
 */
public class UdpServer implements Runnable{

    @Override
    public void run(){
        
        if(Client.ch.myPort == 0)
        {
            Client.msg("UdpServer","Morate prvo pokrenuti TcpServer, kako bi on definirao port.");
            return ;
        }
        Client.msg("UdpServer","Server pokrenut.");
        SimpleSimulatedDatagramSocket socket;
        try {
            //create an UDP socket and bind it to the specified port on the
            //local host
            socket = new SimpleSimulatedDatagramSocket(Client.ch.myPort, 0.2, 200);
        } catch (SocketException | IllegalArgumentException ex) {
            Logger.getLogger(UdpServer.class.getName()).log(Level.SEVERE, null, ex);
            return ;
        }
        Client.msg("UdpServer","Server sluša na portu -> "+Client.ch.myPort);
        byte[] buff = new byte[512]; //received bytes
        
        String rcvString ;
        
        while (Client.ch.udpServerRunningFlag) {
            try {
                socket.setSoTimeout(0);
            } catch (SocketException ex) {
                Logger.getLogger(UdpServer.class.getName()).log(Level.SEVERE, null, ex);
            }
            DatagramPacket udpDatagram = new DatagramPacket(buff, buff.length);
            try {
                socket.receive(udpDatagram);
            } catch (IOException ex) {
                Logger.getLogger(UdpServer.class.getName()).log(Level.SEVERE, null, ex);
            }
            
            rcvString = new String(udpDatagram.getData(), udpDatagram.getOffset(), udpDatagram.getLength());
            // dosao je zahtjev za datotekom
            if(rcvString.startsWith("GET") == true)
            {
                UserAddress ua = new UserAddress();
                ua.setAddress(udpDatagram.getAddress().getHostAddress());
                ua.setPort(udpDatagram.getPort());
                String[] tmp = rcvString.split("#");
                Client.msg("UdpServer","Korisnik -> "+tmp[1]+" traži datoteku -> "+tmp[2]);
                int indexPeer = Client.ch.checkForFreeSlot();
                if(indexPeer != ConnectionHandler.MAX_PEERS)
                {
                    Client.ch.peer[indexPeer] =tmp[1];
                    Client.ch.ua[indexPeer] = ua;
                    if(Client.dh.packetFileForUdpSender(tmp[2], indexPeer) == true)
                    {
                        Client.msg("UdpServer", "Pokrečem UdpSendera");
                        UdpSender us = new UdpSender(socket,indexPeer);
                        new Thread(us).start();
                    }
                }
                
                // u suprotnom je došla potvrda primitka datoteke
            }else{
                String[] headerField = rcvString.split("#");
                if(headerField.length >= 3)
                {
                    int indexPeer = Integer.parseInt(headerField[1]);
                    int packetNumber = Integer.parseInt(headerField[2]);
                    Client.msg("UdpServer", "Primio potvrdu od korisnika ->"+Client.ch.peer[indexPeer]+" za paket ->"+packetNumber);
                    // na polje 1 je korisničko ime a polje 2 datoteka
                    Client.dh.udpFile[indexPeer][packetNumber].setIsReceived(true);
                }else{
                    Client.msg("UdpServer","Primio ne ispravan zahtjev.");
                }
            }
        }
        socket.close();
        Client.msg("UdpServer","Prekidam sa radom!");
    }
}
