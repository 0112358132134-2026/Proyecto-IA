package naive;
import com.google.gson.Gson;
import com.google.gson.JsonNull;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;
import java.net.URLConnection;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

public class functions{

    public static movie GET_MOVIE(){
        movie _movie = new movie();
        try {
            URL url = new URL("http://127.0.0.1:8000/operate");
            URLConnection connection = url.openConnection();
            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line;
            String string = "";
            while ((line = reader.readLine()) != null) {
                string += line;
            }
            Gson g = new Gson();
            _movie= g.fromJson(string,movie.class);
            reader.close();
        } catch (MalformedURLException me) {
            System.err.println("MalformedURLException: " + me);
        } catch (IOException ioe) {
            System.err.println("IOException:  " + ioe);
        }
        return _movie;
    }

    public static void post(String uri, String data) throws Exception {
        movie m = new movie();
        m.name = "hola";
        m.ratio = 1;
        Gson g = new Gson();
        String JSON = g.toJson(m);

        HttpClient cliente = HttpClient.newBuilder().build();
        HttpRequest solicitud = HttpRequest.newBuilder()
                .uri(URI.create(uri + "/" + "José"))
                .POST(HttpRequest.BodyPublishers.ofString(JSON))
                .build();

        HttpResponse<?> respuesta = cliente.send(solicitud, HttpResponse.BodyHandlers.discarding());
        System.out.println(respuesta.statusCode());
        System.out.println(respuesta.toString());
    }
}