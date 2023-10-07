
import com.openfaas.function.repository.UserRepository;
import com.openfaas.function.repository.UserRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;



public class Handler {

    private static UserRepository userRepository = new UserRepositoryImpl();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();

        if (userRepository.init()) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");


        return res;
    }
}
