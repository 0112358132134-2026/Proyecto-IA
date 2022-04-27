package naive;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.database.FirebaseDatabase;
import java.io.FileInputStream;
import java.io.IOException;
public class ConnectToDB {
    FirebaseDatabase db;
    public ConnectToDB() throws IOException {

        FileInputStream fis = new FileInputStream("clave.json");

        FirebaseOptions options = new FirebaseOptions.Builder()
                .setCredentials(GoogleCredentials.fromStream(fis))
                .setDatabaseUrl("https://bd-imdb-default-rtdb.firebaseio.com/")
                .build();

        FirebaseApp.initializeApp(options);
        db = FirebaseDatabase.getInstance();
    }

    public FirebaseDatabase getDb() { return db; }
}