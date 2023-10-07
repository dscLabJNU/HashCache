
import com.openfaas.function.entity.Seat;
import com.openfaas.function.service.SeatService;
import com.openfaas.function.service.SeatServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler {
    private static SeatService seatService = new SeatServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 
        Gson gson = new Gson();
        String requestBody = gson.toJson(args.get("__post_data"));
        System.out.println("RequestBody: "+requestBody);

        
        Seat seatRequest = JsonUtils.json2Object(requestBody, Seat.class);
        mResponse mRes = seatService.distributeSeat(seatRequest);

        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);

        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: dipatchSeat,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
