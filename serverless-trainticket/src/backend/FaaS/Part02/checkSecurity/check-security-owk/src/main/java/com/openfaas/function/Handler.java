
import com.openfaas.function.service.SecurityService;
import com.openfaas.function.service.SecurityServiceImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

public class Handler {
    private static SecurityService securityService=new SecurityServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 
        String owPath = args.get("__ow_path").getAsString();
        String accountId = owPath.substring(owPath.lastIndexOf("/")+1);

        // String accountId = req.getPath().get("accountId");
        mResponse mRes = securityService.check(accountId);

        Gson gson = new Gson();
        JsonObject res = new JsonObject();
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);

        int inputHash = accountId.hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: checkSecurity,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
