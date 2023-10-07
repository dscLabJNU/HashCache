package com.openfaas.function.service;

import com.openfaas.function.repository.TripRepositoryImpl;
import edu.fudan.common.util.JsonUtils;
import edu.fudan.common.util.mResponse;

import com.openfaas.function.entity.*;
import com.openfaas.function.repository.TripRepository;

import com.google.gson.JsonObject;
import com.google.gson.Gson;

import com.google.gson.JsonObject;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;

import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.RequestBody;

import java.util.*;
import java.util.concurrent.TimeUnit;

/**
 * @author fdse
 */
public class TravelServiceImpl implements TravelService {

    private TripRepository repository = new TripRepositoryImpl();
    private OkHttpClient client = new OkHttpClient();

    String success = "Success";
    String noContent = "No Content";

    // String function02_URI = "gateway.openfaas:8080/function/query-for-travel.openfaas-fn";
    String function02_URI = "owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/travel/queryForTravel";

    // String function03_URI = "gateway.openfaas:8080/function/get-route-by-routeid.openfaas-fn";
    String function03_URI = "owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/route/getRouteByRouteId";

    // String function04_URI = "gateway.openfaas:8080/function/get-traintype-by-traintypeid.openfaas-fn";
    String function04_URI = "owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/traintype/getTrainTypeByTrainTypeId";

    // String function06_URI = "gateway.openfaas:8080/function/query-already-sold-orders.openfaas-fn";
    String function06_URI = "owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/order/queryAlreadySoldOrders";

    // String function07_URI = "gateway.openfaas:8080/function/query-for-station-id-by-station-name.openfaas-fn";
    String function07_URI = "owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/stationId/queryForStationIdByStationName";

    // String function08_URI = "gateway.openfaas:8080/function/get-left-ticket-of-interval.openfaas-fn";
    String function08_URI = "owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/ticket/getLeftTicketOfInterval";

    @Override
    public mResponse query(TripInfo info) {
        String startingPlaceName = info.getStartingPlace();
        String endPlaceName = info.getEndPlace();

        String startingPlaceId = queryForStationId(startingPlaceName);
        String endPlaceId = queryForStationId(endPlaceName);


        List<TripResponse> list = new ArrayList<>();

        List<Trip> allTripList = repository.findAll();
        for (Trip tempTrip : allTripList) {
            Route tempRoute = getRouteByRouteId(tempTrip.getRouteId());
            if (tempRoute.getStations().contains(startingPlaceId) &&
                    tempRoute.getStations().contains(endPlaceId) &&
                    tempRoute.getStations().indexOf(startingPlaceId) < tempRoute.getStations().indexOf(endPlaceId)) {
                TripResponse response = getTickets(tempTrip, tempRoute, startingPlaceId, endPlaceId, startingPlaceName, endPlaceName, info.getDepartureTime());
                System.out.println("Iam here 2");
                if (response == null) {
                    return new mResponse<>(0, "No Trip info content", null);
                }
                list.add(response);
            }
        }
        System.out.println("Iam here 1");
        return new mResponse<>(1, success, list);

    }

    private TripResponse getTickets(Trip trip, Route route, String startingPlaceId, String endPlaceId, String startingPlaceName, String endPlaceName, Date departureTime) {

        //Determine if the date checked is the same day and after
        if (!afterToday(departureTime)) {
            return null;
        }

        Travel query = new Travel();
        query.setTrip(trip);
        query.setStartingPlace(startingPlaceName);
        query.setEndPlace(endPlaceName);
        query.setDepartureTime(departureTime);


        String ret = "";
        String json = JsonUtils.object2Json(query);
        Gson gson = new Gson();
        JsonObject jsonObject = gson.fromJson(json, JsonObject.class);
        JsonObject postData = new JsonObject();
        postData.add("__post_data", jsonObject);
        json = gson.toJson(postData);
        try {
            RequestBody body = RequestBody.create(
                    MediaType.parse("application/json"), json);
            System.out.println("Invoking url: "+"http://" + function02_URI);
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://" + function02_URI)
                    .post(body)
                    .build();

            okhttp3.Response response = new OkHttpClient.Builder()
                .connectTimeout(500, TimeUnit.SECONDS) //连接超时
                .readTimeout(500, TimeUnit.SECONDS) //读取超时
                .writeTimeout(500, TimeUnit.SECONDS) //写超时
                .build()
                .newCall(request).execute();
            ret = response.body().string();
        } catch (Exception e) {
            e.printStackTrace();
        }
        mResponse mRes = JsonUtils.json2Object(ret, mResponse.class);
        TravelResult resultForTravel = JsonUtils.conveterObject(mRes.getData(), TravelResult.class);

        // GET request to POST request
        jsonObject = new JsonObject();
        jsonObject.addProperty("travelDate", departureTime+"");
        jsonObject.addProperty("trainNumber", trip.getTripId().toString());
        postData = new JsonObject();
        postData.add("__post_data", jsonObject);
        String travelJson = gson.toJson(postData);
        System.out.println("travelJson: "+travelJson);
        try {
            RequestBody body = RequestBody.create(
                    MediaType.parse("application/json"), travelJson);
            System.out.println("Invoking Url: http://"+function06_URI);
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://" + function06_URI)
                    .post(body)
                    .build();

            okhttp3.Response response = new OkHttpClient.Builder()
                    .connectTimeout(500, TimeUnit.SECONDS) //连接超时
                    .readTimeout(500, TimeUnit.SECONDS) //读取超时
                    .writeTimeout(500, TimeUnit.SECONDS) //写超时
                    .build()
                    .newCall(request).execute();
            ret = response.body().string();
            System.out.println("function06_URI result: "+ret);
        } catch (Exception e){
            e.printStackTrace();
        }

        // try {
        //     System.out.println("Invoking url: "+"http://" + function06_URI + "/" + departureTime + "/" + trip.getTripId().toString());
        //     okhttp3.Request request = new okhttp3.Request.Builder()
        //             .url("http://" + function06_URI + "/" + departureTime + "/" + trip.getTripId().toString())
        //             .get()
        //             .build();

        //     okhttp3.Response response = new OkHttpClient.Builder()
        //             .connectTimeout(60, TimeUnit.SECONDS) //连接超时
        //             .readTimeout(60, TimeUnit.SECONDS) //读取超时
        //             .writeTimeout(60, TimeUnit.SECONDS) //写超时
        //             .build()
        //             .newCall(request).execute();
        //     ret = response.body().string();

        // } catch (Exception e) {
        //     e.printStackTrace();
        // }

        mResponse<SoldTicket> result = JsonUtils.json2Object(ret, mResponse.class);

        TripResponse response = new TripResponse();
        response.setConfortClass(50);
        response.setEconomyClass(50);

        int first = getRestTicketNumber(departureTime, trip.getTripId().toString(),
                startingPlaceName, endPlaceName, SeatClass.FIRSTCLASS.getCode());

        int second = getRestTicketNumber(departureTime, trip.getTripId().toString(),
                startingPlaceName, endPlaceName, SeatClass.SECONDCLASS.getCode());
        response.setConfortClass(first);
        response.setEconomyClass(second);

        response.setStartingStation(startingPlaceName);
        response.setTerminalStation(endPlaceName);

        //Calculate the distance from the starting point
        int indexStart = route.getStations().indexOf(startingPlaceId);
        int indexEnd = route.getStations().indexOf(endPlaceId);
        int distanceStart = route.getDistances().get(indexStart) - route.getDistances().get(0);
        int distanceEnd = route.getDistances().get(indexEnd) - route.getDistances().get(0);
        TrainType trainType = getTrainType(trip.getTrainTypeId());
        //Train running time is calculated according to the average running speed of the train
        int minutesStart = 60 * distanceStart / trainType.getAverageSpeed();
        int minutesEnd = 60 * distanceEnd / trainType.getAverageSpeed();

        Calendar calendarStart = Calendar.getInstance();
        calendarStart.setTime(trip.getStartingTime());
        calendarStart.add(Calendar.MINUTE, minutesStart);
        response.setStartingTime(calendarStart.getTime());
        // TravelServiceImpl.LOGGER.info("[Train Service] calculate time：{}  time: {}", minutesStart, calendarStart.getTime());

        Calendar calendarEnd = Calendar.getInstance();
        calendarEnd.setTime(trip.getStartingTime());
        calendarEnd.add(Calendar.MINUTE, minutesEnd);
        response.setEndTime(calendarEnd.getTime());
        // TravelServiceImpl.LOGGER.info("[Train Service] calculate time：{}  time: {}", minutesEnd, calendarEnd.getTime());

        response.setTripId(new TripId(JsonUtils.conveterObject(result.getData(), SoldTicket.class).getTrainNumber()
        ));
        response.setTrainTypeId(trip.getTrainTypeId());
        response.setPriceForConfortClass(resultForTravel.getPrices().get("confortClass"));
        response.setPriceForEconomyClass(resultForTravel.getPrices().get("economyClass"));

        return response;
    }

    private static boolean afterToday(Date date) {
        Calendar calDateA = Calendar.getInstance();
        Date today = new Date();
        calDateA.setTime(today);

        Calendar calDateB = Calendar.getInstance();
        calDateB.setTime(date);

        if (calDateA.get(Calendar.YEAR) > calDateB.get(Calendar.YEAR)) {
            return false;
        } else if (calDateA.get(Calendar.YEAR) == calDateB.get(Calendar.YEAR)) {
            if (calDateA.get(Calendar.MONTH) > calDateB.get(Calendar.MONTH)) {
                return false;
            } else if (calDateA.get(Calendar.MONTH) == calDateB.get(Calendar.MONTH)) {
                return calDateA.get(Calendar.DAY_OF_MONTH) <= calDateB.get(Calendar.DAY_OF_MONTH);
            } else {
                return true;
            }
        } else {
            return true;
        }
    }

    private TrainType getTrainType(String trainTypeId) {
        String ret = "";
        try {
            System.out.println("Invoking url: "+"http://" + function04_URI + "/" + trainTypeId);
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://" + function04_URI + "/" + trainTypeId)
                    .get()
                    .build();

            okhttp3.Response response = client.newCall(request).execute();
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

    private String queryForStationId(String stationName) {
        String ret = "";
        try {
            System.out.println("Invoking url: "+"http://" + function07_URI + "/" + stationName);
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://" + function07_URI + "/" + stationName)
                    .get()
                    .build();

            okhttp3.Response response = client.newCall(request).execute();
            ret = response.body().string();
            System.out.println("function07_URI res: "+ret);

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

    private Route getRouteByRouteId(String routeId) {
        String ret = "";
        try {
            System.out.println("Invoking url: "+"http://" + function03_URI + "/" + routeId);

            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://" + function03_URI + "/" + routeId)
                    .get()
                    .build();

            okhttp3.Response response = client.newCall(request).execute();
            ret = response.body().string();
            System.out.println("function03_URI ret: "+ret);

        } catch (Exception e) {
            e.printStackTrace();
        }

        mResponse routeRes = JsonUtils.json2Object(ret, mResponse.class);

        Route route1 = new Route();
        if (routeRes.getStatus() == 1) {
            route1 = JsonUtils.conveterObject(routeRes.getData(), Route.class);
        }
        return route1;
    }

    private int getRestTicketNumber(Date travelDate, String trainNumber, String startStationName, String endStationName, int seatType) {
        Seat seatRequest = new Seat();

        String fromId = queryForStationId(startStationName);
        String toId = queryForStationId(endStationName);

        seatRequest.setDestStation(toId);
        seatRequest.setStartStation(fromId);
        seatRequest.setTrainNumber(trainNumber);
        seatRequest.setTravelDate(travelDate);
        seatRequest.setSeatType(seatType);

        String ret = "";
        String json = JsonUtils.object2Json(seatRequest);
        Gson gson = new Gson();
        JsonObject jsonObject = gson.fromJson(json, JsonObject.class);
        JsonObject postData = new JsonObject();
        postData.add("__post_data", jsonObject);
        json = gson.toJson(postData);
        System.out.println(json);
        try {
            RequestBody body = RequestBody.create(
                    MediaType.parse("application/json"), json);
            System.out.println("Invoking url: "+"http://" + function08_URI);
            okhttp3.Request request = new okhttp3.Request.Builder()
                    .url("http://" + function08_URI)
                    .post(body)
                    .build();

            // okhttp3.Response response = client.newCall(request).execute();
            okhttp3.Response response = new OkHttpClient.Builder()
                    .connectTimeout(500, TimeUnit.SECONDS) //连接超时
                    .readTimeout(500, TimeUnit.SECONDS) //读取超时
                    .writeTimeout(500, TimeUnit.SECONDS) //写超时
                    .build()
                    .newCall(request).execute();
            ret = response.body().string();
            System.out.println("function08_URI return: "+ret);
        } catch (Exception e) {
            e.printStackTrace();
        }
        mResponse mRes = JsonUtils.json2Object(ret, mResponse.class);


        return (int) mRes.getData();
    }

}
