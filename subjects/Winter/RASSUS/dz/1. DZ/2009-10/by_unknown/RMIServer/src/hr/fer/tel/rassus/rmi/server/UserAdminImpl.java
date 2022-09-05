/*
 * This code has been developed at Departement of Telecommunications,
 * Faculty of Electrical Eengineering and Computing, University of Zagreb.
 */
package hr.fer.tel.rassus.rmi.server;

import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.RMISecurityManager;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.HashMap;
import java.util.Map;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class UserAdminImpl
        extends UnicastRemoteObject
        implements UserAdmin {

    /**
     * The TCP port the class server will be listening on.
     */
    public static final int CLASS_SERVER_PORT = 4727;
    private final Map users = new HashMap();

    public UserAdminImpl()
            throws RemoteException {
        super();
    }

    public boolean addUser(String username, String password)
            throws RemoteException {
        if (users.get(username) != null) {
            return false;
        }

        if (!username.matches("[A-Za-z0-9]*")) {
            throw new RemoteException("Ill-formed username: " + username);
        }

        users.put(username, password);
        return true;
    }

    public String getPassword(String username) {
        return (String) users.get(username);
    }

    /**
     * Publishes a Counter object by registering it with the RMI Registry and
     * starts the class file server.
     * The method ends after that, but the process is kept alive by the
     * additional threads that were created.
     *
     * @param args ignored---no command line arguments needed.
     */
    public static void main(String[] args) {
        try {
            if (System.getSecurityManager() == null) {
                System.setSecurityManager(new RMISecurityManager());
            }

            System.out.println(
                    "Codebase: " + System.getProperty("java.rmi.server.codebase"));

            // start the class file server
            new ClassServer(CLASS_SERVER_PORT);

            // instantiate and register the remote object
            final UserAdmin serverObject = new UserAdminImpl();
            System.out.println(serverObject);
            Naming.rebind(RMI_NAME, serverObject);
        } catch (MalformedURLException e) {
            System.err.println(
                    "RMI Registry service name binding failed due to: " + e);
            System.exit(1);
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
