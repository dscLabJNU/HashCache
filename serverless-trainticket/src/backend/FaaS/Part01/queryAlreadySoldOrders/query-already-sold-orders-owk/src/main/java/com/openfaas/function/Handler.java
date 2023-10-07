
import com.openfaas.function.service.OrderService;
import com.openfaas.function.service.OrderServiceImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.DateUtils;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

import java.util.Date;


/**
 * function6 queryAlreadySoldOrders
 * query sold tickets
 * Http Method : POST
 * <p>
 * 原API地址：/api/v1/orderservice/order/{travelDate}/{trainNumber}
 * <p>
 * 输入：(String)travelDate,(String)trainNumber
 * 输出：(Object)SoldTicket
 */

 public class Handler {

    private static OrderService orderService = new OrderServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 

        // String owPath = args.get("__ow_path").getAsString();
        // int secondLastSlashIndex = owPath.lastIndexOf("/", owPath.lastIndexOf("/")-1);
        // String travelDateStr = owPath.substring(secondLastSlashIndex+1, owPath.lastIndexOf("/"));
        // String trainNumber = owPath.substring(owPath.lastIndexOf("/")+1);
        JsonObject requestBody = args.get("__post_data").getAsJsonObject();
        String travelDateStr = requestBody.get("travelDate").getAsString();
        String trainNumber = requestBody.get("trainNumber").getAsString();

        // String travelDateStr = req.getPath().get("travelDate");
        Date travelDate = new Date(travelDateStr);

        // String trainNumber = req.getPath().get("trainNumber");

        mResponse mRes = orderService.queryAlreadySoldOrders(travelDate, trainNumber);

        Gson gson = new Gson();
        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);

        int inputHash = travelDateStr.concat(trainNumber).hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: queryAlreadySoldOrders,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
