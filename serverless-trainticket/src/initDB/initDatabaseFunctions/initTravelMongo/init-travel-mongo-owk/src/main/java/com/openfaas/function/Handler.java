
import com.openfaas.function.repository.TripRepository;
import com.openfaas.function.repository.TripRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;

import com.openfaas.function.entity.TravelInfo;
import java.util.ArrayList;
import java.util.Arrays;

public class Handler {

    private static TripRepository tripRepository = new TripRepositoryImpl();
    private static Gson gson = new Gson();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();
        
        // Parse the stations from the request.
        TravelInfo[] travelArray = gson.fromJson(args.get("travels"), TravelInfo[].class);
        JsonObject jsonObject = gson.fromJson(args.get("travles"), JsonObject.class);


        ArrayList<TravelInfo> travelInfos = new ArrayList<>(Arrays.asList(travelArray));

        if (tripRepository.init(travelInfos)) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");


        return res;
    }
}
