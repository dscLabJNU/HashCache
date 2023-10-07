
import com.openfaas.function.repository.AddMoneyRepository;
import com.openfaas.function.repository.AddMoneyRepositoryImpl;
import com.openfaas.function.repository.PaymentRepository;
import com.openfaas.function.repository.PaymentRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;


public class Handler {

    private static AddMoneyRepository addMoneyRepository = new AddMoneyRepositoryImpl();
    private static PaymentRepository paymentRepository = new PaymentRepositoryImpl();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();

        if (addMoneyRepository.init() && paymentRepository.init()) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");



        return res;
    }
}
