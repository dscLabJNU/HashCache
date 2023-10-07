
import com.openfaas.function.entity.Route;
import com.openfaas.function.service.TravelService;
import com.openfaas.function.service.TravelServiceImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;


/**
 * function9 getRouteByTripId
 * <p>
 * get route by tripId
 * Http Method : GET
 * <p>
 * 原API地址： "http://ts-travel-service:12346/api/v1/travelservice/routes/" + trainNumber,
 * <p>
 * 输入：(String)tripId
 * 输出：(Object)Route
 */

public class Handler {

    private static TravelService travelService = new TravelServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 

        String owPath = args.get("__ow_path").getAsString();
        String trainNumber = owPath.substring(owPath.lastIndexOf("/")+1);

        // String trainNumber = req.getPath().get("tripId");
        mResponse mRes = travelService.getRouteByTripId(trainNumber);

        Gson gson = new Gson();
        JsonObject res = new JsonObject();
        // res.setBody(JsonUtils.object2Json(mRes));
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);

        int inputHash = trainNumber.hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getRouteByTripId,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
