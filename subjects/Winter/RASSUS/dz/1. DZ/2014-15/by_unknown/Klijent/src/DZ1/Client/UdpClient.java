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
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;
import java.util.LinkedList;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Marko
 */
public class UdpClient implements Runnable{

    private final String fileName;
    private final int indexPeer;
    
    UdpClient(String peer, String fileName) {
        this.fileName = fileName;
        this.indexPeer = Client.ch.getPeerIndex(peer);
    }
    
    @Override
    public void run(){
        
        byte[] rcvBuf = new byte[ConnectionHandler.UDP_PAYLOAD_SIZE+ConnectionHandler.UDP_HEADER_SIZE];
        byte[] sndBuf ;
        byte[] buffer ;
        
        DatagramPacket sndPacket;
        DatagramPacket rcvPacket;
        
        int packetNumber;
        String packetString;
        int payloadLength;
        String listOfRecivedPackets = "";
        LinkedList<byte[]> receivedPacketsList = new LinkedList<>();
        
        Client.msg("UDPClient-"+this.indexPeer,"Pokrenut prijenos ->"+this.fileName+" od korisnika ->"+Client.ch.peer[indexPeer]);
        
// OTVORI SOCKET /////////////////////////
        SimpleSimulatedDatagramSocket socket;
        InetAddress remoteHost;
        int remotePort;
        try {
            //Create a datagram socket and bind it to any available port on
            //the local host
            remotePort = Client.ch.ua[this.indexPeer].getPort();
            remoteHost = InetAddress.getByName(Client.ch.ua[this.indexPeer].getAddress());
            socket = new SimpleSimulatedDatagramSocket(0.2, 200);
        } catch (SocketException | IllegalArgumentException | UnknownHostException ex ) {
            Logger.getLogger(UdpClient.class.getName()).log(Level.SEVERE, null, ex);
            return;
        }
//HANDSHAKE ////////////////////////////////////
    // POŠALJI ZAHTJEV /////////
        sndBuf =("GET#"+Client.ch.myUsername+"#"+ this.fileName+"#").getBytes();
        sndPacket = new DatagramPacket(sndBuf, sndBuf.length,remoteHost, remotePort);
        boolean requestSent = false ;
while(requestSent == false)
{
        try {
            socket.send(sndPacket);
            socket.setSoTimeout(10000);
        } catch (IOException ex) {
            Logger.getLogger(UdpClient.class.getName()).log(Level.SEVERE, null, ex);
        }
// PRIJENOS DATOTEKE //////////////////////////
        while (true) {
        try{
                rcvPacket = new DatagramPacket(rcvBuf, rcvBuf.length);
                socket.receive(rcvPacket);
                requestSent = true ;
                packetString = new String(rcvPacket.getData(), rcvPacket.getOffset(),rcvPacket.getLength());
// PRIMIO PAKET OD SERVERA ///////////////////////
                if(packetString.startsWith("#")){
    // PROČITAJ PODATKE IZ "HEADERA" ////////////////////////////
                    String[] tmp= packetString.split("#");
                    packetNumber = Integer.parseInt(tmp[2]);
                    payloadLength = Integer.parseInt(tmp[3]);
                    Client.msg("UDPClient-"+this.indexPeer, "Dobio paket ->"+packetNumber);
                    int headerLength = (tmp[0]+"#"+tmp[1]+"#"+tmp[2]+"#"+tmp[3]+"#").length();
                 //   Client.msg("UDPClient-"+this.indexPeer, "Header length ->"+headerLength);
    // AKO NEMAM TAJ PAKET POHRANI GA //////////////////////////////
                    if(listOfRecivedPackets.contains(" "+packetNumber+" ") == false)
                    {
                        listOfRecivedPackets += " "+packetNumber+" ";
                        buffer = new byte[payloadLength];
                        System.arraycopy(rcvPacket.getData(),rcvPacket.getOffset()+headerLength, buffer, 0, payloadLength);
                        receivedPacketsList.add(buffer);
                     //   Client.msg("UDPClient-"+this.indexPeer, "Spremam paket ->"+packetNumber);
                      //  Client.msg("UDPClient-"+this.indexPeer, "rcvPacket ->"+rcvPacket.getLength());
                      //  Client.msg("UDPClient-"+this.indexPeer, "Veličina payload -> "+payloadLength);
                      //  Client.msg("UDPClient-"+this.indexPeer, "Veličina buffer -> "+buffer.length);

                    }else
                    {
                        Client.msg("UDPClient-"+this.indexPeer, "Paket ->"+packetNumber+" imam.");
                    }
    // POŠALJI POTVRDU O PRIMITKU PAKETA /////////////////////////////
                    sndBuf =("#"+tmp[1]+"#"+packetNumber+"#"+payloadLength+"#").getBytes();
                    sndPacket = new DatagramPacket(sndBuf, sndBuf.length,remoteHost, remotePort);

                    socket.send(sndPacket);
                    socket.setSoTimeout(10000);
                    
                    Client.msg("UDPClient-"+this.indexPeer, "Poslao potvrdu za paket ->"+packetNumber);
                }else{
                    Client.msg("UDPClient-"+this.indexPeer, "Nerazumljiv odgovor.");
                    break;
                }
    // KAD DOBIJEM SVE PAKETE PRESTANI SLUŠATI SERVER //////////////////////////////
            } catch (SocketTimeoutException ex) {
                break;
            } catch (IOException ex) {
                Logger.getLogger(UdpClient.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
}
/////////////////////////////////////
// SLAŽEM DATOTEKU //////////////////
        if(!"".equals(listOfRecivedPackets))
            Client.dh.makeFileFromLinkedList(this.fileName,receivedPacketsList,listOfRecivedPackets);
        else
            Client.msg("UdpClient", "Server nije poslao ni jedan paket.");
        Client.msg("UdpClient", "Završio s radom.");
    }
}
