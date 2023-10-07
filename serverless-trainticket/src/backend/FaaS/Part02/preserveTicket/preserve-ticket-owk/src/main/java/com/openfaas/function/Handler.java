// package com.openfaas.function;

import com.openfaas.function.entity.OrderTicketsInfo;
import com.openfaas.function.service.PreserveService;
import com.openfaas.function.service.PreserveServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler {

    private static PreserveService preserveService = new PreserveServiceImpl();

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis(); 
        JsonObject res = new JsonObject();
        // res.setHeader("Access-Control-Allow-Origin", "*");
        // res.setHeader("Access-Control-Allow-Methods", "POST");
        // res.setHeader("Access-Control-Allow-Headers", "x-requested-with,Authorization,content-type");

        try {
            Gson gson = new Gson();
            String requestBody = gson.toJson(args.get("__post_data"));
            System.out.println("RequestBody: "+requestBody);
            OrderTicketsInfo info = JsonUtils.json2Object(requestBody, OrderTicketsInfo.class);
            mResponse mRes = preserveService.preserve(info);
            
            res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
            long duration = System.currentTimeMillis() - startTime;
            System.out.println("FunctionLog: preserveTicket,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        } catch (Exception e) {
            e.printStackTrace();
        }
        // res.addProperty("Access-Control-Allow-Origin", "*");
        // res.addProperty("Access-Control-Allow-Methods", "POST");
        // res.addProperty("Access-Control-Allow-Headers", "x-requested-with,Authorization,content-type");
        System.out.println("result: "+res);
        return res;
    }
}
