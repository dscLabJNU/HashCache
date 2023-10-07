
import com.openfaas.function.service.OrderService;
import com.openfaas.function.service.OrderServiceImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

import java.util.Date;


/**
 * function6 checkSecurityAboutOrder
 * check order if security
 * Http Method : POST
 * 输入：(String)checkDate,(String)accountId
 * 输出：(Object)Security
 */
public class Handler {

    private static OrderService orderService=new OrderServiceImpl();
    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 
        // String owPath = args.get("__ow_path").getAsString();
        // int secondLastSlashIndex = owPath.lastIndexOf("/", owPath.lastIndexOf("/")-1);
        // String accountId = owPath.substring(secondLastSlashIndex+1, owPath.lastIndexOf("/"));
        // String checkDate = owPath.substring(owPath.lastIndexOf("/")+1);
        JsonObject requestBody = args.get("__post_data").getAsJsonObject();
        String checkDate = requestBody.get("checkDate").getAsString();
        String accountId = requestBody.get("accountId").getAsString();


        mResponse mRes = orderService.checkSecurityAboutOrder(new Date(checkDate),accountId);

        Gson gson = new Gson();
        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);

        int inputHash = accountId.concat(checkDate).hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: checkSecurityAboutOrder,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
