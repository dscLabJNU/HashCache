package com.openfaas.function;

import com.openfaas.function.service.InsidePaymentService;
import com.openfaas.function.service.InsidePaymentServiceImpl;
import com.openfaas.model.IHandler;
import com.openfaas.model.IResponse;
import com.openfaas.model.IRequest;
import com.openfaas.model.Response;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler implements com.openfaas.model.IHandler {
    private InsidePaymentService insidePaymentService = new InsidePaymentServiceImpl();

    public IResponse Handle(IRequest req) {
        long startTime=System.currentTimeMillis(); 
        String userId = req.getPath().get("userId");
        String money = req.getPath().get("money");
        mResponse mRes = insidePaymentService.drawBack(userId,money);

        Response res = new Response();
        res.setBody(JsonUtils.object2Json(mRes));
        int inputHash = userId.concat(money).hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: drawBack,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
