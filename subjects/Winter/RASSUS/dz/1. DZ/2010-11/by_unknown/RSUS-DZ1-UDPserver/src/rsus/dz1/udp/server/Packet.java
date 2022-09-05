package rsus.dz1.udp.server;

/**
 *
 * @author Kristijan Bambir <kristijan.bambir@fer.hr>
 */
public class Packet {
    
    private String packetData;
    private boolean isReceived;

    public Packet(String packetData) {
        this.packetData = packetData;
        this.isReceived = false;
    }

    public boolean getIsReceived() {
        return isReceived;
    }

    public void setIsReceived(boolean isReceived) {
        this.isReceived = isReceived;
    }

    public String getPacketData() {
        return packetData;
    }

    public void setPacketData(String packetString) {
        this.packetData = packetString;
    }

}
