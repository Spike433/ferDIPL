package hr.fer.zkist.ppks.readings.tcp.server;

import hr.fer.zkist.ppks.readings.tcp.Messages;
import hr.fer.zkist.ppks.readings.Reading;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class TCPServer {

    private int port;

    public TCPServer(int port) {
        this.port = port;
    }

    public void start() {
        try ( ServerSocket serverSocket = new ServerSocket(port)) { //SOCKET -> BIND -> LISTEN
            while (true) {
                try {
                    Socket clientSocket = serverSocket.accept(); //ACCEPT -> SOCKET
                    new Thread(new ServerTask(clientSocket)).start();
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        } //CLOSE
    }

    public static void main(String[] args) {
        TCPServer server = new TCPServer(12345);
        server.start();
    }

    private class ServerTask implements Runnable {

        private final Socket clientSocket;

        public ServerTask(Socket clientSocket) {
            this.clientSocket = clientSocket;
        }

        @Override
        public void run() {
            try ( BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream(), "UTF-8")); //
                      BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream(), "UTF-8"))) {

//                //receive the greeting
//                String greeting = reader.readLine(); //READ
//                System.out.println("Received: " + greeting);
//
//                if (greeting.equals(Messages.GREETING)) {
//                    //send the greeting
//                    writer.write(greeting); writer.newLine(); // WRITE
//                    writer.flush();
//                    System.out.println("Sent: " + greeting);
//
                //start consuming readings
                String jsonReading;
                while ((jsonReading = reader.readLine()) != null) { //READ
                    //receive a reading
                    Reading reading = Reading.fromJson(jsonReading);
                    System.out.println("Received: " + reading);

                    //send a confirmation
                    String confirmation = Messages.CONFIRM;
                    writer.write(confirmation);
                    writer.newLine(); //WRITE
                    writer.flush();
                    System.out.println("Sent: " + confirmation);
                }
//              }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
}
