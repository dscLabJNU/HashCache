package com.openfaas.function.repository;

import com.openfaas.function.entity.Station;

import java.util.ArrayList;


public interface StationRepository {

    boolean init(ArrayList<Station> stations);

}
