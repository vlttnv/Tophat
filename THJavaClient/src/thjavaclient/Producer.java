/*
 * 
 */
package thjavaclient;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Valentin Tunev
 */
public class Producer {
    private String balancerAddress;
    private int balancerPort;
    private int balancerID;
    
    
    public Producer(String balancerAddress, int balancerPort, int balancerID) {
        this.balancerAddress = balancerAddress;
        this.balancerPort = balancerPort;
        this.balancerID = balancerID;
    }
    
    /**
     * Register with the balancer using a GET request
     * @param host The balancer address
     * @param port The port the balancer is listening on
     * @param id The ID of this producer
     * @throws Exception 
     */
    public void register() throws Exception {

        String url = "http://" + balancerAddress + ":" + Integer.toString(balancerPort) + "/register/" + Integer.toString(balancerID);

        URL obj = new URL(url);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();

        con.setRequestMethod("GET");

        int responseCode = con.getResponseCode();
        System.out.println("Registering using: " + url);
        System.out.println("Worker: " + responseCode);

        StringBuffer response;
        try (BufferedReader in = new BufferedReader(
                new InputStreamReader(con.getInputStream()))) {
            String inputLine;
            response = new StringBuffer();
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
        }

        //print result
        System.out.println(response.toString());

    }

}
