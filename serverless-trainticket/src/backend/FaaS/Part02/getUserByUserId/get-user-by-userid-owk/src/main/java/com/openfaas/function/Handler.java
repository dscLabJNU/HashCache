
import com.openfaas.function.service.UserService;
import com.openfaas.function.service.UserServiceImpl;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;
import com.google.gson.JsonObject;
import com.google.gson.Gson;

public class Handler {

    private static UserService userService = new UserServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 

        String owPath = args.get("__ow_path").getAsString();
        String accountId = owPath.substring(owPath.lastIndexOf("/")+1);

        mResponse mRes = userService.findByUserId(accountId);


        Gson gson = new Gson();
        JsonObject res = new JsonObject();
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);
        

        int inputHash = accountId.hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getUserByUserId,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
