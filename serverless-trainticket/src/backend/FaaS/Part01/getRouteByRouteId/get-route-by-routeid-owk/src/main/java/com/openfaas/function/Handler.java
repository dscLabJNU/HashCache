// package com.openfaas.function;

import com.openfaas.function.service.RouteService;
import com.openfaas.function.service.RouteServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;


/**
 * FINISHED
 * function3 getRouteByRouteId
 * 根据用户输入返回符合条件的所有列车班次
 * GET route info
 * Http Method : GET
 * <p>
 * 原API地址：http://ts-route-service:11178/api/v1/routeservice/routes/ + routeId
 * <p>
 * 输入：(String)RouteId
 * 输出：(Object)route
 */

public class Handler {
    private static RouteService routeService = new RouteServiceImpl();

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis(); 
        String owPath = args.get("__ow_path").getAsString();
        String routeId = owPath.substring(owPath.lastIndexOf("/")+1);

        // String routeId = req.getPath().get("routeId");

        mResponse mRes = routeService.getRouteById(routeId);

        JsonObject res = new JsonObject();

        Gson gson = new Gson();
        // res.setBody(JsonUtils.object2Json(mRes));
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);
        int inputHash = routeId.hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: getRouteByRouteId,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
