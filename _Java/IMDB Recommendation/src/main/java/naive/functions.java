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

    public boolean csvExist() throws IOException, InterruptedException {

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/csvExist"))
                .POST(HttpRequest.BodyPublishers.noBody())
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());
        if (response.body().equals("1")){ return true; } return false;
    }

    public boolean load_CSV(String file) throws IOException, InterruptedException {

        String JSON = "{\n" +
                "  \"file\": " + "\"" + file + "\"" + "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/loadCSV"))
                .POST(HttpRequest.BodyPublishers.ofString(JSON))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());
        if (response.body().equals("1")){ return true; } return false;
    }

    public boolean reload_CSV(String file) throws IOException, InterruptedException{

        String JSON = "{\n" +
                "  \"file\": " + "\"" + file + "\"" + "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/reloadCSV"))
                .POST(HttpRequest.BodyPublishers.ofString(JSON))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());

        if (response.body().equals("1")){ return true; } return false;
    }
    public int userStatus(String user, String password, int option) throws IOException, InterruptedException {

        String JSON = "{\n" +
                "  \"user\": " + "\"" + user + "\"" + ",\n" +
                "  \"option\": " + option + ",\n" +
                "  \"password\": " + "\"" + password + "\"" +  "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/userStatus"))
                .POST(HttpRequest.BodyPublishers.ofString(JSON))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());

        switch (response.body()){
            case "1":
                return 1; //Only exists
            case "2":
                return 2; //Not exist
            case "3":
                return 3; //Exist and password is wrong
            case "4":
                return 4; //Exist and password is OK
            default:
                return 0; //Other
        }
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
    public String simplexAlgorithm(String user, String path) throws IOException, InterruptedException{

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