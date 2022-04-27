package naive;
import com.google.firebase.database.DatabaseReference;

import java.io.IOException;
import java.net.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
public class App {

    private static HttpURLConnection connection;
    public static void main( String[] args ) throws IOException {

        //IMDB_DB firebase = new IMDB_DB();
        //DatabaseReference users_DB = firebase.connect();

        //users_DB.child("vane").setValueAsync(34);
        //users_DB.child("osos").setValueAsync(23);

        //Scanner scanner = new Scanner(System.in);

        Thread t=new Thread(new ShowDbChanges());
        t.run();
        try {
            Thread.sleep(100000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}