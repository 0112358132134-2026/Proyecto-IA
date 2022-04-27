package naive;
import com.google.firebase.database.*;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
public class ShowDbChanges implements Runnable{
    public void run() {

        FireBaseService fbs = null;
        try {
            fbs = new FireBaseService();
        } catch (IOException e) {
            e.printStackTrace();
        }

        DatabaseReference ref = fbs.getDb()
            .getReference("/");

        Map<String, Integer> users = new HashMap<>();
        users.put("je", 34);
        users.put("ja", 222);
        //ref.setValueAsync(users);

        ref.child("joshy").setValueAsync(34);
        ref.child("pato").setValueAsync(23);
    }
}