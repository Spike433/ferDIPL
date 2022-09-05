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

public class UdpPacket {
    
    private byte[] payload;
    private boolean isReceived;

    public UdpPacket(byte[] payload) {
        this.payload = payload;
        this.isReceived = false;
    }

    UdpPacket() {
        this.isReceived = false;
    }

    public boolean getIsReceived() {
        return isReceived;
    }

    public void setIsReceived(boolean isReceived) {
        this.isReceived = isReceived;
    }

    public byte[] getPacketData() {
        return payload;
    }

    public void setPacketData(byte[] payload) {
        this.payload = payload;
    }

}