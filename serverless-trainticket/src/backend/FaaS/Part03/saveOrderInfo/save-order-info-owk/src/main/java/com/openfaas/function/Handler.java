// package com.openfaas.function;

import com.openfaas.function.entity.Order;
import com.openfaas.function.service.OrderService;
import com.openfaas.function.service.OrderServiceImpl;
// import com.openfaas.model.IHandler;
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
        Gson gson = new Gson();
        String requestBody = gson.toJson(args.get("__post_data"));
        System.out.println("requestBody: "+ requestBody);

        Order orderInfo = JsonUtils.json2Object(requestBody, Order.class);
        mResponse mRes = orderService.saveChanges(orderInfo);

        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        System.out.println("Result: "+ res);

        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: saveOrderInfo,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
