package com.openfaas.function.repository;
import com.openfaas.function.entity.PriceConfig;
import java.util.ArrayList;

public interface PriceConfigRepository {

    boolean init(ArrayList<PriceConfig> priceConfigs);

}
