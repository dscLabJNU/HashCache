// package com.openfaas.function;

import com.openfaas.function.entity.Payment;
import com.openfaas.function.entity.PaymentInfo;
import com.openfaas.function.service.PaymentService;
import com.openfaas.function.service.PaymentServiceImpl;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler {

    private static PaymentService paymentService = new PaymentServiceImpl();

    public JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis();
        Gson gson = new Gson();
        String requestBody = gson.toJson(args.get("__post_data"));
        System.out.println("requestBody: "+requestBody);

        PaymentInfo info= JsonUtils.json2Object(requestBody, PaymentInfo.class);
        Payment payment=new Payment();
        payment.setOrderId(info.getOrderId());
        payment.setUserId(info.getUserId());
        payment.setPrice(info.getPrice());
        mResponse mRes = paymentService.pay(payment);

        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: createThirdPartyPaymentAndPay,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);

        return res;
    }
}
