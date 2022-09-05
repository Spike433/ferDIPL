package rsus.dz1.rmi.server;

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.LinkedList;

/**
 *
 * @author Kristijan Bambir <kristijan.bambir@fer.hr>
 */
public interface KnjigaAdmin
        extends Remote {

    String RMI_NAME = "//localhost/Registry";

    String getKnjiga(String naslov) throws RemoteException;
    String getNasloviKnjiga() throws RemoteException;

}
