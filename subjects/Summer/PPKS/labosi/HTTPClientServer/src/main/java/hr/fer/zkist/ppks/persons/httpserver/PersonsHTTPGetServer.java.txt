/*
 * Copyright 2022 Krešimir Pripužić
 */
package hr.fer.zkist.ppks.persons.httpserver;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import hr.fer.zkist.ppks.persons.Cordinates;
import hr.fer.zkist.ppks.persons.CordinatesService;

import java.io.*;
import java.net.InetSocketAddress;
import java.net.URI;
import java.nio.charset.StandardCharsets;

/**
 *
 * @author Krešimir Pripužić <kresimir.pripuzic@fer.hr>
 */
public class PersonsHTTPGetServer {

    private final CordinatesService cordinatesService;
    private final HttpServer httpServer;

    // todo hosted url http://localhost:8000/cords
    public PersonsHTTPGetServer(int port) throws IOException {
        cordinatesService = new CordinatesService();
        httpServer = HttpServer.create(new InetSocketAddress(port), 0);
        httpServer.createContext("/cords", new PersonsHTTPGetServer.PersonsHandler()); // todo change cords
    }


    public void start() {
        httpServer.start();
    }    

    public static void main(String[] args) throws IOException {
        PersonsHTTPGetServer server = new PersonsHTTPGetServer(8000);
        server.start();
    }
    
    class PersonsHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange httpExchange) throws IOException {

            // Add CORS headers
            Headers headers = httpExchange.getResponseHeaders();
            headers.add("Access-Control-Allow-Origin", "*"); // Allow requests from any origin todo add cors
            headers.add("Access-Control-Allow-Methods", "GET"); // Allow GET requests
            headers.add("Access-Control-Allow-Headers", "Content-Type");
            headers.add("Content-Type", "application/json; charset=" + StandardCharsets.UTF_8.name());

            if (httpExchange.getRequestMethod().equalsIgnoreCase("GET")) {
                // Process the GET request and return the coordinates

                switch (httpExchange.getRequestMethod()) {
                    case "GET":
                        handleGet(httpExchange);
                        break;
                    case "POST":
                        handlePost(httpExchange);
                        break;
                    case "PUT":
                        handlePut(httpExchange);
                        break;
                    case "DELETE":
                        handleDelete(httpExchange);
                        break;
                }

            } else {
                // Return 405 Method Not Allowed for other request methods
                httpExchange.sendResponseHeaders(405, -1);
            }
        }

        private void handleGet(HttpExchange httpExchange) throws IOException { //todo only keep handleGet
            URI uri = httpExchange.getRequestURI();
            byte[] responseBody = new byte[0]; //default body for malformed requests
            int responseCode = 404; //default status code for malformed requests

            if (uri.getPath().equals("/cords")) {
                //return all persons

                responseBody = Cordinates.listToJson(cordinatesService.get()).getBytes("UTF-8");
                responseCode = 200;
            } else if (uri.getPath().matches("/cords/[0-9]*")) { // todo not needed
                //return person with given id
                String[] split = uri.getPath().split("/");
                Cordinates cordinates = cordinatesService.get(Integer.parseInt(split[2]));
                if (cordinates != null) {
                    responseBody = cordinates.toJson().getBytes("UTF-8");
                    responseCode = 200;
                }
            }
            
            httpExchange.getResponseHeaders().set("content-type", "application/json");
            httpExchange.sendResponseHeaders(responseCode, responseBody.length);
            try (OutputStream os = httpExchange.getResponseBody()) { //write and close the response body
                os.write(responseBody);
            }           
        }

        private void handlePost(HttpExchange httpExchange) throws IOException {
            //return status code 501 - no implemented
            httpExchange.sendResponseHeaders(501, -1);            
        }

        private void handlePut(HttpExchange httpExchange) throws IOException {
            //return status code 501 - no implemented
            httpExchange.sendResponseHeaders(501, -1);
        }

        private void handleDelete(HttpExchange httpExchange) throws IOException {
            //return status code 501 - no implemented
            httpExchange.sendResponseHeaders(501, -1);
        }
    }
}
