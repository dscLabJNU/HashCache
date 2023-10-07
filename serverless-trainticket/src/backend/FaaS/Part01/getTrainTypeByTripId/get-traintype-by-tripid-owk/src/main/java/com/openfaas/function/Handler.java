
import com.openfaas.function.service.TravelService;
import com.openfaas.function.service.TravelServiceImpl;

import com.google.gson.JsonObject;
import com.google.gson.Gson;

import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;


/**
 * function11 getTrainTypeByTripId
 *
 * get train type by tripId
 * Http Method : GET
 * <p>
 * 原API地址： "http://ts-travel-service:12346/api/v1/travelservice/train_types/{tripId}
 * <p>
 * 输入：(String)tripId
 * 输出：(Object)TrainType
 */
public class Handler {

    private static TravelService travelService = new TravelServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 
        String owPath = args.get("__ow_path").getAsString();
        String tripId = owPath.substring(owPath.lastIndexOf("/")+1);

        // String tripId = req.getPath().get("tripId");
        mResponse mRes = travelService.getTrainTypeByTripId(tripId);
        
        Gson gson = new Gson();
        JsonObject res = new JsonObject();
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);
        
        int inputHash = tripId.hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getTrainTypeByTripId,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
