package naive;
import javax.swing.*;
import java.io.BufferedReader;
import java.io.FileReader;
public class functions{
    private static BufferedReader reader;
    private static String line;
    private static String lines[];

    public static void readFile(String path){
        try{
            reader = new BufferedReader(new FileReader(path));
            while ((line = reader.readLine()) != null){
                lines = line.split(",");
                printLine();
                System.out.println();
            }
        } catch (Exception e){
            JOptionPane.showMessageDialog(null,e);
        }
    }

    public static void printLine(){
        for(int i = 0; i<lines.length;i++){
            System.out.print(lines[i] + "  |  ");
        }
    }
}