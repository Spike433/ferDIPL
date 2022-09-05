/*
 * This code has been developed at Departement of Telecommunications,
 * Faculty of Electrical Eengineering and Computing, University of Zagreb.
 */
package hr.fer.tel.rassus.tcp.server;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class Server {

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) throws IOException {

        int port = 10002; // server port
        String rcvStr = null; // received String
        String sendStr = null; // sent String

        // create a server socket and bind it to the specified port on the local
        // host
        ServerSocket serverSocket = new ServerSocket(port);//SOCKET->BIND->LISTEN

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

            // read few lines of text
            while ((rcvStr = inFromClient.readLine()) != null) {
                System.out.println("Server received: " + rcvStr);

                //shutdown if requested
                if (rcvStr.contains("shutdown")) {
                    return;
                }

                sendStr = rcvStr.toUpperCase();

                outToClient.println(sendStr);
                System.out.println("Server sends: " + sendStr);
            }

            // close the streams and releases any system resources associated
            // with it
            outToClient.close();
            inFromClient.close();

            // close the socket
            socket.close();//CLOSE
        }
    }
}
