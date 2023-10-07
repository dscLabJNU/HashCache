
import com.openfaas.function.dto.BasicAuthDto;
import com.openfaas.function.service.TokenService;
import com.openfaas.function.service.TokenServiceImpl;


import com.google.gson.JsonObject;
import com.google.gson.Gson;



import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;


/**
 * function1 queryInfo
 * FINISHED/UNTESTED
 * 根据用户输入返回符合条件的所有列车班次
 * get left trip tickets
 * Http Method : POST
 * <p>
 * 原API地址：ts-travel-service/api/v1/travelservice/trips/left
 * <p>
 * 输入：前端传来的json数据 转成的TripInfo对象
 * 输出：List<TripResponse>
 */

 public class Handler {

    private static TokenService tokenService = new TokenServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 
        Gson gson = new Gson();
        String requestBody = gson.toJson(args.get("__post_data"));
        System.out.println("RequestBody: "+requestBody);


        BasicAuthDto dao = JsonUtils.json2Object(requestBody, BasicAuthDto.class);
        mResponse mRes = tokenService.getToken(dao);

        JsonObject res = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);

        // res.setHeader("Access-Control-Allow-Origin", "*");
        // res.setHeader("Access-Control-Allow-Methods", "POST");
        // res.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getToken,"+requestBody.hashCode()+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
