package naive;
import com.google.gson.Gson;
import jdk.security.jarsigner.JarSigner;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.Scanner;
public class functions{

    // CSV functions
    private String Json;
    public boolean csvExist() throws IOException, InterruptedException {

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/csvExist"))
                .POST(HttpRequest.BodyPublishers.noBody())
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());
        return response.body().equals("1");
    }
    public boolean load_CSV(String file) throws IOException, InterruptedException {

        Json = "{\n" +
                "  \"file\": " + "\"" + file.replace('\\','/') + "\"" + "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/loadCSV"))
                .POST(HttpRequest.BodyPublishers.ofString(Json))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());
        return response.body().equals("1");
    }
    public boolean reload_CSV(String file) throws IOException, InterruptedException{

        Json = "{\n" +
                "  \"file\": " + "\"" + file.replace('\\','/') + "\"" + "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/reloadCSV"))
                .POST(HttpRequest.BodyPublishers.ofString(Json))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());

        return response.body().equals("1");
    }

    // Search functions
    public void search() throws IOException, InterruptedException {

        Scanner scanner = new Scanner(System.in);
        boolean stopSearch = false;
        while(!stopSearch){
            System.out.println("---------------------------------------------------------");
            System.out.println("                         SEARCH                          ");
            System.out.println("---------------------------------------------------------");
            System.out.println("Enter a text to search for related movies:");
            String toSearch = scanner.next();
            System.out.println("---------------------------------------------------------");
            Movies results = movieSearch(toSearch);
            int size = results.searchedMovies.size();
            if(toSearch.equals("")){
                size = 0;
            }
            if(size > 0){
                System.out.println("These are your results:");
                for(int i = 0; i < results.searchedMovies.size(); i++){
                    System.out.println((i + 1) + " " + results.searchedMovies.get(i));
                }
            }
            else{System.out.println("Sorry, no results found!");}
            System.out.println("---------------------------------------------------------");
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
            clearScreen();
        }
    }
    public Movies movieSearch(String name) throws IOException, InterruptedException {

        Json = "{\n" +
                "  \"name\": " + "\"" + name + "\"" + "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/movieSearch"))
                .POST(HttpRequest.BodyPublishers.ofString(Json))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());

        Gson g = new Gson();
        return g.fromJson(response.body(), Movies.class);
    }
    public Movies showAllMovies() throws IOException, InterruptedException{

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/showAllMovies"))
                .POST(HttpRequest.BodyPublishers.noBody())
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());
        Gson g = new Gson();
        return g.fromJson(response.body(), Movies.class);
    }
    public void printAllMovie(Movies movies){

        if(movies != null){
            List<List<String>> listMovies = movies.allMovies;
            for(int i = 0; i < listMovies.size(); i++){
                System.out.print((i + 1) + ". ");
                for(int j = 0; j < listMovies.get(i).size(); j++){
                    String value = listMovies.get(i).get(j);
                    if(j == 0){
                        System.out.printf("%1$-52s",value);
                    }
                    else if(j == 1){
                        System.out.printf("%1$-35s",value);
                    }
                    else if(j == 2){
                        System.out.printf("%1$-62s",value);
                    }
                    else if(j == 3){
                        System.out.printf("%1$-5s",value);
                    }
                }
                System.out.println();
            }
            System.out.print("      |");
            System.out.printf("%1$-51s|","MOVIE NAME");
            System.out.printf("%1$-34s|","DIRECTOR NAME");
            System.out.printf("%1$-60s|","GENRES");
            System.out.printf("%1$-4s|","IMDB SCORE");
            System.out.println();
        }
    }

    // Rent Movies - Functions
    public void rentAMovie(String user) throws IOException, InterruptedException {

        askMovies(user);
        clearScreen();
        Scanner scanner = new Scanner(System.in);
        boolean stopSearch = false;
        while(!stopSearch){
            System.out.println("-----------------------------------------------------");
            System.out.print("Enter a text to search for related movies:");
            String toSearch = scanner.next();
            System.out.println("-----------------------------------------------------");
            Movies results = movieSearch(toSearch);
            int length = results.searchedMovies.size();
            if(toSearch.length() == 0){
                length = 0;
            }

            if(length > 0){
                System.out.println("These are your results:");
                for(int i = 0; i < results.searchedMovies.size(); i++){
                    System.out.println((i + 1) + " " + results.searchedMovies.get(i));
                }
                boolean indexExist = false;
                int intIndex = -2;
                while(!indexExist){
                    System.out.println("----------------------------------------------------------------------------------------------");
                    System.out.print("Enter the number of the movie you want to rent or enter (-1) if you dont want to rent a movie:");
                    String index = scanner.next();
                    try{
                        intIndex = Integer.parseInt(index);
                        if(intIndex >= -1 && intIndex <= results.searchedMovies.size()){
                            indexExist = true;
                        }
                    }
                    catch (Exception e){
                        System.out.print("");
                    }
                }
                if(intIndex != -1){
                    clearScreen();
                    String confirmation = "";
                    boolean confirmOK = false;
                    while(!confirmOK){
                        System.out.println("Do you want to rent the movie: " + results.searchedMovies.get(intIndex - 1) + "? (Yes/No)");
                        confirmation = scanner.next().toLowerCase();
                        if(confirmation.equals("yes") || confirmation.equals("no") || confirmation.equals("y") || confirmation.equals("n")){
                            confirmOK = true;
                        }
                        clearScreen();
                    }
                    if(confirmation.equals("yes") || confirmation.equals("y")){
                        String qualification = "";
                        boolean qualificationOk = false;
                        while(!qualificationOk){
                            System.out.println("You liked the movie: " + results.searchedMovies.get(intIndex - 1) + "? (Yes/No)");
                            qualification = scanner.next().toLowerCase();
                            if(qualification.equals("yes") || qualification.equals("no") || qualification.equals("y") || qualification.equals("n")){
                                qualificationOk = true;
                            }
                            clearScreen();
                        }
                        int vote = 0;
                        if(qualification.equals("yes") || qualification.equals("y")){
                            vote = 1;
                        }
                        addRating(user, results.searchedMovies.get(intIndex - 1), vote);
                    }
                }
            }
            else{System.out.println("Sorry, no results found!");}

            String option = "";
            boolean optionOK = false;
            while(!optionOK){
                System.out.println("Do you want to keep looking to rent another movie? (Yes/No)");
                option = scanner.next().toLowerCase();
                if(option.equals("yes") || option.equals("no") || option.equals("y") || option.equals("n")){
                    optionOK = true;
                }
                clearScreen();
            }
            if(option.equals("no") || option.equals("n")){ stopSearch = true; }
        }
    }
    public void askMovies(String user) throws IOException, InterruptedException {

        Json = "{\n" +
                "  \"user\": " + "\"" + user + "\"" + "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/userHasLikes"))
                .POST(HttpRequest.BodyPublishers.ofString(Json))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());

        if(response.body().equals("0")) {

            Json = "{\n" +
                    "  \"user\": " + "\"" + user + "\"" + ",\n" +
                    "  \"exist\": " + 0 + "\n" +
                    "}";

            HttpClient _client = HttpClient.newHttpClient();
            HttpRequest _request = HttpRequest.newBuilder()
                    .uri(URI.create("http://127.0.0.1:8000/showRecommendations"))
                    .POST(HttpRequest.BodyPublishers.ofString(Json))
                    .build();

            HttpResponse<String> _response = _client.send(_request, HttpResponse.BodyHandlers.ofString());
            Gson g = new Gson();
            Movies movies = g.fromJson(_response.body(), Movies.class);
            List<List<String>> allMovies = movies.allMovies;
            int index = 1;
            for (List<String> movie : allMovies) {
                System.out.println("-----------------------------------------------------------------------------------------------------");
                System.out.printf("%1$-52s", "Name (" + index + "/" + allMovies.size() + ")");
                System.out.println();
                System.out.println("-----------------------------------------------------------------------------------------------------");
                int counter = 0;
                for (String s : movie) {
                    if (counter == 0){
                        System.out.print(s);
                    }
                    counter += 1;
                }

                System.out.println();
                // Questions
                String qualification = "";
                boolean qualificationOk = false;
                Scanner scanner = new Scanner(System.in);
                while (!qualificationOk) {
                    System.out.println("-----------------------------------------------------------------------------------------------------");
                    System.out.println("Did you like the movie: " + movie.get(0) + "? (Yes/No/NV {no vote})");
                    qualification = scanner.next().toLowerCase();
                    if (qualification.equals("yes") || qualification.equals("no") || qualification.equals("y") || qualification.equals("n") || qualification.equals("nv")) {
                        qualificationOk = true;
                    }
                }
                if (qualification.equals("yes") || qualification.equals("y")) {
                    addRating(user, movie.get(0), 1);
                } else if (qualification.equals("no") || qualification.equals("n")) {
                    addRating(user, movie.get(0), 0);
                }
                clearScreen();
                index += 1;
            }
        }
    }
    public void addRating(String user, String movie, int vote) throws IOException, InterruptedException {

        Json = "{\n" +
                "  \"user\": " + "\"" + user + "\"" + ",\n" +
                "  \"movie\": " + "\"" + movie + "\"" + ",\n" +
                "  \"vote\": " + vote + "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/addRating"))
                .POST(HttpRequest.BodyPublishers.ofString(Json))
                .build();

        client.send(request,HttpResponse.BodyHandlers.ofString());
    }

    // Login Functions
    public int userStatus(String user, String password, int option) throws IOException, InterruptedException {

        Json = "{\n" +
                "  \"user\": " + "\"" + user + "\"" + ",\n" +
                "  \"option\": " + option + ",\n" +
                "  \"password\": " + "\"" + password + "\"" +  "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/userStatus"))
                .POST(HttpRequest.BodyPublishers.ofString(Json))
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

    // Recommendation Function
    public void showRecommendations(String user) throws IOException, InterruptedException{

        Json = "{\n" +
                "  \"user\": " + "\"" + user + "\"" + "\n" +
                "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/userHasLikes"))
                .POST(HttpRequest.BodyPublishers.ofString(Json))
                .build();

        HttpResponse<String> response = client.send(request,HttpResponse.BodyHandlers.ofString());

        int exist = 1;
        if(response.body().equals("0")){
            exist = 0;
        }
        Json = "{\n" +
                "  \"user\": " + "\"" + user + "\"" + ",\n" +
                "  \"exist\": " + exist + "\n" +
                "}";

        HttpClient _client = HttpClient.newHttpClient();
        HttpRequest _request = HttpRequest.newBuilder()
                .uri(URI.create("http://127.0.0.1:8000/showRecommendations"))
                .POST(HttpRequest.BodyPublishers.ofString(Json))
                .build();

        HttpResponse<String> _response = _client.send(_request,HttpResponse.BodyHandlers.ofString());
        Gson g = new Gson();
        String ok = "";
        Movies movies = g.fromJson(_response.body(), Movies.class);
        List<List<String>> recommendations = movies.allMovies;
        System.out.println("Your recommendations are: ");
        int rowCounter = 1;
        for (List<String> recommendation : recommendations) {
            System.out.print(rowCounter + ". ");
            int counter = 0;
            for (String s : recommendation) {
                if(counter == 0){
                    System.out.printf("%1$-54s",s);
                }
                else if(counter == 1){
                    System.out.printf("%1$-35s",s);
                }
                else if(counter == 2){
                    System.out.printf("%1$-40s",s);
                }
                else if(counter == 3){
                    System.out.printf("%1$-60s",s);
                }
                else if(counter == 4){
                    System.out.printf("%1$-95s",s);
                }
                else if(counter == 5){
                    System.out.printf("%1$-15s",s);
                }
                else if(counter == 6){
                    System.out.printf("%1$-15s",s);
                }
                else if(counter == 7){
                    System.out.printf("%1$-20s",s);
                }
                counter += 1;
            }
            System.out.println();
            rowCounter += 1;
        }
        System.out.print("    ");
        System.out.printf("%1$-54s","MOVIE TITLE");
        System.out.printf("%1$-35s","DIRECTOR");
        System.out.printf("%1$-40s","GENRES");
        System.out.printf("%1$-60s","ACTORS");
        System.out.printf("%1$-95s","KEYWORDS");
        System.out.printf("%1$-15s","IMDB SCORE");
        System.out.printf("%1$-15s","USER VOTES");
        System.out.printf("%1$-20s","SCORE");
        System.out.println();
    }

    // Other Functions
    public void clearScreen(){
        for(int i = 0; i <= 1000; i++){
            System.out.println();
        }
    }
}