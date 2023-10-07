
import com.openfaas.function.repository.ContactsRepository;
import com.openfaas.function.repository.ContactsRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;



public class Handler {

    private static ContactsRepository contactsRepository = new ContactsRepositoryImpl();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();
        
        if (contactsRepository.init()) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");

        return res;
    }
}
