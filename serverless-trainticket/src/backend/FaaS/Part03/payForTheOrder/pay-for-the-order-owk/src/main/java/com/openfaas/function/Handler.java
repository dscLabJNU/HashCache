// package com.openfaas.function;

import com.openfaas.function.entity.PaymentInfo;
import com.openfaas.function.service.InsidePaymentService;
import com.openfaas.function.service.InsidePaymentServiceImpl;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler{
    private static InsidePaymentService insidePaymentService = new InsidePaymentServiceImpl();

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis(); 
        JsonObject res = new JsonObject();

        // res.setHeader("Access-Control-Allow-Origin", "*");
        // res.setHeader("Access-Control-Allow-Methods", "POST");
        // res.setHeader("Access-Control-Allow-Headers", "x-requested-with,Authorization,content-type");

        try {
            Gson gson = new Gson();
            String requestBody = gson.toJson(args.get("__post_data"));
            System.out.println("requestBody: "+requestBody);
            PaymentInfo info= JsonUtils.json2Object(requestBody, PaymentInfo.class);
            mResponse mRes = insidePaymentService.pay(info);

            res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
            // res.setBody(JsonUtils.object2Json(mRes));
            long duration = System.currentTimeMillis() - startTime;
            System.out.println("FunctionLog: payForTheOrder,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return res;
        

    }
    
}
