
import com.openfaas.function.repository.ConfigRepository;
import com.openfaas.function.repository.ConfigRepositoryImpl;

import com.google.gson.JsonObject;
import com.google.gson.Gson;

public class Handler {

    private static ConfigRepository configRepository = new ConfigRepositoryImpl();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();

        if (configRepository.init()) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");


        return res;
    }
}
