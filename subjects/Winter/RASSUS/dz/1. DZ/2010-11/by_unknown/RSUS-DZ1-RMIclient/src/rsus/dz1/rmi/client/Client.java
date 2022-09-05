package rsus.dz1.rmi.client;

import rsus.dz1.rmi.server.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.rmi.Naming;
import java.rmi.RMISecurityManager;

/**
 *
 * @author Kristijan Bambir <kristijan.bambir@fer.hr>
 */
public class Client {

    public static final String APP_NAME = "KnjigaAdmin";
    public static final String EXIT_COMMAND = "exit";

    public static void main(String[] args) {
        if (System.getSecurityManager() == null) {
            System.setSecurityManager(new RMISecurityManager());
        }

        try {
            final KnjigaAdmin remoteObject =
                    (KnjigaAdmin) Naming.lookup(KnjigaAdmin.RMI_NAME);

            final BufferedReader stdIn =
                    new BufferedReader(new InputStreamReader(System.in));

            System.err.println("Welcome to the " + APP_NAME + "! Type \"" +
                    EXIT_COMMAND + "\" to end the session.");

            while (true) {
                System.err.print(APP_NAME + "$ ");
                System.err.flush();

                final String cmd = stdIn.readLine();
                if (cmd.equals(EXIT_COMMAND)) {
                    System.err.println("End of session.");
                    break;
                }

                // a separate try-block for client input processing. If the processing
                // of a command fails, the client will not exit.
                try {
                    // split the command line into tokens delimited by spaces
                    final String[] tokens = cmd.split("\\ ");
                    if ("getknjiga".equals(tokens[0])) {
                        final String knjiga = remoteObject.getKnjiga(tokens[1]);
                        if (knjiga != null) {
                            System.err.println(knjiga);
                        } else {
                            System.err.println("Nema knjige s tim naslovom!");
                        }
                    } else if ("getnasloviknjiga".equals(tokens[0])) {
                        final String knjige = remoteObject.getNasloviKnjiga();
                        if (knjige != null) {
                            System.err.println(knjige);
                        } else {
                            System.err.println("Nema knjiga!");
                        }
                    } else {
                        System.err.println("Invalid command. Commands: getknjiga, getnasloviknjiga");
                    }
                } catch (Exception e) {
                    System.err.println("Error processing input: " + cmd);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
