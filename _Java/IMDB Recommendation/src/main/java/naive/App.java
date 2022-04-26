package naive;
import javax.swing.*;
public class App {
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