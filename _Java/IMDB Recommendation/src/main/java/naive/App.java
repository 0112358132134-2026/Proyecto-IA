package naive;
import java.io.IOException;
import java.util.Scanner;
public class App {
    private static final Scanner scanner = new Scanner(System.in);
    private static final functions fn = new functions();
    public static void main( String[] args ) throws IOException, InterruptedException {

        boolean csvExists = fn.csvExist();
        boolean optionOK = false;
        String str_option = "";

        if (csvExists){
            while(!optionOK){
                System.out.println("There is already data loaded, do you want to load a new data? (Yes/No)");
                str_option = scanner.next().toLowerCase();
                if(str_option.equals("yes") || str_option.equals("no") || str_option.equals("n") || str_option.equals("y")){
                    optionOK = true;
                }
                fn.cls();
            }
            if(str_option.equals("yes") || str_option.equals("y")){
                boolean validFile = false;
                while(!validFile){
                    System.out.println("Please enter a file.csv to import new data");
                    String csv_file = scanner.next();
                    validFile = fn.reload_CSV(csv_file);
                    fn.clearScreen();
                }
                System.out.println("The csv file was uploaded successfully");
            }
        }
        else{
            boolean validFile = false;
            while(!validFile){
                System.out.println("Please enter a file.csv to import data");
                String csv_file = scanner.next();
                validFile = fn.load_CSV(csv_file);
                fn.clearScreen();
            }
            System.out.println("The csv file was uploaded successfully");
        }

        boolean exit = false;
        while(!exit){
            System.out.println("--------------------");
            System.out.println("WELCOME TO IMDB 5000");
            System.out.println("--------------------");
            System.out.println("1. Create user");
            System.out.println("2. Log in");
            System.out.println("3. Exit");
            System.out.println("--------------------");

            int option = -1;
            optionOK = false;
            while(!optionOK){
                try{
                    System.out.print("Please enter a option:");
                    str_option = scanner.next();
                    if(str_option.equals("1") || str_option.equals("2") || str_option.equals("3")){
                        optionOK = true;
                        option = Integer.parseInt(str_option);
                    }
                } catch(Exception e){}
            }

            String user;
            String password;
            int userStatus = -1;
            String information = "";
            switch (option){
                case 1:

                    System.out.print("User:");
                    user = scanner.next();
                    System.out.print("Password:");
                    password = scanner.next();

                    try{ userStatus = fn.userStatus(user,password,option);}
                    catch(Exception e){System.out.println(e.getMessage());}

                    if(userStatus == 1){
                        System.out.println("This user already exists");
                        break;
                    }
                    else if(userStatus == 2){
                        System.out.println("User created!");
                    }
                    break;
                case 2:

                    System.out.print("User:");
                    user = scanner.next();
                    System.out.print("Password:");
                    password = scanner.next();

                    //Validate if user exist
                    try{ userStatus = fn.userStatus(user,password,option);}
                    catch(Exception e){System.out.println(e.getMessage());}

                    if(userStatus == 2){
                        System.out.println("This user not exists");
                        break;
                    }
                    else if(userStatus == 3){
                        System.out.println("Your password is wrong");
                        break;
                    }
                    else if(userStatus == 4){
                        System.out.println("OK!");
                    }
                    break;
                case 3:
                    exit = true;
                    break;
            }
            fn.clearScreen();
            System.out.println(information);
            if(((userStatus == 2 && option == 1) || userStatus == 4 || option == 3) && !exit){
                boolean exitToSecondMenu = false;
                while(!exitToSecondMenu){
                    System.out.println("--------------------");
                    System.out.println("IMDB 5000");
                    System.out.println("--------------------");
                    System.out.println("1. View recommendations");
                    System.out.println("2. Search movie");
                    System.out.println("3. Show all movies");
                    System.out.println("4. Rent a movie");
                    System.out.println("5. Upload another csv file");
                    System.out.println("6. Exit");
                    System.out.println("--------------------");

                    optionOK = false;
                    while(!optionOK){
                        try{
                            System.out.print("Please enter a option:");
                            str_option = scanner.next();
                            if(str_option.equals("1") || str_option.equals("2") || str_option.equals("3") || str_option.equals("4") || str_option.equals("5") || str_option.equals("6")) {
                                optionOK = true;
                                option = Integer.parseInt(str_option);
                            }
                        } catch(Exception e){}
                    }
                    fn.clearScreen();
                    switch (option){
                        case 1:
                            System.out.println("Recommendations");
                            //Show the simplex algorithm if not exist user data
                            //Show the complex algorithm if exist user data
                            break;
                        case 2:
                            fn.search();
                            break;
                        case 3:
                            Movies movies = fn.showAllMovies();
                            fn.printAllMovie(movies);
                            break;
                        case 4:
                            // If it is the first time, ask him 10 options
                            fn.rentAMovie();
                            break;
                        case 5:
                            boolean validFile = false;
                            while(!validFile){
                                System.out.println("Please enter a file.csv to import a new data");
                                String csv_file = scanner.next();
                                validFile = fn.reload_CSV(csv_file);
                            }
                            System.out.println("The csv file was uploaded successfully");
                            break;
                        case 6:
                            exitToSecondMenu = true;
                            break;
                    }
                    fn.clearScreen();
                }
            }
        }
    }
}