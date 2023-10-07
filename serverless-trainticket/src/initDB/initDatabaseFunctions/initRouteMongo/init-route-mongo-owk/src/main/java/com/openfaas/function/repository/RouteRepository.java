package com.openfaas.function.repository;
import com.openfaas.function.entity.RouteInfo;
import java.util.ArrayList;

public interface RouteRepository {

    boolean init(ArrayList<RouteInfo> routeInfos);

}
