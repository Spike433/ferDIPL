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
public class UserAddress {
    private String ipAddress;
    private int port;
    
    public String getAddress()
    {
        return this.ipAddress;
    }
    public int getPort()
    {
        return this.port;
    }
    public void setAddress(String ipAddress)
    {
        this.ipAddress = ipAddress;
    }
    public void setPort(int port)
    {
        this.port = port;
    }
}