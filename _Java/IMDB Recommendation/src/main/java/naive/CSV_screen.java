package naive;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import naive.functions;
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
                String path = textField1.getText();
                functions.readFile(path);
            }
        });
    }
}