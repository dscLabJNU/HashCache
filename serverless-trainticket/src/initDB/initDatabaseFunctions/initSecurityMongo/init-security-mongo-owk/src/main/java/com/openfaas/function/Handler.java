
import com.openfaas.function.repository.SecurityRepository;
import com.openfaas.function.repository.SecurityRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;



public class Handler {

    private static SecurityRepository securityRepository = new SecurityRepositoryImpl();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();

        if (securityRepository.init()) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");

        return res;
    }
}
