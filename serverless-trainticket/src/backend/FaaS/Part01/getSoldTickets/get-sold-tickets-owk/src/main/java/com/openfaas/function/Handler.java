
import com.openfaas.function.entity.*;
import com.openfaas.function.service.OrderService;
import com.openfaas.function.service.OrderServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;


/**
 * function10 getSoldTickets
 * <p>
 * get ticket list by date and trip id
 * Http Method : POST
 * <p>
 * 原API地址： "http://ts-order-service:12031/api/v1/orderservice/order/tickets"
 * <p>
 * 输入：(object)Seat
 * 输出：(Object)LeftTicketInfo
 */
public class Handler {

    private static OrderService orderService = new OrderServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 
        Gson gson = new Gson();
        String requestBody = gson.toJson(args.get("__post_data"));
        System.out.println("RequestBody: "+requestBody);

        Seat seatRequest = JsonUtils.json2Object(requestBody, Seat.class);
        mResponse mRes = orderService.getSoldTickets(seatRequest);

        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);

        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getSoldTickets,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
