/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.Client;

import java.io.IOException;

/**
 *
 * @author Marko
 */
public class TcpClient {
    
    void sendMsg(String peer, String msg) throws IOException, InterruptedException {
        // provjeri jel postoji taj korisnik
        int index = Client.ch.getPeerIndex(peer);

        if(index == ConnectionHandler.MAX_PEERS)
        {
            Client.msg("TCPClient","Korisnik ne postoji u zapisima, treba ga prvo dohvatiti sa web servisa.");
            return ;
        }
        // provjeri jel već postoji socket prema tom korisniku
        if(Client.ch.tcpSocket[index] == null)
        {
            // ako ne postoji otvori novu TCP konekciju prema tom korisniku
            Client.ch.openTcpSocket(index);
            Client.ch.openTcpStreams(index);
            Client.ch.helloMsg(index);
            
            // pokreni listenera za taj socket u novoj dretvi
            TcpListener tl = new TcpListener(index);
            new Thread(tl).start();
            Thread.sleep(1000);
        }
        // pošalji poruku korisniku
        
        Client.ch.outToPeer[index].println(msg);
        Client.msg(Client.ch.myUsername,peer+" : "+msg);
    }
}
