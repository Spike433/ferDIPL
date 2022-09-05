package rsus.dz1.tcp.client;

import com.thoughtworks.xstream.*;
import com.thoughtworks.xstream.io.xml.DomDriver;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.LinkedList;

/**
 *
 * @author Kristijan Bambir <kristijan.bambir@fer.hr>
 */
public class Client {

    public static void main(String[] args) throws IOException {
        String serverName = "localhost"; // server name
        int port = 50002; // server port
        String rcvXml = "";

        // create a stream socket and connect it to the specified port number
        // on the named host
        Socket clientSocket = new Socket(serverName, port);//SOCKET->CONNECT

        XStream xstream = new XStream(new DomDriver());
        xstream.alias("autor", Autor.class);
        xstream.alias("knjiga", Knjiga.class);

        Autor marko = new Autor("Marko", "Marković", "43162758945");
        Autor ivan = new Autor("Ivan", "Horvat", "75245698531");
        Autor hrvoje = new Autor("Hrvoje", "Lujo", "45124786358");
        Autor matija = new Autor("Matija", "Ban", "71234895153");
        Knjiga pustinja = new Knjiga("Pustinja", 2005, "Algoritam", marko);
        Knjiga subota = new Knjiga("Subota", 2007, "Profil", ivan);
        Knjiga windows = new Knjiga("Windows", 2005, "Algoritam", hrvoje);

        Container container = new Container();
        container.addKnjiga(pustinja);
        container.addKnjiga(subota);
        container.addKnjiga(windows);

        String sendXml = xstream.toXML(container);

        // get the socket's output stream and open a PrintWriter on it
        PrintWriter outToServer = new PrintWriter(clientSocket.getOutputStream(), true);

        // get the socket's input stream and open a BufferedReader on it
        BufferedReader inFromServer = new BufferedReader(new InputStreamReader(
                clientSocket.getInputStream()));

        // print a String and then terminate the line
        outToServer.println(sendXml);
        System.out.println("Client sends:\n" + sendXml);

        outToServer.println("end");
        System.out.println("Client sends:\n" + "end");

        while (true) {
            // read a line of text
            String rcvString = inFromServer.readLine();
            System.out.println("Client received: " + rcvString);
            if (rcvString.equals("end")) break;
            rcvXml += rcvString;
        }

        Container rcvContainer = (Container) xstream.fromXML(rcvXml);
        LinkedList<Knjiga> knjigaList = rcvContainer.getKnjige();

        for (Knjiga trenutnaKnjiga : knjigaList) {
            System.out.println(trenutnaKnjiga.getNaslov());
        }
        
        clientSocket.close();//CLOSE
    }

}
