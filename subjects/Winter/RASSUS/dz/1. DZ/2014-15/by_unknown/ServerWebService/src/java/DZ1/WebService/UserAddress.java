/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.WebService;

/**
 *
 * @author Marko
 */
public class UserAddress {
    private String address;
    private int port;

    public UserAddress() {
        this.address = "" ;
        this.port = 0 ;
    }
    
    public String getAddress()
    {
        return this.address;
    }
    public int getPort()
    {
        return this.port;
    }
    public void setAddress(String addr)
    {
        this.address = addr;
    }
    public void setPort(int p)
    {
        this.port = p;
    }
}
