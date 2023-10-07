
import com.openfaas.function.repository.TrainTypeRepository;
import com.openfaas.function.repository.TrainTypeRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;


public class Handler {

    private static TrainTypeRepository trainTypeRepository = new TrainTypeRepositoryImpl();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();


        if (trainTypeRepository.init()) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");


        return res;
    }
}
