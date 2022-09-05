/*
 * This code has been developed at Departement of Telecommunications,
 * Faculty of Electrical Eengineering and Computing, University of Zagreb.
 */
package hr.fer.tel.rassus.tcp.client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class Client {

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) throws IOException {

        String serverName = new String("localhost"); // server name
        int port = 10002; // server port

        // create a stream socket and connect it to the specified port number
        // on the named host
        Socket clientSocket = new Socket(serverName, port);//SOCKET->CONNECT

        String sendString = new String("Any string...");

        // get the socket's output stream and open a PrintWriter on it
        PrintWriter outToServer = new PrintWriter(clientSocket.getOutputStream(), true);

        // get the socket's input stream and open a BufferedReader on it
        BufferedReader inFromServer = new BufferedReader(new InputStreamReader(
                clientSocket.getInputStream()));

        // print a String and then terminate the line
        outToServer.println(sendString);
        System.out.println("Client sends: " + sendString);

        // read a line of text
        String rcvString = inFromServer.readLine();
        System.out.println("Client received: " + rcvString);

        clientSocket.close();//CLOSE
    }
}
