// package com.openfaas.function;


import com.openfaas.function.service.StationService;
import com.openfaas.function.service.StationServiceImpl;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

import java.util.List;


public class Handler {

    private static StationService stationService = new StationServiceImpl();

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis();
        Gson gson = new Gson();
        String requestBody = gson.toJson(args.get("__post_data"));
        // System.out.println("requestBody: "+ requestBody);

        List<String> info = JsonUtils.json2Object(requestBody, List.class);
        mResponse mRes = stationService.queryByIdBatch(info);

        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        // System.out.println("Result: "+ res);
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getStationIdListByNameList,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
