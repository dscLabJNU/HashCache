// package com.openfaas.function;

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

        String owPath = args.get("__ow_path").getAsString();
        String orderId = owPath.substring(owPath.lastIndexOf("/")+1);
        // String OrderId = req.getPath().get("orderId");
        mResponse mRes = orderService.getOrderById(orderId);

        Gson gson = new Gson();
        JsonObject res = new JsonObject();
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);
        // res.setBody(JsonUtils.object2Json(mRes));
        
        int inputHash = orderId.hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getOrderById,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
