/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.Client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Marko
 */
public class ConnectionHandler {
    public static int MAX_PEERS = 20;
    public static int UDP_PAYLOAD_SIZE = 10000;
    public static int UDP_HEADER_SIZE = 50 ;
    
    // running flags
    public boolean tcpServerRunningFlag;
    public boolean udpServerRunningFlag;
    public boolean[] tcpListenerRunningFlag;
    
    // list of peers
    public String[] peer;           
    public UserAddress[] ua;
    
    // TCP connetion
    public Socket[] tcpSocket;
    public PrintStream [] outToPeer ;
    public BufferedReader [] inFromPeer ;
     
    // who am i?
    public int myPort;
    public String myAddress;
    public String myUsername;
      
    public ConnectionHandler(){
        // initiate global variables
        this.tcpSocket = new Socket[MAX_PEERS];
        this.outToPeer = new PrintStream[MAX_PEERS];
        this.inFromPeer = new BufferedReader[MAX_PEERS];
        this.peer = new String[MAX_PEERS];
        this.tcpListenerRunningFlag = new boolean[MAX_PEERS];
        this.tcpServerRunningFlag = false;
        this.udpServerRunningFlag = false;
        
        this.myPort = 0;
        this.myAddress = "";
        this.myUsername = "";
        
        ua = new UserAddress[MAX_PEERS];
        for(int i=0;i<MAX_PEERS;i++)
        {
            
            this.peer[i] = "";
            UserAddress tmp = new UserAddress();
            ua[i] = tmp;
            this.tcpListenerRunningFlag[i] = false;
            
        }
    ///////////////////////////////////////////////////////
    }
    
    public int checkForFreeSlot(){
        for(int i=0;i<MAX_PEERS;i++)
        {
            if("".equals(this.peer[i]))
            {
                return i;
            }
        }
        return MAX_PEERS;
    }
    
    public int getPeerIndex(String username){
        int i;
        for(i=0;i<MAX_PEERS;i++)
        {
            if(this.peer[i].equals(username))
            {
                break;
            }
        }
        return i;
    }
    
    public void closeAllTCPListeners(){
        
        Client.msg("ConnectionHandler","Gasim sve TCP konekcije prema korisnicima...");
        for(int i=0;i<MAX_PEERS;i++)
        {
            this.tcpListenerRunningFlag[i] = false;
            this.inFromPeer[i] = null;
            this.outToPeer[i] = null;
            this.tcpSocket[i] = null;
        }
        Client.msg("System","Sve TCP konekcije su prekinute.");
    }

    public String listPeers() {
        
        String result= "";
        for(int i=0;i<MAX_PEERS;i++)
        {
            if(!"".equals(this.peer[i]))
            {
                result += (this.peer[i])+" ";
            }
        }
       return result; 
    }
    
    // TCP connection methods
    
    public void openTcpSocket(int index) throws IOException {
        this.tcpSocket[index]= new Socket(this.ua[index].getAddress(),this.ua[index].getPort()); //SOCKET->CONNECT    
    }
    
    public void openTcpStreams(int index){
        try {
            this.outToPeer[index] = new PrintStream(this.tcpSocket[index].getOutputStream());
            this.inFromPeer[index] = new BufferedReader(new InputStreamReader(this.tcpSocket[index].getInputStream()));
        } catch (IOException ex) {
            Logger.getLogger(ConnectionHandler.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    public void helloMsg(int indexPeer) {
        Client.ch.outToPeer[indexPeer].println("@"+Client.ch.myUsername);    }
    
    public void closeTcpConnection(int index) {
        this.tcpSocket[index] = null;
        this.outToPeer[index] = null;
        this.inFromPeer[index] = null;
    }
}
