package naive;
import java.io.IOException;
import java.util.Scanner;
public class App {
    private static final Scanner scanner = new Scanner(System.in);
    private static final functions fn = new functions();
    public static void main( String[] args ) throws IOException, InterruptedException {

        fn.clearScreen();
        boolean csvExist = fn.csvExist();
        boolean optionOK = false;
        String str_option = "";

        if (csvExist){
            while(!optionOK){
                System.out.println("----------------------------------------------------------------------");
                System.out.println("There is already data loaded, do you want to load a new data? (Yes/No)");
                System.out.println("----------------------------------------------------------------------");
                str_option = scanner.next().toLowerCase();
                if(str_option.equals("yes") || str_option.equals("no") || str_option.equals("n") || str_option.equals("y")){
                    optionOK = true;
                }
                fn.clearScreen();
            }
        }
        if(str_option.equals("yes") || str_option.equals("y") || !csvExist){
            boolean validFile = false;
            while(!validFile){
                System.out.println("Please enter a file.csv to import data: ");
                String csv_file = scanner.next();
                validFile = fn.load_CSV(csv_file);
                fn.clearScreen();
            }
            System.out.println("The csv file was uploaded successfully");
        }

        boolean exit = false;
        while(!exit){
            int option = -1;
            optionOK = false;
            while(!optionOK){
                System.out.println("----------------------");
                System.out.println("|      IMDB 5000      |");
                System.out.println("----------------------");
                System.out.println("|1.    Create user    |");
                System.out.println("|2.      Log in       |");
                System.out.println("|3.       Exit        |");
                System.out.println("----------------------");
                try{
                    System.out.print("Enter a option:");
                    str_option = scanner.next();
                    if(str_option.equals("1") || str_option.equals("2") || str_option.equals("3")){
                        optionOK = true;
                        option = Integer.parseInt(str_option);
                    }
                } catch(Exception e){optionOK = false;}
                fn.clearScreen();
            }

            String user = "";
            String password;
            int userStatus = -1;
            String information = "";

            if(option == 1 || option == 2){
                System.out.print("USER:");
                user = scanner.next();
                System.out.print("PASSWORD:");
                password = scanner.next();

                try{
                    userStatus = fn.userStatus(user,password,option);
                }
                catch(Exception e){
                    System.out.println(e.getMessage());
                }

                switch (userStatus){
                    case 1:
                        information = "This user already exists";
                        break;
                    case 2:
                        if(option == 1){
                            information = "User created!";
                        }
                        else{
                            information = "This user not exists";
                        }
                        break;
                    case 3:
                        information = "Your password is wrong";
                        break;
                }
            }
            else{
                exit = true;
            }

            fn.clearScreen();
            if(((userStatus == 2 && option == 1) || userStatus == 4 || option == 3) && !exit){
                boolean exitToSecondMenu = false;
                System.out.println(information);
                while(!exitToSecondMenu){
                    optionOK = false;
                    while(!optionOK){
                        System.out.println("-----------------------------");
                        System.out.println("|   WELCOME TO IMDB 5000    |");
                        System.out.println("--------------------------- |");
                        System.out.println("|1.  View recommendations   |");
                        System.out.println("|2.      Search movie       |");
                        System.out.println("|3.     Show all movies     |");
                        System.out.println("|4.      Rent a movie       |");
                        System.out.println("|5. Upload another csv file |");
                        System.out.println("|6.         Exit            |");
                        System.out.println("-----------------------------");
                        try{
                            System.out.print("Enter a option:");
                            str_option = scanner.next();
                            if(str_option.equals("1") || str_option.equals("2") || str_option.equals("3") || str_option.equals("4") || str_option.equals("5") || str_option.equals("6")) {
                                optionOK = true;
                                option = Integer.parseInt(str_option);
                            }
                        } catch(Exception e){optionOK = false;}
                        fn.clearScreen();
                    }
                    switch (option){
                        case 1:
                            fn.showRecommendations(user);
                            break;
                        case 2:
                            fn.search();
                            break;
                        case 3:
                            Movies movies = fn.showAllMovies();
                            fn.printAllMovie(movies);
                            break;
                        case 4:
                            fn.rentAMovie(user);
                            break;
                        case 5:
                            boolean validFile = false;
                            while(!validFile){
                                System.out.println("Please enter a file.csv to import a new data");
                                String csv_file = scanner.next();
                                validFile = fn.reload_CSV(csv_file);
                                fn.clearScreen();
                            }
                            System.out.println("The csv file was uploaded successfully");
                            break;
                        case 6:
                            exitToSecondMenu = true;
                            break;
                    }
                    if(option != 3 && option != 1){
                        fn.clearScreen();
                    }
                }
            }
            else {
                System.out.println(information);
            }
        }
    }
}