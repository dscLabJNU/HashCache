package com.openfaas.function.repository;

import com.mongodb.client.*;
import com.openfaas.function.entity.Payment;
import edu.fudan.common.util.JsonUtils;
import org.bson.Document;

import java.util.ArrayList;
import java.util.List;

import static com.mongodb.client.model.Filters.eq;

public class PaymentRepositoryImpl implements PaymentRepository {
    MongoClient mongoClient = MongoClients.create("mongodb://ts-serverless-inside-payment-mongo.default:27017");
    private MongoDatabase database = mongoClient.getDatabase("ts");
    private MongoCollection<Document> collection = database.getCollection("payment");


    @Override
    public List<Payment> findByUserId(String userId) {
        List<Payment> result = new ArrayList<>();
        Document tempDoc;
        MongoCursor<Document> cursor = collection.find(eq("userId", userId)).iterator();
        try {
            while (cursor.hasNext()) {
                tempDoc = cursor.next();
                tempDoc.remove("_id");
                result.add(JsonUtils.json2Object(tempDoc.toJson(), Payment.class));
            }
        } finally {
            cursor.close();
        }
        return result;
    }

    @Override
    public void save(Payment payment) {
        Document doc = new Document(JsonUtils.object2Map(payment));
        collection.insertOne(doc);
    }
}
