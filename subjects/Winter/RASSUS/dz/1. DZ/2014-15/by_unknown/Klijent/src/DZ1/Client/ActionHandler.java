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
public class ActionHandler {
    
    private String location;
    private String action;
    private String value;

    public ActionHandler() {
        this.value = "" ;
        this.location = "";
        this.action = "";
    }
    
    private void getParameters(String input){

        String[] arg = input.split(" +");
        
        String command = arg[0].trim(); // command form location.action
        arg = command.split("\\.");
        
        this.location = arg[0].trim();
        if(arg.length > 1)
            this.action = arg[1].trim();
        this.value = input.substring(command.length()).trim();
        
    }

    public void start(String input) throws IOException, InterruptedException{
        
            this.getParameters(input);
        
            // naredbe za upravljanje aplikacijom
            // naredbe bez argumenata za komunikaciju sa web uslugom
        switch(this.location.toLowerCase()){
            case "sys":
                switch (this.action.toLowerCase()){
                    case "closeconnections": 
                        this.closeConnections();
                    break;
                    case "start":
                        this.startTCPServer();
                        Thread.sleep(500);
                        this.startUDPServer();
                        this.updateWsRegistration();
                    break;
                    case "listusers":
                        this.listUsers();
                    break;
                    case "removeuser":
                        this.removeUser();
                    break;
                    case "updatefiles":
                        Client.dh.getFilesFromFolder();
                    break;
                    case "listsharedfiles":
                        Client.dh.getSharedFiles();
                    break;
                    default: 
                        this.printUnknownAction();
                    break;
                }
            break;
            case "tcp":
                switch (this.action.toLowerCase()){
                    case "start":
                        this.startTCPServer();
                    break;
                    case "stop":
                        this.stopTCPServer();
                    break;
                    default: 
                        this.printUnknownAction();
                    break;
                }
            break;
            case "udp":
                switch (this.action.toLowerCase()){
                    case "start":
                        this.startUDPServer();
                    break;
                    case "stop":
                        this.stopUDPServer();
                    break;
                    default: 
                        this.printUnknownAction();
                    break;
                }
            break;
            case "ws":
                switch (this.action.toLowerCase()){
                    // naredbe za komunikaciju sa web uslugom
                    case "register": 
                        this.registerToWs();
                    break;
                    case "logout": 
                        this.logoutWs();
                    break;
                    case "searchfile": 
                        this.searchFileOnWs();
                    break;
                    case "searchuser":
                        this.searchUserOnWs();
                    break;
                    case "update":
                        this.updateWsRegistration();
                    break;
                    default: 
                        this.printUnknownAction();
                    break;
                }
            break;
            // ako poruka nije za system ni za web service onda je za klijenta
            // slanje poruke klijentu ili dohvaćanje datoteke
             
            default:
                // ako je akcija msg onda šalješ poruku tom klijentu
                switch (this.action.toLowerCase()){
                    case "msg":
                        this.sendMsgToPeer(this.location, this.value);
                    break;
                    case "get":
                        this.getFileFromPeer(this.location,this.value);
                    break;
                    default: 
                        this.printUnknownAction();
                    break;
                }      
            break;
        }
    }

    private void sendMsgToPeer(String peerUsername, String value) throws IOException, InterruptedException{
        // posaljes poruku klijentu sa usernamom spremljnim u variabli "location"
        TcpClient tc = new  TcpClient();
        tc.sendMsg(peerUsername, value);
    }

    private void getFileFromPeer(String peerUsername, String fileName) {
        // dohvati datoteku od klijenta sa usernamom spremljnim u variabli "location"
        // naziv datoteke u varijabli value               
        UdpClient uc = new UdpClient(peerUsername,fileName);
        new Thread(uc).start();
    }

    private void closeConnections() {
        this.stopTCPServer();
        this.stopUDPServer();
        Client.ch.closeAllTCPListeners();
    }

    private void printUnknownAction() {
        Client.msg("System","Nepoznata naredba.");
    }

    private void registerToWs() {
        if("".equals(Client.ch.myUsername) || "".equals(Client.dh.sharedFiles) || "".equals(Client.ch.myAddress) || Client.ch.myPort == 0)
        {
            Client.msg("System","Prvo pokreni tcp server i postavi username i sharedfolder. ");
            return ;
        }
        Client.msg("System","Registriram se na web uslugu... ");
        if ( Client.register(Client.ch.myUsername, Client.dh.sharedFiles, Client.ch.myAddress,Client.ch.myPort)){
            Client.msg("System","Uspješno registriran na web uslugu.");
        }else{
            Client.msg("System","Pokušaj registracije neuspješan.");
        }
    }

    private void updateWsRegistration() {
       this.logoutWs();
       this.registerToWs();
    }

    private void searchUserOnWs() {
        Client.msg("System","Tražim korisnika "+this.value+ " ... ");
        
        UserAddress ua = Client.searchUser(this.value);
        if(ua == null){
            Client.msg("System","Korisnik "+this.value+" nije pronađen.");
        }
        else{
            Client.msg("System","Korisnik "+this.value+" pronađen.");
            int index = Client.ch.checkForFreeSlot();
            if( index != ConnectionHandler.MAX_PEERS){
                Client.ch.peer[index] = this.value;
                Client.ch.ua[index] =ua;
            }
            else{
                Client.msg("System","Popis pun, novi korisnik nije dodan.");
            }
        }    
    }

    private void searchFileOnWs() {
        Client.msg("System","Šaljem upit za datoteku "+this.value+" .");
        // vraca popis korisnika koji imaju tu datoteku
        String r = Client.searchFile(this.value);
        if (r.equals("") ){
            Client.msg("System","Nepostoji datoteka : "+this.value+" na serveru.");
        }else{
            String[] tmp = r.split(" +");
            for (String tmp1 : tmp) {
                if (!"".equals(tmp1) && !tmp1.equals(Client.ch.myUsername)) {
                    this.value = tmp1;
                    break;
                }
            }
            Client.msg("System","Korisnici koji sadrže traženu datoteku: "+r);
        }    
    }

    private void logoutWs() {
        Client.msg("System","Odjavljujem se sa web usluge ... ");
        if ( Client.logout(Client.ch.myUsername, Client.ch.myAddress,Client.ch.myPort)){
            Client.msg("System","Uspješno odjavljen.");
        }else{
            Client.msg("System","Odjava nije uspjela.");
        }    
    }

    private void startTCPServer() {
        Client.msg("System","Pokrećem TCP server...");
        Client.ch.tcpServerRunningFlag = true;
        TcpServer ts = new TcpServer();
        new Thread(ts).start();
    }

    private void stopTCPServer() {
        Client.msg("System","Gasim TCP server...");
        Client.ch.tcpServerRunningFlag = false;
    }

    private void startUDPServer() {
        Client.msg("System","Pokrećem UDP server...");
        Client.ch.udpServerRunningFlag = true;
        UdpServer us = new UdpServer();
        new Thread(us).start();   
    }

    private void stopUDPServer() {
        Client.msg("System","Gasim UDP server...");
        Client.ch.udpServerRunningFlag = false;
    }

    private void listUsers() {
        Client.msg("System","Popis korisnika : "+Client.ch.listPeers());    
    }

    private void removeUser() {

        for(int i=0;i<Client.ch.peer.length;i++){
            
            if(this.value.equals(Client.ch.peer[i])){
                
                Client.ch.peer[i] = "";
                Client.ch.ua[i] = null;
                Client.ch.tcpSocket[i] = null;
                Client.ch.tcpListenerRunningFlag[i] = false;
                Client.ch.inFromPeer[i] = null;
                Client.ch.outToPeer[i] = null;
                
            }
        }
    }
}
