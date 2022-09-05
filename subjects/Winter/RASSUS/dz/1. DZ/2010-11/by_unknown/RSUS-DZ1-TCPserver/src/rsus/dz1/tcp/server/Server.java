package rsus.dz1.tcp.server;

import com.thoughtworks.xstream.*;
import com.thoughtworks.xstream.io.xml.DomDriver;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import rsus.dz1.tcp.client.*;

/**
 *
 * @author Kristijan Bambir <kristijan.bambir@fer.hr>
 */
public class Server {

    public static void main(String[] args) throws IOException {
        int port = 50002; // server port
        int number = 1;

        // create a server socket and bind it to the specified port on the local
        // host
        ServerSocket serverSocket = new ServerSocket(port);//SOCKET->BIND->LISTEN

        XStream xstream = new XStream(new DomDriver());
        xstream.alias("autor", Autor.class);
        xstream.alias("knjiga", Knjiga.class);

        while (true) {
            // create a new socket, accept and listen for a connection to be
            // made to this socket
            Socket socket = serverSocket.accept();//ACCEPT

            // create a new PrintWriter from an existing OutputStream
            PrintWriter outToClient = new PrintWriter(socket.getOutputStream(),
                    true);

            // create a buffering character-input stream that uses a
            // default-sized input buffer
            BufferedReader inFromClient = new BufferedReader(
                    new InputStreamReader(socket.getInputStream()));

            String rcvXml = "";

            // read few lines of text
            while (true) {
                String rcvString = inFromClient.readLine();
                System.out.println("Server received: " + rcvString);
                if (rcvString.equals("end")) break;
                //shutdown if requested
                if (rcvString.contains("shutdown")) {
                    return;
                }
                rcvXml += rcvString + "\n";
            }

            Container rcvContainer = (Container) xstream.fromXML(rcvXml);
            for (Knjiga knjiga : rcvContainer.getKnjige()) {
                knjiga.setNaslov(knjiga.getNaslov().toUpperCase());
                knjiga.setIzdavac(knjiga.getIzdavac().toUpperCase());
            }

            String sendXml = xstream.toXML(rcvContainer);
            outToClient.println(sendXml);
            System.out.println("Server sends:\n" + sendXml);

            outToClient.println("end");
            System.out.println("Server sends: " + "end");

            BufferedWriter out = new BufferedWriter(new FileWriter(
                    "src/rsus/dz1/tcp/server/file" + number + ".xml"));
            out.write(rcvXml);
            out.close();

            number++;

            // close the streams and releases any system resources associated
            // with it
            outToClient.close();
            inFromClient.close();

            // close the socket
            socket.close();//CLOSE
        }
    }

}
