// package com.openfaas.function;

import com.openfaas.function.repository.TripRepositoryImpl;
import com.openfaas.function.service.TravelServiceImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;

import com.openfaas.function.entity.*;
import com.openfaas.function.service.TravelService;


import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

import java.util.ArrayList;
import java.util.Date;


/**
 * function1 queryInfo
 * FINISHED/UNTESTED
 * 根据用户输入返回符合条件的所有列车班次
 * get left trip tickets
 * Http Method : POST
 * <p>
 * 原API地址：ts-travel-service/api/v1/travelservice/trips/left
 * <p>
 * 输入：前端传来的json数据 转成的TripInfo对象
 * 输出：List<TripResponse>
 */

public class Handler {

    private static TravelService travelService = new TravelServiceImpl();

    public static JsonObject main(JsonObject args) {

        long startTime=System.currentTimeMillis(); 
        Gson gson = new Gson();
        String requestBody = gson.toJson(args.get("__post_data"));
        System.out.println("requestBody: "+ requestBody);
        TripInfo info = JsonUtils.json2Object(requestBody, TripInfo.class);
        mResponse mRes = travelService.query(info);

        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        System.out.println("Result: "+ res);
        // res.setHeader("Access-Control-Allow-Origin","*");
        // res.setHeader("Access-Control-Allow-Methods", "POST");
        // res.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
        long duration=System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getLeftTripTickets,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
