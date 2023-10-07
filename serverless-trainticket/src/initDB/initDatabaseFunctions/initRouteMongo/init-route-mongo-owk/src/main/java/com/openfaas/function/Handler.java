
import com.openfaas.function.repository.RouteRepository;
import com.openfaas.function.repository.RouteRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;

import com.openfaas.function.entity.RouteInfo;
import java.util.ArrayList;
import java.util.Arrays;


public class Handler {

    private static RouteRepository routeRepository = new RouteRepositoryImpl();
    private static Gson gson = new Gson();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();
        
        // Parse the stations from the request.
        RouteInfo[] routesArray = gson.fromJson(args.get("routes"), RouteInfo[].class);
        ArrayList<RouteInfo> routeInfos = new ArrayList<>(Arrays.asList(routesArray));


        if (routeRepository.init(routeInfos)) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");


        return res;
    }
}
