package naive;
import com.google.gson.Gson;

import javax.swing.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.*;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class App {

    private static HttpURLConnection connection;
    public static void main( String[] args ) {

        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                JFrame burden = new CSV_screen();
                burden.setSize(300,300);
                burden.setVisible(true);
            }
        });
    }
}