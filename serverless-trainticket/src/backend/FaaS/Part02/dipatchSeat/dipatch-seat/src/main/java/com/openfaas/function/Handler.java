package com.openfaas.function;

import com.openfaas.function.entity.Seat;
import com.openfaas.function.service.SeatService;
import com.openfaas.function.service.SeatServiceImpl;
import com.openfaas.model.IHandler;
import com.openfaas.model.IResponse;
import com.openfaas.model.IRequest;
import com.openfaas.model.Response;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler implements com.openfaas.model.IHandler {
    private SeatService seatService = new SeatServiceImpl();

    public IResponse Handle(IRequest req) {
        long startTime=System.currentTimeMillis(); 
        Seat seatRequest = JsonUtils.json2Object(req.getBody(), Seat.class);
        mResponse mRes = seatService.distributeSeat(seatRequest);

        Response res = new Response();
        res.setBody(JsonUtils.object2Json(mRes));
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: dipatchSeat,"+req.getBody().hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
