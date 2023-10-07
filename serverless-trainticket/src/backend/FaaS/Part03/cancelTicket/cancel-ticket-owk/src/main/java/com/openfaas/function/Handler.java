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

        // if (req.getHeaders().get("Access-control-request-method") == null ) {
            String owPath = args.get("__ow_path").getAsString();
            int secondLastSlashIndex = owPath.lastIndexOf("/", owPath.lastIndexOf("/")-1);
            String orderId = owPath.substring(secondLastSlashIndex+1, owPath.lastIndexOf("/"));
            String loginId = owPath.substring(owPath.lastIndexOf("/")+1);
            mResponse mRes = cancelService.cancelOrder(orderId, loginId);

            Gson gson = new Gson();
            // res.setBody(JsonUtils.object2Json(mRes));
            JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
            res.add("body", body);
            int inputHash = orderId.concat(loginId).hashCode();
            long duration = System.currentTimeMillis() - startTime;
            System.out.println("FunctionLog: cancelTicket,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        // }

        return res;
    }
}
