package com.openfaas.function;

import com.openfaas.function.service.CancelService;
import com.openfaas.function.service.CancelServiceImpl;
import com.openfaas.model.IHandler;
import com.openfaas.model.IResponse;
import com.openfaas.model.IRequest;
import com.openfaas.model.Response;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler implements com.openfaas.model.IHandler {

    private CancelService cancelService = new CancelServiceImpl();

    public IResponse Handle(IRequest req) {
        long startTime=System.currentTimeMillis(); 
        Response res = new Response();
        res.setHeader("Access-Control-Allow-Origin", "*");
        res.setHeader("Access-Control-Allow-Methods", "GET");
        res.setHeader("Access-Control-Allow-Headers", "x-requested-with,Authorization,content-type");

        if (req.getHeaders().get("Access-control-request-method") == null ) {
            String orderId = req.getPath().get("orderId");
            String loginId = req.getPath().get("loginId");
            mResponse mRes = cancelService.cancelOrder(orderId, loginId);
            res.setBody(JsonUtils.object2Json(mRes));
            int inputHash = orderId.concat(loginId).hashCode();
            long duration = System.currentTimeMillis() - startTime;
            System.out.println("FunctionLog: cancelTicket,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        }

        return res;
    }
}
