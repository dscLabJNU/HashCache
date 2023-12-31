package com.openfaas.function.service;

import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;
import com.openfaas.function.entity.*;

import java.util.HashMap;

import okhttp3.OkHttpClient;
import java.util.concurrent.TimeUnit;


public class BasicServiceImpl implements BasicService {
    private OkHttpClient client = new OkHttpClient();

    private String function03_URI = "owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/route/getRouteByRouteId";
    private String function04_URI = "owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/traintype/getTrainTypeByTrainTypeId";
    private String function05_URI = "owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/price/getPriceByRouteIdAndTrainType";
    private String function07_URI = "owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/stationId/queryForStationIdByStationName";


    @Override
    public mResponse queryForTravel(Travel info) {

        mResponse response = new mResponse<>();
        TravelResult result = new TravelResult();
        result.setStatus(true);
        response.setStatus(1);
        response.setMsg("Success");
        boolean startingPlaceExist = checkStationExists(info.getStartingPlace());
        boolean endPlaceExist = checkStationExists(info.getEndPlace());

        if (!startingPlaceExist || !endPlaceExist) {
            result.setStatus(false);
            response.setStatus(0);
            response.setMsg("Start place or end place not exist!");
        }

        TrainType trainType = queryTrainType(info.getTrip().getTrainTypeId());
        if (trainType == null) {
            // BasicServiceImpl.LOGGER.info("traintype doesn't exist");
            result.setStatus(false);
            response.setStatus(0);
            response.setMsg("Train type doesn't exist");
        } else {
            result.setTrainType(trainType);
        }

        String routeId = info.getTrip().getRouteId();
        String trainTypeString = null;
        if (trainType != null) {
            trainTypeString = trainType.getId();
        }
        Route route = getRouteByRouteId(routeId);
        PriceConfig priceConfig = queryPriceConfigByRouteIdAndTrainType(routeId, trainTypeString);

        String startingPlaceId = queryForStationId(info.getStartingPlace());
        String endPlaceId = queryForStationId(info.getEndPlace());

        //  log.info("startingPlaceId : " + startingPlaceId + "endPlaceId : " + endPlaceId);

        int indexStart = 0;
        int indexEnd = 0;
        if (route != null) {
            indexStart = route.getStations().indexOf(startingPlaceId);
            indexEnd = route.getStations().indexOf(endPlaceId);
        }

        // log.info("indexStart : " + indexStart + " __ " + "indexEnd : " + indexEnd);
        if (route != null) {
            //     log.info("route.getDistances().size : " + route.getDistances().size());
        }
        HashMap<String, String> prices = new HashMap<>();
        try {
            int distance = 0;
            if (route != null) {
                distance = route.getDistances().get(indexEnd) - route.getDistances().get(indexStart);
            }

            /**
             * We need the price Rate and distance (starting station).
             */
            double priceForEconomyClass = distance * priceConfig.getBasicPriceRate();
            double priceForConfortClass = distance * priceConfig.getFirstClassPriceRate();
            prices.put("economyClass", "" + priceForEconomyClass);
            prices.put("confortClass", "" + priceForConfortClass);
        } catch (Exception e) {
            prices.put("economyClass", "95.0");
            prices.put("confortClass", "120.0");
        }
        result.setPrices(prices);
        result.setPercent(1.0);
        response.setData(result);
        return response;
    }

    private String queryForStationId(String stationName) {
        String ret = "";
        try {
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://"+function07_URI + "/" + stationName)
                    .get()
                    .build();

            // okhttp3.Response response = client.newCall(request).execute();
            okhttp3.Response response = new OkHttpClient.Builder()
            .connectTimeout(60, TimeUnit.SECONDS) //连接超时
            .readTimeout(60, TimeUnit.SECONDS) //读取超时
            .writeTimeout(60, TimeUnit.SECONDS) //写超时
            .build()
            .newCall(request).execute();
            ret = response.body().string();

        } catch (Exception e) {
            e.printStackTrace();
        }
        mResponse stationIDRes = JsonUtils.json2Object(ret, mResponse.class);

        String stationID = "";
        if (stationIDRes.getStatus() == 1) {
            stationID = (String) stationIDRes.getData();
        }
        return stationID;
    }

    private boolean checkStationExists(String stationName) {
        String ret = "";
        try {
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://"+function07_URI + "/" + stationName)
                    .get()
                    .build();

            // okhttp3.Response response = client.newCall(request).execute();
            okhttp3.Response response = new OkHttpClient.Builder()
            .connectTimeout(60, TimeUnit.SECONDS) //连接超时
            .readTimeout(60, TimeUnit.SECONDS) //读取超时
            .writeTimeout(60, TimeUnit.SECONDS) //写超时
            .build()
            .newCall(request).execute();
            ret = response.body().string();

        } catch (Exception e) {
            e.printStackTrace();
        }
        mResponse stationIDRes = JsonUtils.json2Object(ret, mResponse.class);
        return stationIDRes.getStatus() == 1;
    }

    private TrainType queryTrainType(String trainTypeId) {
        String ret = "";
        try {
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://"+function04_URI + "/" + trainTypeId)
                    .get()
                    .build();

            // okhttp3.Response response = client.newCall(request).execute();
            okhttp3.Response response = new OkHttpClient.Builder()
            .connectTimeout(60, TimeUnit.SECONDS) //连接超时
            .readTimeout(60, TimeUnit.SECONDS) //读取超时
            .writeTimeout(60, TimeUnit.SECONDS) //写超时
            .build()
            .newCall(request).execute();
            ret = response.body().string();

        } catch (Exception e) {
            e.printStackTrace();
        }
        mResponse TrainTypeRes = JsonUtils.json2Object(ret, mResponse.class);

        TrainType trainType = null;
        if (TrainTypeRes.getStatus() == 1) {
            trainType = JsonUtils.conveterObject(TrainTypeRes.getData(), TrainType.class);
        }
        return trainType;
    }

    private Route getRouteByRouteId(String routeId) {
        String ret = "";
        try {
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://"+function03_URI + "/" + routeId)
                    .get()
                    .build();

            // okhttp3.Response response = client.newCall(request).execute();
            okhttp3.Response response = new OkHttpClient.Builder()
            .connectTimeout(60, TimeUnit.SECONDS) //连接超时
            .readTimeout(60, TimeUnit.SECONDS) //读取超时
            .writeTimeout(60, TimeUnit.SECONDS) //写超时
            .build()
            .newCall(request).execute();
            ret = response.body().string();

        } catch (Exception e) {
            e.printStackTrace();
        }
        mResponse routeRes = JsonUtils.json2Object(ret, mResponse.class);

        Route route = null;
        if (routeRes.getStatus() == 1) {
            route = JsonUtils.conveterObject(routeRes.getData(), Route.class);

        }
        return route;
    }

    private PriceConfig queryPriceConfigByRouteIdAndTrainType(String routeId, String trainType) {
        String ret = "";
        try {
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://"+function05_URI + "/" + routeId + "/" + trainType)
                    .get()
                    .build();

            // okhttp3.Response response = client.newCall(request).execute();
            okhttp3.Response response = new OkHttpClient.Builder()
            .connectTimeout(60, TimeUnit.SECONDS) //连接超时
            .readTimeout(60, TimeUnit.SECONDS) //读取超时
            .writeTimeout(60, TimeUnit.SECONDS) //写超时
            .build()
            .newCall(request).execute();
            ret = response.body().string();

        } catch (Exception e) {
            e.printStackTrace();
        }
        mResponse priceConfigRes = JsonUtils.json2Object(ret, mResponse.class);

        PriceConfig priceConfig = null;
        if (priceConfigRes.getStatus() == 1) {
            priceConfig = JsonUtils.conveterObject(priceConfigRes.getData(), PriceConfig.class);
        }
        return priceConfig;
    }

}
