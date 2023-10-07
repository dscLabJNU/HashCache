
import com.openfaas.function.entity.*;
import com.openfaas.function.service.OrderService;
import com.openfaas.function.service.OrderServiceImpl;

import com.google.gson.JsonObject;
import com.google.gson.Gson;

import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;


public class Handler {
    private static OrderService orderService = new OrderServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 
        Gson gson = new Gson();
        String requestBody = gson.toJson(args.get("__post_data"));
        System.out.println("RequestBody: "+requestBody);

        Order order = JsonUtils.json2Object(requestBody, Order.class);
        mResponse mRes = orderService.create(order);

        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);

        long duration =  System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: createOrder,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
