// package com.openfaas.function;

import com.openfaas.function.entity.OrderInfo;
import com.openfaas.function.service.OrderService;
import com.openfaas.function.service.OrderServiceImpl;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;


public class Handler {

    private static OrderService orderService = new OrderServiceImpl();

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis(); 
        JsonObject res = new JsonObject();
        // res.setHeader("Access-Control-Allow-Origin", "*");
        // res.setHeader("Access-Control-Allow-Methods", "POST");
        // res.setHeader("Access-Control-Allow-Headers", "x-requested-with,Authorization,content-type");


        try {
            Gson gson = new Gson();
            String requestBody = gson.toJson(args.get("__post_data"));
            // System.out.println("requestBody: "+requestBody);
            OrderInfo info = JsonUtils.json2Object(requestBody, OrderInfo.class);
            mResponse mRes = orderService.queryOrdersForRefresh(info,info.getLoginId());
            
            res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
            // res.setBody(JsonUtils.object2Json(mRes));
            long duration = System.currentTimeMillis() - startTime;
            System.out.println("FunctionLog: queryOrdersForRefresh,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return res;
    }
}
