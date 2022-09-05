/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.Client;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Marko
 */
class TcpListener implements Runnable{
    
    final private int connectionIdentifier;

    public TcpListener(int index) {

        this.connectionIdentifier = index;
    }

    @Override
    public void run() {
        Client.ch.tcpListenerRunningFlag[this.connectionIdentifier] = true;
        String peer = "unknown";
        String rcvString ;

        try {
            while(Client.ch.tcpListenerRunningFlag[this.connectionIdentifier]
                    && (rcvString = Client.ch.inFromPeer[this.connectionIdentifier].readLine())!= null)
            {   
                if (rcvString.startsWith("@")) {
                    // dodaj ime korisnika u list
                    peer = rcvString.substring(1);
                    Client.msg("TCPListener-"+this.connectionIdentifier,"Spojen sa klijentom "+peer);
                    Client.ch.peer[this.connectionIdentifier] = peer;
                    continue;
                }
                // ispisi poruku korisnika u textbox
                Client.msg(peer,rcvString);
            }
        } catch (IOException ex) {
            Logger.getLogger(TcpListener.class.getName()).log(Level.SEVERE, null, ex);
        }
        Client.msg("TCPListener-"+this.connectionIdentifier,"Korisnik "+peer+" je napustio razgovor");
        Client.ch.tcpListenerRunningFlag[this.connectionIdentifier] = false;
        Client.ch.closeTcpConnection(this.connectionIdentifier);
    }
}