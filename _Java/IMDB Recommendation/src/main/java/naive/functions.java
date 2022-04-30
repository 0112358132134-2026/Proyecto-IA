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
import java.util.List;
import java.util.Scanner;
public class functions{

    // CSV functions
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
                "  \"file\": " + "\"" + file.replace('\\','/') + "\"" + "\n" +
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
                "  \"file\": " + "\"" + file.replace('\\','/') + "\"" + "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/reloadCSV"))
                .POST(HttpRequest.BodyPublishers.ofString(JSON))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());

        if (response.body().equals("1")){ return true; } return false;
    }

    // Search functions
    public void search() throws IOException, InterruptedException {

        Scanner scanner = new Scanner(System.in);
        boolean stopSearch = false;
        while(!stopSearch){
            System.out.print("Enter a text to search for related movies:");
            String toSearch = scanner.next();
            Movies results = movieSearch(toSearch);
            if(results.searchedMovies.size() > 0){
                System.out.println("These are your results:");
                for(int i = 0; i < results.searchedMovies.size(); i++){
                    System.out.println((i + 1) + " " + results.searchedMovies.get(i));
                }
            }
            else{System.out.println("No results found");}

            String option = "";
            boolean optionOK = false;
            while(!optionOK){
                System.out.println("Do you want to keep search? (Yes/No)");
                option = scanner.next().toLowerCase();
                if(option.equals("yes") || option.equals("no") || option.equals("y") || option.equals("n")){
                    optionOK = true;
                }
            }
            if(option.equals("no") || option.equals("n")){ stopSearch = true; }
        }
    }
    public Movies movieSearch(String name) throws IOException, InterruptedException {

        String JSON = "{\n" +
                "  \"name\": " + "\"" + name + "\"" + "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/movieSearch"))
                .POST(HttpRequest.BodyPublishers.ofString(JSON))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());

        Gson g = new Gson();
        Movies movies = g.fromJson(response.body(), Movies.class);
        return movies;
    }

    // Display functions
    public Movies showAllMovies() throws IOException, InterruptedException{

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/showAllMovies"))
                .POST(HttpRequest.BodyPublishers.noBody())
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());
        Gson g = new Gson();
        Movies movies = g.fromJson(response.body(), Movies.class);
        return movies;
    }
    public void printAllMovie(Movies movies){

        if(movies != null){
            List<List<String>> listMovies = movies.allMovies;
            for(int i = 0; i < listMovies.size(); i++){
                System.out.print((i + 1) + ". ");
                for(int j = 0; j < listMovies.get(i).size(); j++){
                    String value = listMovies.get(i).get(j);
                    if(j == 0){
                        System.out.print(String.format("%1$-52s",value));
                    }
                    else if(j == 1){
                        System.out.print(String.format("%1$-35s",value));
                    }
                    else if(j == 2){
                        System.out.print(String.format("%1$-62s",value));
                    }
                    else if(j == 3){
                        System.out.print(String.format("%1$-5s",value));
                    }
                }
                System.out.println();
            }
        }
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

    public void rentAMovie() throws IOException, InterruptedException {
        Scanner scanner = new Scanner(System.in);
        boolean stopSearch = false;
        while(!stopSearch){
            System.out.print("Enter a text to search for related movies:");
            String toSearch = scanner.next();
            Movies results = movieSearch(toSearch);
            if(results.searchedMovies.size() > 0){
                System.out.println("These are your results:");
                for(int i = 0; i < results.searchedMovies.size(); i++){
                    System.out.println((i + 1) + " " + results.searchedMovies.get(i));
                }
                boolean indexExist = false;
                int intIndex = -1;
                while(!indexExist){
                    System.out.println("Enter the number of the movie you want to rent:");
                    String index = scanner.next();
                    try{
                        intIndex = Integer.parseInt(index);
                        if(intIndex > 0 && intIndex <= results.searchedMovies.size()){
                            indexExist = true;
                        }
                    }
                    catch (Exception e){
                    }
                }
                String confirmation = "";
                boolean confirmOK = false;
                while(!confirmOK){
                    System.out.println("Do you want to rent this movie?: " + results.searchedMovies.get(intIndex - 1) + " (Yes/No)");
                    confirmation = scanner.next().toLowerCase();
                    if(confirmation.equals("yes") || confirmation.equals("no") || confirmation.equals("y") || confirmation.equals("n")){
                        confirmOK = true;
                    }
                }
                if(confirmation.equals("yes") || confirmation.equals("y")){
                    String calfication = "";
                    boolean calficationOk = false;
                    while(!calficationOk){
                        System.out.println("You liked the movie?: " + results.searchedMovies.get(intIndex - 1) + " (Yes/No)");
                        calfication = scanner.next().toLowerCase();
                        if(calfication.equals("yes") || calfication.equals("no") || calfication.equals("y") || calfication.equals("n")){
                            calficationOk = true;
                        }
                    }
                    // Save "Like" or "Dislike"
                    System.out.println("SIUUUU");
                }
            }
            else{System.out.println("No results found");}

            String option = "";
            boolean optionOK = false;
            while(!optionOK){
                System.out.println("Do you want to keep looking to rent another movie? (Yes/No)");
                option = scanner.next().toLowerCase();
                if(option.equals("yes") || option.equals("no") || option.equals("y") || option.equals("n")){
                    optionOK = true;
                }
            }
            if(option.equals("no") || option.equals("n")){ stopSearch = true; }
        }
    }

    public void clearScreen(){
        for(int i = 0; i <= 1000; i++){
            System.out.println("");
        }
    }

    // Unusable functions
    public static Movies GET_MOVIE(){
        Movies _movie = new Movies();
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
            _movie= g.fromJson(string, Movies.class);
            reader.close();
        } catch (MalformedURLException me) {
            System.err.println("MalformedURLException: " + me);
        } catch (IOException ioe) {
            System.err.println("IOException:  " + ioe);
        }
        return _movie;
    }
}