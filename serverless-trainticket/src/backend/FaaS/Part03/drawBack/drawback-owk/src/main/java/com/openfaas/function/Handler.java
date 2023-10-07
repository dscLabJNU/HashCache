// package com.openfaas.function;

import com.openfaas.function.service.InsidePaymentService;
import com.openfaas.function.service.InsidePaymentServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler {
    private static InsidePaymentService insidePaymentService = new InsidePaymentServiceImpl();

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis(); 
        
        String owPath = args.get("__ow_path").getAsString();
        int secondLastSlashIndex = owPath.lastIndexOf("/", owPath.lastIndexOf("/")-1);
        String userId = owPath.substring(secondLastSlashIndex+1, owPath.lastIndexOf("/"));
        String money = owPath.substring(owPath.lastIndexOf("/")+1);
        // String userId = req.getPath().get("userId");
        // String money = req.getPath().get("money");
        mResponse mRes = insidePaymentService.drawBack(userId, money);

        Gson gson = new Gson();
            // res.setBody(JsonUtils.object2Json(mRes));
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        JsonObject res = new JsonObject();
        res.add("body", body);
        // res.setBody(JsonUtils.object2Json(mRes));
        int inputHash = userId.concat(money).hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: drawBack,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
