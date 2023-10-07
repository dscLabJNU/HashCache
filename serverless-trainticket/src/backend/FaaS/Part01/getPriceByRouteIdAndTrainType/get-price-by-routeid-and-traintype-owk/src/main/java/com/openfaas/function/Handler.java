// package com.openfaas.function;

import com.openfaas.function.service.PriceService;
import com.openfaas.function.service.PriceServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;


/**
 * function5 findByRouteIdAndTrainType
 * FINSHED/UNTESTED
 * get price by routeid and train type
 * Http Method : GET
 * <p>
 * 原API地址："http://ts-price-service:16579/api/v1/priceservice/prices/" + routeId + "/" + trainType
 * <p>
 * 输入：(String)routeId , (String)trainType
 * 输出：(Object)priceConfig
 */
public class Handler {

    private static PriceService priceService = new PriceServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 
        String owPath = args.get("__ow_path").getAsString();
        int secondLastSlashIndex = owPath.lastIndexOf("/", owPath.lastIndexOf("/")-1);
        String routeId = owPath.substring(secondLastSlashIndex+1, owPath.lastIndexOf("/"));
        String trainType = owPath.substring(owPath.lastIndexOf("/")+1);

        // String routeId = req.getPath().get("routeId");
        // String trainType = req.getPath().get("trainType");

        mResponse mRes = priceService.findByRouteIdAndTrainType(routeId,trainType);

        Gson gson = new Gson();
        JsonObject res = new JsonObject();
        // res.setBody(JsonUtils.object2Json(mRes));
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);
        
        int inputHash = routeId.concat(trainType).hashCode();
        long duration=System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getPriceByRouteIdAndTrainType,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
