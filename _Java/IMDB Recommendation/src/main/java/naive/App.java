package naive;
import java.io.IOException;
import java.util.Random;
import java.util.Scanner;
public class App {

    private static Scanner scanner = new Scanner(System.in);
    private static functions fn = new functions();
    public static void main( String[] args ) throws IOException, InterruptedException {

        boolean exit = false;
        while(!exit){
            System.out.println("--------------------");
            System.out.println("WELCOME TO IMDB 5000");
            System.out.println("--------------------");
            System.out.println("1. Create user");
            System.out.println("2. Log in");
            System.out.println("3. Exit");
            System.out.println("--------------------");

            boolean optionOK = false;
            String str_option;
            int option = -1;
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

            int userExist = 3;

            //Request data
            System.out.print("User:");
            String user = scanner.next();
            System.out.print("Password:");
            String password = scanner.next();

            switch (option){
                case 1:

                    //Validate if user exist
                    try{ userExist = fn.userStatus(user,password);}
                    catch(Exception e){System.out.println(e.getMessage().toString());}

                    if(userExist == 1){
                        System.out.println("This user already exists");
                        break;
                    }
                    else if(userExist == 2){
                        //Create user
                        System.out.println("User created!");
                        //Show movie with simple algorithm
                    }
                    else if(userExist == 3){
                        //Send path to CSV
                        System.out.println("User created!");
                        System.out.println("You are the first user in the system, please enter a path to read a CSV archive");
                        String csv_path = scanner.next();
                        //Show movie with simple algorithm
                        String movies = fn.simplexWithPath(user,csv_path);
                    }
                    break;
                case 2:

                    //Validate if user exist
                    try{ userExist = fn.userStatus(user,password);}
                    catch(Exception e){System.out.println(e.getMessage().toString());}

                    if(userExist == 2){
                        System.out.println("This user not exists");
                        break;
                    }
                    else if(userExist == 4){
                        System.out.println("Your password is wrong");
                        break;
                    }
                    else if(userExist == 5){
                        //Show movie with complex algorithm (If user has movies rated)
                        //Show movie with simple algorithm (If user hasn't movies rated)
                    }
                    break;
                case 3:
                    exit = true;
                    break;
            }

            if(userExist == 2 || userExist == 3 || userExist == 5){
                System.out.println("IMDB 5000");
                System.out.println("1. Select movie to vote");
                System.out.println("2. Exit");
            }
        }
    }
}