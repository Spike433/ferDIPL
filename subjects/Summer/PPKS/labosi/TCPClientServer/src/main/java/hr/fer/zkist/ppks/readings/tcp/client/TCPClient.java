package hr.fer.zkist.ppks.readings.tcp.client;

import hr.fer.zkist.ppks.readings.Reading;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class TCPClient {

    public static void main(String[] args) {
        try ( Socket clientSocket = new Socket("localhost", 12345); //SOCKET -> CONNECT
                  BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream(), "UTF-8")); //
                  BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream(), "UTF-8"))) {

//            //send the greeting
//            String greeting = Messages.GREETING;
//            writer.write(greeting); writer.newLine(); //WRITE
//            writer.flush();
//            System.out.println("Sent: " + greeting);
//
//            //receive the greeting
//            greeting = reader.readLine(); //READ
//            System.out.println("Received : " + greeting);
//
//            if (greeting.equals(Messages.GREETING)) {
            //start sending readings
            while (true) {
                //send a reading
                Reading reading = new Reading("id_5", "temperature", (Math.random() * 60) - 20, "C");
                writer.write(reading.toJson());
                writer.newLine(); //WRITE
                writer.flush();
                System.out.println("Sent: " + reading);

                //receive confirmation
                String confirmation = reader.readLine(); //READ
                System.out.println("Received: " + confirmation);

                try {
                    Thread.sleep(5000);
                } catch (InterruptedException ex) {
                    //do nothing
                }
            }
            //           }

        } catch (IOException ex) {
            Logger.getLogger(TCPClient.class.getName()).log(Level.SEVERE, null, ex);
        } //CLOSE
    }
}
