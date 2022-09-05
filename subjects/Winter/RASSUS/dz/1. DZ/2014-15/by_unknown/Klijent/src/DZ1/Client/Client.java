/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.Client;

/**
 *
 * @author Marko
 */

public class Client{
    public static ConnectionHandler ch;
    public static DataHandler dh;
    
    private static void init(){
        
        ch = new ConnectionHandler();
        dh = new DataHandler();
    }
    
    public static void msg(String from,String msg){
        
        System.out.println("<"+from+"> "+msg);
    }
    
    public static void main(String[] args) {
        
        Client.init();
        ClientGUI cgui = new ClientGUI();
        cgui.start();
    }

    public static Boolean register(java.lang.String username, java.lang.String sharedFiles, java.lang.String address, java.lang.Integer port) {
        DZ1.Client.Service_Service service = new DZ1.Client.Service_Service();
        DZ1.Client.Service sPort = service.getServicePort();
        return sPort.register(username, sharedFiles, address, port);
    }

    public static String searchFile(java.lang.String filename) {
        DZ1.Client.Service_Service service = new DZ1.Client.Service_Service();
        DZ1.Client.Service sPort = service.getServicePort();
        return sPort.searchFile(filename);
    }

    public static boolean logout(java.lang.String username, java.lang.String address, int port) {
        DZ1.Client.Service_Service service = new DZ1.Client.Service_Service();
        DZ1.Client.Service sPort = service.getServicePort();
        return sPort.logout(username, address, port);
    }

    public static UserAddress searchUser(java.lang.String username) {
        DZ1.Client.Service_Service service = new DZ1.Client.Service_Service();
        DZ1.Client.Service sPort = service.getServicePort();
        return sPort.searchUser(username);
    }
}

