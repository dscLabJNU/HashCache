import com.openfaas.function.repository.StationRepository;
import com.openfaas.function.repository.StationRepositoryImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import com.openfaas.function.entity.Station;

import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

import java.util.ArrayList;
import java.util.Arrays;

public class Handler {

    private static StationRepository stationRepository = new StationRepositoryImpl();
    private static Gson gson = new Gson();

    public static JsonObject main(JsonObject args) {                
        JsonObject res = new JsonObject();

        // Parse the stations from the request.
        Station[] stationsArray = gson.fromJson(args.get("stations"), Station[].class);
        ArrayList<Station> stations = new ArrayList<>(Arrays.asList(stationsArray));

        if (stationRepository.init(stations)) {
            res.addProperty("body", "Success");
        } else res.addProperty("body", "Fail");


        return res;
    }
}
