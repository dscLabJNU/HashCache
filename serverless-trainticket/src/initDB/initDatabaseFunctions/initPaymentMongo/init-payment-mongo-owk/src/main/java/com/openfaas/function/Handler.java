
import com.openfaas.function.repository.PaymentRepository;
import com.openfaas.function.repository.PaymentRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;



public class Handler {

    private static PaymentRepository paymentRepository = new PaymentRepositoryImpl();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();

        if (paymentRepository.init()) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");



        return res;
    }
}
