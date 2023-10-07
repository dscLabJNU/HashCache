// package com.openfaas.function;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.openfaas.function.service.StationService;
import com.openfaas.function.service.StationServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;
import org.bson.Document;
import java.net.URLDecoder;
import java.io.UnsupportedEncodingException;


/**
 * FINISHED
 * function7
 * query-stationID-by-stationName
 * Http Method : GET
 * <p>
 * 原API地址："http://ts-station-service:12345/api/v1/stationservice/stations/id/" + stationName
 * <p>
 * 输入：(String)stationName
 * 输出：(String)stationID
 */

 public class Handler {

    private static StationService stationService = new StationServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 
    	System.out.println("start");
        MongoClient mongoClient = MongoClients.create("mongodb://ts-station-mongo.default:27017");
        MongoDatabase database = mongoClient.getDatabase("ts");
        MongoCollection<Document> collection = database.getCollection("station");
        System.out.println("success");

        String owPathRaw = args.get("__ow_path").getAsString();
        String owPath = "";
        try {
            String owPathTmp = URLDecoder.decode(owPathRaw, "utf-8");
            owPath = URLDecoder.decode(owPathTmp, "utf-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        String stationName = owPath.substring(owPath.lastIndexOf("/")+1);

        // String stationName = req.getPath().get("stationName");
        mResponse mRes = stationService.queryForId(stationName);

        JsonObject res = new JsonObject();
        Gson gson = new Gson();

        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);
        System.out.println("res: "+res);
        int inputHash = stationName.hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: queryForStationIdByStationName,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
