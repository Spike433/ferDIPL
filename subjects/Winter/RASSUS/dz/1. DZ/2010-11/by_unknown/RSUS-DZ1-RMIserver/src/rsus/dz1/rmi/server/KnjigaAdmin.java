package rsus.dz1.rmi.server;

import java.rmi.Remote;
import java.rmi.RemoteException;

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
