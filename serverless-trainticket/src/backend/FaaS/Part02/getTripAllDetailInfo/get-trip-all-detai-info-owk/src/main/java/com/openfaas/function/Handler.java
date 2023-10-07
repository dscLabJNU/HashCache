
import com.openfaas.function.entity.*;
import com.openfaas.function.entity.TripInfo;
import com.openfaas.function.service.TravelService;
import com.openfaas.function.service.TravelServiceImpl;

import com.google.gson.JsonObject;
import com.google.gson.Gson;

import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler {

    private static TravelService travelService = new TravelServiceImpl();

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis(); 
        Gson gson = new Gson();
        String requestBody = gson.toJson(args.get("__post_data"));
        System.out.println("RequestBody: "+requestBody);

        TripAllDetailInfo info= JsonUtils.json2Object(requestBody, TripAllDetailInfo.class);
        mResponse mRes = travelService.getTripAllDetailInfo(info);

        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);

        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getTripAllDetailInfo,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
