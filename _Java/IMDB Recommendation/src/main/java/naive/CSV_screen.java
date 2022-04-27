package naive;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
public class CSV_screen extends JFrame{
    private JPanel panel1;
    private JButton cargarCSVButton;
    private JTextField textField1;

    public CSV_screen(){
        super("IMDB 5000");
        setContentPane(panel1);
        cargarCSVButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                //movie m = functions.GET_MOVIE();
                //String name = m.name;
                //int ratio = m.ratio;
                try {
                    functions.post("http://127.0.0.1:8000/ola","Simon");
                } catch (Exception ex) {
                    throw new RuntimeException(ex);
                }
            }
        });
    }
}