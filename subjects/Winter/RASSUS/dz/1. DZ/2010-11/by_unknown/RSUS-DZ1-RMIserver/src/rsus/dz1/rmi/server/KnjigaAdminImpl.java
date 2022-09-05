package rsus.dz1.rmi.server;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.RMISecurityManager;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.LinkedList;
import com.thoughtworks.xstream.*;
import com.thoughtworks.xstream.io.xml.DomDriver;
import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;

/**
 *
 * @author Kristijan Bambir <kristijan.bambir@fer.hr>
 */
public class KnjigaAdminImpl
        extends UnicastRemoteObject
        implements KnjigaAdmin {

    /**
     * The TCP port the class server will be listening on.
     */
    private final Container container;
    private final String xmlFilePath = "src/rsus/dz1/rmi/server/File.xml";

    public KnjigaAdminImpl()
            throws RemoteException, FileNotFoundException, IOException {
        super();

        XStream xstream = new XStream(new DomDriver());
        xstream.alias("knjiga", Knjiga.class);
        xstream.alias("autor", Autor.class);

        byte[] buffer = new byte[(int) new File(xmlFilePath).length()];
        BufferedInputStream f = null;
        try {
            f = new BufferedInputStream(new FileInputStream(xmlFilePath));
            f.read(buffer);
        } finally {
            if (f != null) try { f.close(); } catch (IOException ignored) { }
        }

        container = (Container) xstream.fromXML(new String(buffer));
    }

    public String getKnjiga(String naslov)
            throws RemoteException {
        LinkedList<Knjiga> knjige = container.getKnjige();
        for (Knjiga knjiga : knjige) {
            if (knjiga.getNaslov().toLowerCase().equals(naslov.toLowerCase())) {
                return "Naslov: " + knjiga.getNaslov() + "; " +
                       "Godina izdanja: " + knjiga.getGodinaIzdanja() + "; " +
                       "Izdavač: " + knjiga.getIzdavac() + "; " +
                       "Autor: " + knjiga.getAutor().getPrezime() + ", " +
                       knjiga.getAutor().getIme();
            }
        }
        return null;
    }

    public String getNasloviKnjiga()
            throws RemoteException {
        String naslovi = "";
        for (Knjiga trenutnaKnjiga : container.getKnjige()) {
            naslovi += trenutnaKnjiga.getNaslov();
            if (container.getKnjige().indexOf(trenutnaKnjiga) !=
                    container.getKnjige().size()-1) {
                naslovi += ", ";
            }
        }
        return naslovi;
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

            // instantiate and register the remote object
            final KnjigaAdmin serverObject = new KnjigaAdminImpl();
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
