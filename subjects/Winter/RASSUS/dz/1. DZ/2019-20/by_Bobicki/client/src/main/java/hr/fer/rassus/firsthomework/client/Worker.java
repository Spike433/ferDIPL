package hr.fer.rassus.firsthomework.client;

import java.io.*;
import java.net.Socket;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class Worker implements Runnable{
    private final Socket clientSocket;
    private final AtomicBoolean isRunning;
    private final AtomicInteger activeConnections;
    private long startTime;

    public Worker(Socket clientSocket, AtomicBoolean isRunning, AtomicInteger activeConnections, long startTime) {
        this.clientSocket = clientSocket;
        this.isRunning = isRunning;
        this.activeConnections = activeConnections;
        this.startTime = startTime;
    }

    @Override
    public void run() {
        try (// create a new BufferedReader from an existing InputStream
             BufferedReader inFromClient = new BufferedReader(new InputStreamReader(
                     clientSocket.getInputStream()));
             // create a PrintWriter from an existing OutputStream
             PrintWriter outToClient = new PrintWriter(new OutputStreamWriter(
                     clientSocket.getOutputStream()), true)) {

            String receivedString;

            // read a few lines of text
            while ((receivedString = inFromClient.readLine()) != null/*READ*/) {
                System.out.println("Server received: " + receivedString);
                TimeUnit.SECONDS.sleep(2);

                //shutdown the server if requested
                if (receivedString.contains("shutdown")) {
                    outToClient.println("Server has been shutdown!");//WRITE
                    System.out.println("Server sent: Server has been shutdown!");
                    isRunning.set(false);
                    activeConnections.getAndDecrement();
                    return;
                }

                long currentTime = System.nanoTime() / 1000000000;
                long duration = currentTime - startTime;
                int neighbourReadingsLine = (int)(duration % 100) + 2;

                String stringToSend = duration + "+" + neighbourReadingsLine;
                // send a String then terminate the line and flush
                outToClient.println(stringToSend);//WRITE
                System.out.println("Server sent: " + stringToSend + " (duration (in seconds) + line to read)");
                System.out.println();
            }
            activeConnections.getAndDecrement();
        }
        catch (IOException ex) {
            System.err.println("Exception caught when trying to read or send data: " + ex);
        }
        catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}