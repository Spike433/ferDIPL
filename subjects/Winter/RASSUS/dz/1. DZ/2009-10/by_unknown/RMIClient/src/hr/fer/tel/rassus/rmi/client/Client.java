/*
 * Ovaj kod razvijen je na Zavodu za Telekomunikacije za domacu zadacu
 * "Distribuirano programiranje" iz predmeta "Raspodijeljeni sustavi".
 */
package hr.fer.tel.rassus.rmi.client;

import hr.fer.tel.rassus.rmi.server.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.rmi.Naming;
import java.rmi.RMISecurityManager;

/**
 * Connects to a remote UserAdmin object, calls its methods, and prints the
 * return values.
 *
 */
public class Client {

    public static final String APP_NAME = "UserAdmin";
    public static final String EXIT_COMMAND = "exit";

    public static void main(String[] args) {
        if (System.getSecurityManager() == null) {
            System.setSecurityManager(new RMISecurityManager());
        }

        try {
            final UserAdmin remoteObject =
                    (UserAdmin) Naming.lookup(UserAdmin.RMI_NAME);

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
                    if ("adduser".equals(tokens[0])) {
                        final boolean success = remoteObject.addUser(tokens[1], tokens[2]);
                        if (success) {
                            System.err.println("New user added. Username: " + tokens[1] +
                                    ", password: " + tokens[2]);
                        } else {
                            System.err.println("User already exists.");
                        }
                    } else if ("getpass".equals(tokens[0])) {
                        final String passwd = remoteObject.getPassword(tokens[1]);
                        if (passwd != null) {
                            System.err.println(
                                    "User " + tokens[1] + " has password " + passwd);
                        } else {
                            System.err.println("User " + tokens[1] + " does not exist");
                        }
                    } else {
                        System.err.println("Invalid command. Commands: getpass, adduser");
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
