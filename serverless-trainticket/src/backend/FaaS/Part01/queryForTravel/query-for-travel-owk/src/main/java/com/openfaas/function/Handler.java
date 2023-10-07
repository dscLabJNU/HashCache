// package com.openfaas.function;

import com.openfaas.function.service.BasicService;
import com.openfaas.function.service.BasicServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;

import com.openfaas.function.entity.*;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

/**
 * function2 queryForTravel
 * FINISHED/UNTESTED
 * <p>
 * query basic travel information
 * Http Method : POST
 * <p>
 * 原API地址："http://ts-basic-service:15680/api/v1/basicservice/basic/travel"
 * <p>
 * 输入：(object)Travel
 * 输出：(object)TravelResult
 */

public class Handler {

    private static BasicService basicService = new BasicServiceImpl();

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis(); 
        Gson gson = new Gson();
        String requestBody = gson.toJson(args.get("__post_data"));
        System.out.println("RequestBody: "+requestBody);

        Travel info = JsonUtils.json2Object(requestBody, Travel.class);
        mResponse mRes = basicService.queryForTravel(info);

        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);

        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: queryForTravel,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
