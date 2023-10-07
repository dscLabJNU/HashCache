package com.openfaas.function.repository;
import com.openfaas.function.entity.TravelInfo;
import java.util.ArrayList;


public interface TripRepository {

    boolean init(ArrayList<TravelInfo> travelInfos);

}
