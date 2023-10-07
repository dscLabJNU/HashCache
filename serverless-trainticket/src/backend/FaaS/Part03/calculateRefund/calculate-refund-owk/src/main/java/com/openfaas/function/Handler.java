// package com.openfaas.function;

import com.openfaas.function.service.CancelService;
import com.openfaas.function.service.CancelServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler {
    private static CancelService cancelService = new CancelServiceImpl();

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis(); 
        JsonObject res = new JsonObject();
        
        // res.setHeader("Access-Control-Allow-Origin", "*");
        // res.setHeader("Access-Control-Allow-Methods", "GET");
        // res.setHeader("Access-Control-Allow-Headers", "x-requested-with,Authorization,content-type");

        try {
            System.out.println("args: "+args);
            String owPath = args.get("__ow_path").getAsString();
            String orderId = owPath.substring(owPath.lastIndexOf("/")+1);

            mResponse mRes = cancelService.calculateRefund(orderId);
            
            Gson gson = new Gson();
            JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
            res.add("body", body);
            long duration = System.currentTimeMillis() - startTime;
            System.out.println("FunctionLog: calculateRefund,"+orderId.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        } catch (Exception e) {
            e.printStackTrace();
        }

	    return res;
    }
}
