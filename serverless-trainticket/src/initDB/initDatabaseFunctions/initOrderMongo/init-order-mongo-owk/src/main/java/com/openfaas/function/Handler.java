
import com.openfaas.function.repository.OrderRepository;
import com.openfaas.function.repository.OrderRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;


public class Handler {

    private static OrderRepository orderRepository = new OrderRepositoryImpl();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();

        if (orderRepository.init()) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");

        return res;
    }
}
