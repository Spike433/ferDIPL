
package DZ1.Client;

import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.jws.WebResult;
import javax.jws.WebService;
import javax.xml.bind.annotation.XmlSeeAlso;
import javax.xml.ws.Action;
import javax.xml.ws.RequestWrapper;
import javax.xml.ws.ResponseWrapper;


/**
 * This class was generated by the JAX-WS RI.
 * JAX-WS RI 2.2.6-1b01 
 * Generated source version: 2.2
 * 
 */
@WebService(name = "Service", targetNamespace = "http://WebService.DZ1/")
@XmlSeeAlso({
    ObjectFactory.class
})
public interface Service {


    /**
     * 
     * @param port
     * @param username
     * @param address
     * @return
     *     returns boolean
     */
    @WebMethod
    @WebResult(targetNamespace = "")
    @RequestWrapper(localName = "logout", targetNamespace = "http://WebService.DZ1/", className = "DZ1.Client.Logout")
    @ResponseWrapper(localName = "logoutResponse", targetNamespace = "http://WebService.DZ1/", className = "DZ1.Client.LogoutResponse")
    @Action(input = "http://WebService.DZ1/Service/logoutRequest", output = "http://WebService.DZ1/Service/logoutResponse")
    public boolean logout(
        @WebParam(name = "username", targetNamespace = "")
        String username,
        @WebParam(name = "address", targetNamespace = "")
        String address,
        @WebParam(name = "port", targetNamespace = "")
        int port);

    /**
     * 
     * @param port
     * @param username
     * @param sharedFiles
     * @param address
     * @return
     *     returns java.lang.Boolean
     */
    @WebMethod(operationName = "Register")
    @WebResult(targetNamespace = "")
    @RequestWrapper(localName = "Register", targetNamespace = "http://WebService.DZ1/", className = "DZ1.Client.Register")
    @ResponseWrapper(localName = "RegisterResponse", targetNamespace = "http://WebService.DZ1/", className = "DZ1.Client.RegisterResponse")
    @Action(input = "http://WebService.DZ1/Service/RegisterRequest", output = "http://WebService.DZ1/Service/RegisterResponse")
    public Boolean register(
        @WebParam(name = "username", targetNamespace = "")
        String username,
        @WebParam(name = "sharedFiles", targetNamespace = "")
        String sharedFiles,
        @WebParam(name = "address", targetNamespace = "")
        String address,
        @WebParam(name = "port", targetNamespace = "")
        Integer port);

    /**
     * 
     * @param filename
     * @return
     *     returns java.lang.String
     */
    @WebMethod(operationName = "SearchFile")
    @WebResult(targetNamespace = "")
    @RequestWrapper(localName = "SearchFile", targetNamespace = "http://WebService.DZ1/", className = "DZ1.Client.SearchFile")
    @ResponseWrapper(localName = "SearchFileResponse", targetNamespace = "http://WebService.DZ1/", className = "DZ1.Client.SearchFileResponse")
    @Action(input = "http://WebService.DZ1/Service/SearchFileRequest", output = "http://WebService.DZ1/Service/SearchFileResponse")
    public String searchFile(
        @WebParam(name = "filename", targetNamespace = "")
        String filename);

    /**
     * 
     * @return
     *     returns java.lang.String
     */
    @WebMethod
    @WebResult(targetNamespace = "")
    @RequestWrapper(localName = "listClients", targetNamespace = "http://WebService.DZ1/", className = "DZ1.Client.ListClients")
    @ResponseWrapper(localName = "listClientsResponse", targetNamespace = "http://WebService.DZ1/", className = "DZ1.Client.ListClientsResponse")
    @Action(input = "http://WebService.DZ1/Service/listClientsRequest", output = "http://WebService.DZ1/Service/listClientsResponse")
    public String listClients();

    /**
     * 
     * @param username
     * @return
     *     returns DZ1.Client.UserAddress
     */
    @WebMethod
    @WebResult(targetNamespace = "")
    @RequestWrapper(localName = "searchUser", targetNamespace = "http://WebService.DZ1/", className = "DZ1.Client.SearchUser")
    @ResponseWrapper(localName = "searchUserResponse", targetNamespace = "http://WebService.DZ1/", className = "DZ1.Client.SearchUserResponse")
    @Action(input = "http://WebService.DZ1/Service/searchUserRequest", output = "http://WebService.DZ1/Service/searchUserResponse")
    public UserAddress searchUser(
        @WebParam(name = "username", targetNamespace = "")
        String username);

}
