/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package DZ1.Client;


import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.LinkedList;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Marko
 */
public class DataHandler {
    public String sharedFiles ;
    public Path sharedFolder ;
    public UdpPacket[][] udpFile ;
    
    public DataHandler(){
        this.sharedFiles = "";
        this.sharedFolder = null;
        this.udpFile = new UdpPacket[ConnectionHandler.MAX_PEERS][];
    }
    
    public void getFilesFromFolder(){
        this.sharedFiles = "";
        Client.msg("DataHandler", "Čitam sve datoteke sa lokacije "+this.sharedFolder);
        try(DirectoryStream<Path> stream= Files.newDirectoryStream(this.sharedFolder))
        {
            for(Path file: stream){
                this.sharedFiles += " "+file.getFileName();
            }
        } catch (IOException e) {
            System.err.println(e);
        }
        Client.msg("DataHandler", "Pročitao : "+this.sharedFiles);
    }
    
    public void getSharedFiles(){
        Client.msg("DataHandler","Dijelim datoteke : "+ sharedFiles);
    }
    
    public String getSharedFolder(){
        return this.sharedFolder.toString();
    }
    
    public void setSharedFolder(String sharedFolder){
        this.sharedFolder = Paths.get(sharedFolder);
        this.getFilesFromFolder();
    }
    
    public boolean packetFileForUdpSender(String fileName, int indexPeer){
        
        Client.msg("DataHandler", "Pripremam datoteku "+fileName+" zaslanje.");
        if(this.udpFile[indexPeer] != null)
        {
            Client.msg("DataHandler", "Korisnik "+Client.ch.peer[indexPeer]+" već preuzima datoteku.");
            return false;
        }
        Client.msg("DataHandler", "Dijelim datoteku "+fileName+" u pakete.");
        FileInputStream fis;
        long numberOfBytesInFile;
        try {
            fis = new FileInputStream(Client.dh.sharedFolder+"\\"+fileName);
            numberOfBytesInFile = fis.getChannel().size();
        } catch (FileNotFoundException ex) {
            Logger.getLogger(DataHandler.class.getName()).log(Level.SEVERE, null, ex);
            Client.msg("DataHandler", "Tražena datoteka "+fileName+" ne postoji.");
            return false;
        } catch (IOException ex) {
            Logger.getLogger(DataHandler.class.getName()).log(Level.SEVERE, null, ex);
            Client.msg("DataHandler", "Ne mogu dohvatiti veličinu datoteke "+fileName);
            return false;
        }
        int numberOfPackets = (int)(numberOfBytesInFile/ConnectionHandler.UDP_PAYLOAD_SIZE)+1;
        
        this.udpFile[indexPeer] = new UdpPacket[numberOfPackets];
        
        byte[] payload = new byte[ConnectionHandler.UDP_PAYLOAD_SIZE];
        byte[] buffer ;
        byte[] header ;
        
        for(int i=0;i<numberOfPackets;i++)
        {
            int numberOfReadBytes;
            try {
                numberOfReadBytes = fis.read(payload, 0, ConnectionHandler.UDP_PAYLOAD_SIZE);
            } catch (IOException ex) {
                Logger.getLogger(DataHandler.class.getName()).log(Level.SEVERE, null, ex);
                Client.msg("DataHandler", "Ne mogu čitati iz datoteke "+fileName);
                return false;
            }
            if(numberOfReadBytes != -1)
            {
                header = ("#"+indexPeer+"#"+i+"#"+numberOfReadBytes+"#").getBytes();
                buffer = new byte[ConnectionHandler.UDP_PAYLOAD_SIZE+ConnectionHandler.UDP_HEADER_SIZE];
                System.arraycopy(header, 0, buffer, 0, header.length);
                System.arraycopy(payload,0,buffer,header.length,numberOfReadBytes);
                this.udpFile[indexPeer][i] = new UdpPacket(buffer);
            }
        }
        Client.msg("DataHandler", "Datoteka "+fileName+" uspješno podjeljena u "+this.udpFile[indexPeer].length+" paketa.");

        try {
            fis.close();
        } catch (IOException ex) {
            Logger.getLogger(DataHandler.class.getName()).log(Level.SEVERE, null, ex);
        }
        return true;
    }

    public boolean prepareUdpFileSlot(int indexPeer, int numberOfPackets) {
        
        if(this.udpFile[indexPeer] == null)
        {
            this.udpFile[indexPeer] = new UdpPacket[numberOfPackets];
            return true;
        }
        Client.msg("DataHandler", "Korisnik "+Client.ch.peer[indexPeer]+" već preuzima datoteku.");
        return false;
    }
    
    public void makeFileFromLinkedList(String fileName,LinkedList<byte[]> receivedPacketsList,String listOfRecivedPackets){ 
        Client.msg("DataHandler", "Spajam datoteku.");
        String[] order = listOfRecivedPackets.trim().split(" +");
        FileOutputStream fos;
        try {
            fos = new FileOutputStream(this.sharedFolder+"\\preuzeo-"+fileName);
        } catch (FileNotFoundException ex) {
            Logger.getLogger(DataHandler.class.getName()).log(Level.SEVERE, null, ex);
            Client.msg("DataHandler", "Nemogu otvoriti datoteku.");
            return ;
        }
        for(int j,i=0;i<order.length;i++)
        {
            for(j=0;j<order.length;j++)
            {
                if(order[j].equals(""+i))
                {  
                    break;
                }
            }
            try{
        //        Client.msg("DataHandler", "Pišem "+receivedPacketsList.get(j).length+" bytova u datoteku");                
                fos.write(receivedPacketsList.get(j));
            } catch (IOException ex) {
                Logger.getLogger(DataHandler.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
            Client.msg("DataHandler", "Gotov.");
    }
}
