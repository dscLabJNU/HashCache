
import com.openfaas.function.service.ContactsService;
import com.openfaas.function.service.ContactsServiceImpl;

import com.google.gson.JsonObject;
import com.google.gson.Gson;

import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

import java.util.UUID;

public class Handler {
    private static ContactsService contactsService = new ContactsServiceImpl();

    public static JsonObject main(JsonObject args) {
        long startTime=System.currentTimeMillis(); 
        String owPath = args.get("__ow_path").getAsString();
        String contactsId = owPath.substring(owPath.lastIndexOf("/")+1);

        // String contactsId = req.getPath().get("contactsId");
        mResponse mRes = contactsService.findContactsById(UUID.fromString(contactsId));

        Gson gson = new Gson();
        JsonObject res = new JsonObject();
        // res.setBody(JsonUtils.object2Json(mRes));
        JsonObject body = gson.fromJson(JsonUtils.object2Json(mRes), JsonObject.class);
        res.add("body", body);
        
        long duration = System.currentTimeMillis() - startTime;
        int inputHash = contactsId.hashCode();
        System.out.println("FunctionLog: getContactsByContactsId,"+inputHash+","+JsonUtils.object2Json(mRes).hashCode()+","+duration);
        return res;
    }
}
