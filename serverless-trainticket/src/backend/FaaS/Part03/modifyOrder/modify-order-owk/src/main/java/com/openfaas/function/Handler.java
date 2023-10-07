// package com.openfaas.function;

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

        String owPath = args.get("__ow_path").getAsString();
        int secondLastSlashIndex = owPath.lastIndexOf("/", owPath.lastIndexOf("/")-1);
        String orderId = owPath.substring(secondLastSlashIndex+1, owPath.lastIndexOf("/"));
        String orderStatus = owPath.substring(owPath.lastIndexOf("/")+1);

        // String OrderId = req.getPath().get("orderId");
        // String orderStatus = req.getPath().get("orderStatus");
        mResponse mRes = orderService.modifyOrder(orderId, Integer.parseInt(orderStatus));

        Gson gson = new Gson();
        JsonObject res = new JsonObject();
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);
        int inputHash = orderId.concat(orderStatus).hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: modifyOrder,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
