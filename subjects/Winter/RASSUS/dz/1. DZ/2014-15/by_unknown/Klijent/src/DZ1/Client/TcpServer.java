/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.Client;

import java.net.ServerSocket;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;
/**
 *
 * @author Marko
 */
public class TcpServer implements Runnable{

    @Override
    public void run() {
        Client.msg("TCPserver","Pokrenut.");
        ServerSocket serverSocket;
        try {
            serverSocket = new ServerSocket(0x0); //SOCKET->BIND->LISTEN
            Client.ch.myPort=serverSocket.getLocalPort();
            Client.ch.myAddress = InetAddress.getLocalHost().getHostAddress();
        } catch (IOException ex) {
            Logger.getLogger(TcpServer.class.getName()).log(Level.SEVERE, null, ex);
            return ;
        }
        
        Client.msg("TCPserver","Adresa klijenta: "+Client.ch.myAddress+".");
        Client.msg("TCPserver","Čekam konekcije na portu: "+Client.ch.myPort+".");
        
        Socket newSocket ;
        while (Client.ch.tcpServerRunningFlag) {
            // create a new socket, accept and listen for a connection to be
            // made to this socket
            try {
                    newSocket = serverSocket.accept(); //ACCEPT
            } catch (IOException ex) {
                Logger.getLogger(TcpServer.class.getName()).log(Level.SEVERE, null, ex);
                return ;
            }
            // dosao je novi korisnik
            // probaj ga dodati u listu
            int indexPeer = Client.ch.checkForFreeSlot();
            Client.ch.tcpSocket[indexPeer] = newSocket;
            if(indexPeer != ConnectionHandler.MAX_PEERS)
            {
                Client.ch.openTcpStreams(indexPeer);
                Client.ch.helloMsg(indexPeer);
                // korisnik je dodan pokreni dretvu za njega
                TcpListener ls =new TcpListener(indexPeer);
                new Thread(ls).start();

            }
            else
            {
                try {
                    // korisnik nije dodan ignoriraj i nastavi slušati za dolazne zahtjeve
                    newSocket.close();
                } catch (IOException ex) {
                    Logger.getLogger(TcpServer.class.getName()).log(Level.SEVERE, null, ex);
                }
                Client.msg("TCPserver","Nemoguće prihvatiti konekciju previše korisnika spojenih na klijent");
            }
        }
        
        try {
            serverSocket.close();
        } catch (IOException ex) {
            Logger.getLogger(TcpServer.class.getName()).log(Level.SEVERE, null, ex);
        }
        Client.msg("TCPserver","TCPserver ugašen.");
    } 
}
