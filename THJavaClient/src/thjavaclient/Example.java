/*
 * 
 */

package thjavaclient;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Valentin Tunev
 */
public class Example {
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Producer pd = new Producer("SOME_REMOTE_ADDRESS", 5000, 1);
        try {
            pd.register();
        } catch (Exception ex) {
            Logger.getLogger(Producer.class.getName()).log(Level.SEVERE, null, ex);
        }
        
    }
    
}
