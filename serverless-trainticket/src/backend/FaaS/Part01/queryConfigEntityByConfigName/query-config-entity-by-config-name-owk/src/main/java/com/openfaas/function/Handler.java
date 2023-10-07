// package com.openfaas.function;

import com.openfaas.function.service.ConfigService;
import com.openfaas.function.service.ConfigServiceImpl;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;


/**
 * function12 queryConfigEntity
 *
 * query config entity by configName
 * Http Method : GET
 * <p>
 * 原API地址："http://ts-config-service:15679/api/v1/configservice/configs/" + configName
 * <p>
 * 输入：(String)configName
 * 输出：(Object)Config
 */

public class Handler {

    private static ConfigService configService = new ConfigServiceImpl();

    public static JsonObject main(JsonObject args) {                
        long startTime=System.currentTimeMillis(); 

        String owPath = args.get("__ow_path").getAsString();
        String configName = owPath.substring(owPath.lastIndexOf("/")+1);

        // String configName = req.getPath().get("configName");
        mResponse mRes = configService.query(configName);

        JsonObject res = new JsonObject();
        Gson gson = new Gson();

        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);

        int inputHash = configName.hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: queryConfigEntityByConfigName,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
