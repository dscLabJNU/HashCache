// package com.openfaas.function;

import com.openfaas.function.service.ContactsService;
import com.openfaas.function.service.ContactsServiceImpl;
// import com.openfaas.model.IHandler;
// import com.openfaas.model.IResponse;
// import com.openfaas.model.IRequest;
// import com.openfaas.model.Response;
import com.google.gson.JsonObject;
import com.google.gson.Gson;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

import java.util.UUID;

public class Handler {

    private static ContactsService contactsService = new ContactsServiceImpl();
    
    // private String extractAccountId(String owPath){
    //     String accountId = owPath.substring(owPath.lastIndexOf("/"));
    //     return accountId;
    // }

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis(); 
        Gson gson = new Gson();
        String owPath = args.get("__ow_path").getAsString();
        String accountId = owPath.substring(owPath.lastIndexOf("/")+1);;

        mResponse mRes = contactsService.findContactsByAccountId(UUID.fromString(accountId));
        JsonObject res = new JsonObject();
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);
        // res.setBody(JsonUtils.object2Json(mRes));
        // res.setHeader("Access-Control-Allow-Origin","*");
        // res.setHeader("Access-Control-Allow-Methods", "*");
        // res.setHeader("Access-Control-Allow-Headers", "x-requested-with,Authorization,content-type");
        int inputHash = accountId.hashCode();
        long duration = System.currentTimeMillis() - startTime;
        System.out.println("FunctionLog: findContactsByAccountId,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
	    return res;
    }
}
