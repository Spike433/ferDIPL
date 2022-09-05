/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.WebService;

import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;

/**
 *
 * @author Marko
 */
@WebService(serviceName = "Service")
public class Service {
        
    final static int MAX_CLIENT = 20 ;
    
    private String[] client;
    private UserAddress[] location;
    private String[] sharedFiles;

    public Service() {
        this.location = new UserAddress[MAX_CLIENT];
        this.sharedFiles = new String[MAX_CLIENT];
        this.client = new String[MAX_CLIENT];
        
        
        for(int i=0;i<MAX_CLIENT;i++){
            this.client[i]="";
            this.sharedFiles[i]="";
            UserAddress tmp = new UserAddress();
            this.location[i] = tmp;
        }
    }
    
    /**
     * Web service: Registrira klijenta na server.
     * @param username
     * @param sharedFiles
     * @param address
     * @param port
     * @return 
     */
    
    @WebMethod(operationName = "Register")
    public Boolean Register(@WebParam(name = "username") String username, @WebParam(name = "sharedFiles") String sharedFiles, @WebParam(name = "address") String address, @WebParam(name = "port") Integer port) {
        
        int freeSlot = MAX_CLIENT;
        
        for(int i=0;i<MAX_CLIENT;i++)
        {
            if(this.client[i].equals("") && freeSlot == MAX_CLIENT)
            {
                freeSlot = i;
            }
            else if(this.client[i].toLowerCase().equals(username.toLowerCase()))
            {
                return false;
            }
        }
        if(freeSlot != MAX_CLIENT)
        {
            this.client[freeSlot] = username;
            this.sharedFiles[freeSlot] = sharedFiles;
            this.location[freeSlot].setPort(port);
            this.location[freeSlot].setAddress(address);
            return true;
        }
        return false;
    }

    /**
     * Web service : traženje datoteka na serveru
     * @param filename
     * @return result
     */
    
    @WebMethod(operationName = "SearchFile")
    public String SearchFile(@WebParam(name = "filename") String filename) {
       
        int i;
        String result;
        result = "";
        for(i=0;i<MAX_CLIENT;i++)
        {
            if(!"".equals(this.client[i]))
            {
                if (this.sharedFiles[i].toLowerCase().contains(filename.toLowerCase())) {
                    result += " " + this.client[i];
                }
            }
        }
        return result;
    }


    /**
     * Web service operation
     * @return 
     */
    @WebMethod(operationName = "listClients")
    public java.lang.String listClients() {
        String result;
        result = "";
        for (int i=0;i<MAX_CLIENT;i++)
        {
            if(this.client[i].equals("")) {
                
            } else {
                result += i+". ->{ IME:"+this.client[i]+" ADRESA:"+this.location[i].getAddress()+" PORT:"+this.location[i].getPort()+" DATOTEKE:"+this.sharedFiles[i]+"}";
            }
        }
        return result;
    }

    /**
     * Web service operation
     * @param username
     * @param address
     * @param port
     * @return 
     */
    @WebMethod(operationName = "logout")
    public boolean logout(@WebParam(name = "username") String username, @WebParam(name = "address") String address, @WebParam(name = "port") int port) {
        
        for(int i=0;i<MAX_CLIENT;i++)
        {
            if(this.client[i].equals(username))
            {
               this.client[i] = "";
               this.location[i].setAddress("");
               this.location[i].setPort(0);
               this.sharedFiles[i] = "";
               return true;
            }
        }
        return false;
    }

    /**
     * Web service operation
     * @param username
     * @return 
     */
    @WebMethod(operationName = "searchUser")
    public UserAddress searchUser(@WebParam(name = "username") String username) {
        for(int i=0;i<MAX_CLIENT;i++)
        {
            if(this.client[i].equals(username))
            {
                return this.location[i];
            }
        }
        return null;
    }
}
