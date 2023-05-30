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
public class SingleClientTCPServer { 

    private int port;

    public SingleClientTCPServer(int port) {
        this.port = port;
    }

    public void start() {
        try ( ServerSocket serverSocket = new ServerSocket(port); //SOCKET -> BIND -> LISTEN
                  Socket clientSocket = serverSocket.accept(); //ACCEPT -> SOCKET
                  BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream(), "UTF-8")); //
                  BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream(), "UTF-8"))) {

//            //receive the greeting
//            String greeting = reader.readLine();
//            System.out.println("Received: " + greeting);
//
//            if (greeting.equals(Messages.GREETING)) {
//                //send the greeting
//                writer.write(greeting);
//                writer.newLine();
//                writer.flush();
//                System.out.println("Sent: " + greeting);
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
//            }
        } catch (IOException ex) {
            ex.printStackTrace();
        } //CLOSE
    }

    public static void main(String[] args) {
        SingleClientTCPServer server = new SingleClientTCPServer(12345);
        server.start();
    }
}
