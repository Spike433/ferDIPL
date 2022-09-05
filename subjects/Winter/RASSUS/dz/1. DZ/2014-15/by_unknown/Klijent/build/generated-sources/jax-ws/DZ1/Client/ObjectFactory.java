
package DZ1.Client;

import javax.xml.bind.JAXBElement;
import javax.xml.bind.annotation.XmlElementDecl;
import javax.xml.bind.annotation.XmlRegistry;
import javax.xml.namespace.QName;


/**
 * This object contains factory methods for each 
 * Java content interface and Java element interface 
 * generated in the DZ1.Client package. 
 * <p>An ObjectFactory allows you to programatically 
 * construct new instances of the Java representation 
 * for XML content. The Java representation of XML 
 * content can consist of schema derived interfaces 
 * and classes representing the binding of schema 
 * type definitions, element declarations and model 
 * groups.  Factory methods for each of these are 
 * provided in this class.
 * 
 */
@XmlRegistry
public class ObjectFactory {

    private final static QName _ListClients_QNAME = new QName("http://WebService.DZ1/", "listClients");
    private final static QName _ListClientsResponse_QNAME = new QName("http://WebService.DZ1/", "listClientsResponse");
    private final static QName _SearchUser_QNAME = new QName("http://WebService.DZ1/", "searchUser");
    private final static QName _Logout_QNAME = new QName("http://WebService.DZ1/", "logout");
    private final static QName _SearchUserResponse_QNAME = new QName("http://WebService.DZ1/", "searchUserResponse");
    private final static QName _LogoutResponse_QNAME = new QName("http://WebService.DZ1/", "logoutResponse");
    private final static QName _SearchFile_QNAME = new QName("http://WebService.DZ1/", "SearchFile");
    private final static QName _RegisterResponse_QNAME = new QName("http://WebService.DZ1/", "RegisterResponse");
    private final static QName _Register_QNAME = new QName("http://WebService.DZ1/", "Register");
    private final static QName _SearchFileResponse_QNAME = new QName("http://WebService.DZ1/", "SearchFileResponse");

    /**
     * Create a new ObjectFactory that can be used to create new instances of schema derived classes for package: DZ1.Client
     * 
     */
    public ObjectFactory() {
    }

    /**
     * Create an instance of {@link SearchUserResponse }
     * 
     */
    public SearchUserResponse createSearchUserResponse() {
        return new SearchUserResponse();
    }

    /**
     * Create an instance of {@link Logout }
     * 
     */
    public Logout createLogout() {
        return new Logout();
    }

    /**
     * Create an instance of {@link SearchUser }
     * 
     */
    public SearchUser createSearchUser() {
        return new SearchUser();
    }

    /**
     * Create an instance of {@link ListClientsResponse }
     * 
     */
    public ListClientsResponse createListClientsResponse() {
        return new ListClientsResponse();
    }

    /**
     * Create an instance of {@link ListClients }
     * 
     */
    public ListClients createListClients() {
        return new ListClients();
    }

    /**
     * Create an instance of {@link SearchFileResponse }
     * 
     */
    public SearchFileResponse createSearchFileResponse() {
        return new SearchFileResponse();
    }

    /**
     * Create an instance of {@link Register }
     * 
     */
    public Register createRegister() {
        return new Register();
    }

    /**
     * Create an instance of {@link RegisterResponse }
     * 
     */
    public RegisterResponse createRegisterResponse() {
        return new RegisterResponse();
    }

    /**
     * Create an instance of {@link SearchFile }
     * 
     */
    public SearchFile createSearchFile() {
        return new SearchFile();
    }

    /**
     * Create an instance of {@link LogoutResponse }
     * 
     */
    public LogoutResponse createLogoutResponse() {
        return new LogoutResponse();
    }

    /**
     * Create an instance of {@link UserAddress }
     * 
     */
    public UserAddress createUserAddress() {
        return new UserAddress();
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link ListClients }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://WebService.DZ1/", name = "listClients")
    public JAXBElement<ListClients> createListClients(ListClients value) {
        return new JAXBElement<ListClients>(_ListClients_QNAME, ListClients.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link ListClientsResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://WebService.DZ1/", name = "listClientsResponse")
    public JAXBElement<ListClientsResponse> createListClientsResponse(ListClientsResponse value) {
        return new JAXBElement<ListClientsResponse>(_ListClientsResponse_QNAME, ListClientsResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link SearchUser }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://WebService.DZ1/", name = "searchUser")
    public JAXBElement<SearchUser> createSearchUser(SearchUser value) {
        return new JAXBElement<SearchUser>(_SearchUser_QNAME, SearchUser.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Logout }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://WebService.DZ1/", name = "logout")
    public JAXBElement<Logout> createLogout(Logout value) {
        return new JAXBElement<Logout>(_Logout_QNAME, Logout.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link SearchUserResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://WebService.DZ1/", name = "searchUserResponse")
    public JAXBElement<SearchUserResponse> createSearchUserResponse(SearchUserResponse value) {
        return new JAXBElement<SearchUserResponse>(_SearchUserResponse_QNAME, SearchUserResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link LogoutResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://WebService.DZ1/", name = "logoutResponse")
    public JAXBElement<LogoutResponse> createLogoutResponse(LogoutResponse value) {
        return new JAXBElement<LogoutResponse>(_LogoutResponse_QNAME, LogoutResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link SearchFile }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://WebService.DZ1/", name = "SearchFile")
    public JAXBElement<SearchFile> createSearchFile(SearchFile value) {
        return new JAXBElement<SearchFile>(_SearchFile_QNAME, SearchFile.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link RegisterResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://WebService.DZ1/", name = "RegisterResponse")
    public JAXBElement<RegisterResponse> createRegisterResponse(RegisterResponse value) {
        return new JAXBElement<RegisterResponse>(_RegisterResponse_QNAME, RegisterResponse.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Register }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://WebService.DZ1/", name = "Register")
    public JAXBElement<Register> createRegister(Register value) {
        return new JAXBElement<Register>(_Register_QNAME, Register.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link SearchFileResponse }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://WebService.DZ1/", name = "SearchFileResponse")
    public JAXBElement<SearchFileResponse> createSearchFileResponse(SearchFileResponse value) {
        return new JAXBElement<SearchFileResponse>(_SearchFileResponse_QNAME, SearchFileResponse.class, null, value);
    }

}
