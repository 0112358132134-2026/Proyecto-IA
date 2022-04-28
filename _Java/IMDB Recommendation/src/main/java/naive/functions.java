package naive;
import com.google.gson.Gson;
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
public class functions{
    public String userExistGET(String user){
        movie _movie = new movie();
        String str = "";
        try {
            URL url = new URL("http://127.0.0.1:8000/prueba/" + user);
            URLConnection connection = url.openConnection();
            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                str += line;
            }
            Gson g = new Gson();
            _movie= g.fromJson(str,movie.class);
            reader.close();
        } catch (MalformedURLException me) {
            System.err.println("MalformedURLException: " + me);
        } catch (IOException ioe) {
            System.err.println("IOException:  " + ioe);
        }
        return str;
    }
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
        String JSON = "{'user':'jdeloen','password':'jdeloen'}";

        HttpClient cliente = HttpClient.newBuilder().build();
        HttpRequest solicitud = HttpRequest.newBuilder()
                .uri(URI.create(uri))
                .POST(HttpRequest.BodyPublishers.ofString(JSON))
                .build();

        HttpResponse<?> respuesta = cliente.send(solicitud, HttpResponse.BodyHandlers.discarding());
        System.out.println(respuesta.statusCode());
        System.out.println(respuesta.toString());
    }

    public int userStatus(String user, String password) throws IOException, InterruptedException {

        String JSON = "{\n" +
                "  \"user\": " + "\"" + user + "\"" + ",\n" +
                "  \"password\": " + "\"" + password + "\"" +  "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/userStatus"))
                .POST(HttpRequest.BodyPublishers.ofString(JSON))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());

        switch (response.body().toString()){
            case "1":
                return 1; //Only exists
            case "2":
                return 2; //Not exist and not is the first user
            case "3":
                return 3; //Not exist and is the first user
            case "4":
                return 4; //Exist and password is wrong
            case "5":
                return 5; //Exist and password is OK
            default:
                return 0; //Other
        }
    }

    public String simplexWithPath(String user, String path) throws IOException, InterruptedException{

        String JSON = "{\n" +
                "  \"user\": " + "\"" + user + "\"" + ",\n" +
                "  \"password\": " + "\"" + path + "\"" +  "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/firstUser"))
                .POST(HttpRequest.BodyPublishers.ofString(JSON))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());

        Gson g = new Gson();
        movie mov = new movie();
        mov = g.fromJson(response.body(),movie.class);

        return response.body();
    }
}