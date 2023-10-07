// package com.openfaas.function;

import com.openfaas.function.entity.TrainType;
import com.openfaas.function.service.TrainService;
import com.openfaas.function.service.TrainServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;


/**
 * function4 queryTrainType
 * FINISHED/UNTESTED
 * <p>
 * get train's info by id
 * Http Method : GET
 * <p>
 * 原API地址："http://ts-train-service:14567/api/v1/trainservice/trains/" + trainTypeId
 * <p>
 * 输入：(String)trainTypeId
 * 输出：(Object)TrainType(查不到的的话返回输入的ID)
 */


 public class Handler {
    private static TrainService trainService = new TrainServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 
        String owPath = args.get("__ow_path").getAsString();
        String trainTypeId = owPath.substring(owPath.lastIndexOf("/")+1);

        // String trainTypeId = req.getPath().get("trainTypeId");

        TrainType trainType = trainService.retrieve(trainTypeId);
        mResponse mRes;

        if (trainType == null) {
            mRes=new mResponse(0, "here is no TrainType with the trainType id", trainTypeId);
        } else {
            mRes=new mResponse(1, "success", trainType);
        }

        JsonObject res = new JsonObject();
        Gson gson = new Gson();
        // res.setBody(JsonUtils.object2Json(mRes));
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);

        int inputHash = trainTypeId.hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getTrainTypeByTrainTypeId,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
