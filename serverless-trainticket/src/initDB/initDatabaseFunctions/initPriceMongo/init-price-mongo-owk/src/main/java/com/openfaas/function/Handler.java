
import com.openfaas.function.repository.PriceConfigRepository;
import com.openfaas.function.repository.PriceConfigRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;

import com.openfaas.function.entity.PriceConfig;
import java.util.ArrayList;
import java.util.Arrays;

public class Handler {

    private static PriceConfigRepository priceConfigRepository = new PriceConfigRepositoryImpl();
    private static Gson gson = new Gson();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();
        
        // Parse the stations from the request.
        PriceConfig[] priceArray = gson.fromJson(args.get("prices"), PriceConfig[].class);
        
        
        ArrayList<PriceConfig> priceConfigs = new ArrayList<>(Arrays.asList(priceArray));

        if (priceConfigRepository.init(priceConfigs)) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");


        return res;
    }
}
