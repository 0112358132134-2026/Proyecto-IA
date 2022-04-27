package naive;
import com.google.firebase.database.DatabaseReference;
import java.io.IOException;
public class IMDB_DB {

    public DatabaseReference connect() {

        ConnectToDB fbs = null;
        try {
            fbs = new ConnectToDB();
        } catch (
                IOException e) {
            e.printStackTrace();
        }

        DatabaseReference db = fbs.getDb()
                .getReference("/");

        db.child("vane").setValueAsync(34);
        db.child("osos").setValueAsync(23);

        return db;
    }
}