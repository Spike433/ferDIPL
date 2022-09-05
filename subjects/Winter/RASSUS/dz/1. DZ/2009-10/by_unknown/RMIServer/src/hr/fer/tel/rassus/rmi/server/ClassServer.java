/*
 * Ovaj kod razvijen je na Zavodu za Telekomunikacije za domacu zadacu
 * "Distribuirano programiranje" iz predmeta "Raspodijeljeni sustavi".
 */
package hr.fer.tel.rassus.rmi.server;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.URL;
import java.net.URLConnection;

/**
 * <p>
 * Provides the basic functionality of a mini-webserver, specialized to serve
 * HTTP GET requests for class files. Retrieves class files from the default 
 * class loader.
 * </p><p>
 * The class server creates a thread that listens on a socket and accepts
 * HTTP GET requests. The HTTP response contains the bytecode of the class
 * that requested in the GET header.
 * </p><p>
 * For loading remote classes, an RMI application can use this server 
 * in place of an HTTP server.
 * </p>
 * @author Sun Microsystems, inc.
 */
public class ClassServer
        implements Runnable {

    private final ServerSocket server;

    /**
     * @param port The port on which this server is listening.
     * @exception IOException if ServerSocket throws one
     */
    public ClassServer(int port)
            throws IOException {
        this.server = new ServerSocket(port);
        newListener();
        System.err.println("Class server started on port " + port);
    }

    /**
     * The listener thread that accepts a connection to the server, parses the
     * header to obtain the class file name and sends back the bytecode of the
     * class (or an error response if the class is not found or the request header
     * is malformed).
     */
    public void run() {
        final Socket socket;

        // accept a connection
        try {
            socket = server.accept();
        } catch (IOException e) {
            System.err.println("Class server died: " + e.getMessage());
            e.printStackTrace();
            return;
        }

        // create a new thread that will listen for the next request
        newListener();

        try {
            final DataOutputStream out =
                    new DataOutputStream(socket.getOutputStream());
            try {
                // get path to class file from header
                final DataInputStream in =
                        new DataInputStream(socket.getInputStream());
                final String path = getPath(in);
                // retrieve bytecodes from a class file
                byte[] bytecodes = getBytes(path);
                // send bytecodes in response (assumes HTTP/1.0 or later)
                try {
                    out.writeBytes("HTTP/1.0 200 OK\r\n");
                    out.writeBytes("Content-Length: " + bytecodes.length + "\r\n");
                    out.writeBytes("Content-Type: application/java\r\n\r\n");
                    out.write(bytecodes);
                    out.flush();
                } catch (IOException ie) {
                    System.err.println("Request processed, but error responding");
                    ie.printStackTrace();
                    return;
                }
            } catch (Exception e) {
                System.err.println("Request processing failed: ");
                e.printStackTrace();
                // send error response
                out.writeBytes("HTTP/1.0 400 " + e.getMessage() + "\r\n");
                out.writeBytes("Content-Type: text/html\r\n\r\n");
                out.flush();
            }
        } catch (IOException ex) {
            System.err.println("Class server error writing response: " + ex.getMessage());
            ex.printStackTrace();
        } finally {
            try {
                socket.close();
            } catch (IOException e) {
                // no handling necessary. The socket will either close or not,
                // there is nothing to do about it.
            }
        }
    }

    /**
     * Reads the input stream containing the request from the client for a dynamic
     * class load. Extracts the first header line and from it the pathname of the
     * requested class.
     *
     * @param is the input stream from the remote client.
     * @return The full pathname of the requested class.
     */
    private String getPath(InputStream is)
            throws IOException {
        final BufferedReader in = new BufferedReader(new InputStreamReader(is));

        // extract class name from the GET line
        String line = in.readLine();
        final String path;
        final int lastSpace = line.lastIndexOf(' ');
        if (lastSpace > 4 && line.startsWith("GET /")) {
            path = line.substring(4, lastSpace).trim();
        } else {
            throw new IOException("Malformed request header: " + line);
        }

        System.err.println("Class server received request for class: " + path);
        return path;
    }

    /**
     * Reads the class file containing the bytecode of the class
     * represented by the argument <b>path</b>. The <b>path</b> is an absolute
     * path (starting with a slash) that will be resolved relative to the
     * classpath.
     *
     * @param path pathname of the class file requested.
     * @return the bytecode of the class
     * @exception IOException Thrown for general I/O errors.
     * @exception ClassNotFoundException
     *              if the class corresponding to <b>path</b> could not be
     *              loaded.
     */
    private byte[] getBytes(String path)
            throws IOException, ClassNotFoundException {
        final URL url = this.getClass().getResource(path);
        if (url == null) {
            throw new ClassNotFoundException(
                    "Resource not found in classpath: " + path);
        }

        final URLConnection conn = url.openConnection();
        final DataInputStream in = new DataInputStream(conn.getInputStream());
        final byte[] classFile = new byte[conn.getContentLength()];
        in.readFully(classFile);
        System.err.println("Class server successfully read: " + path);
        return classFile;
    }

    /**
     * Creates a new thread for the request listener.
     */
    private void newListener() {
        (new Thread(this)).start();
    }
}
