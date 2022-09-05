/*
 * Ovaj kod razvijen je na Zavodu za Telekomunikacije za domacu zadacu
 * "Distribuirano programiranje" iz predmeta "Raspodijeljeni sustavi".
 */
package hr.fer.tel.rassus.rmi.server;

import java.rmi.Remote;
import java.rmi.RemoteException;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public interface UserAdmin
        extends Remote {

    String RMI_NAME = "//localhost/Registry";

    String getPassword(String user) throws RemoteException;

    boolean addUser(String user, String password) throws RemoteException;
}
