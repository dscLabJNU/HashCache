set -e
echo "Part01 Data Initiation"

cd src/initDB/initDatabaseFunctions/

buildFunction(){
    func_dir=$1
    runtime=$2
    echo "BUILDING $func_dir..."
    cd $func_dir
    owk_function_dir=$(find ./ -name "*owk")
    cd $owk_function_dir
    rm -rf .gradle
    bash build-action.sh $runtime 2>&1 > /dev/null
    cd ../..
    echo "FINISHED $func_dir"
}

runtime=$1
if [ -z "$runtime" ]; then
    echo "lack of param 'runtime'"
    exit
fi

function_dirs=$(ls -d */)
for func_dir in ${function_dirs[@]}
do   
    # buildFunction $func_dir $runtime &
    buildFunction $func_dir $runtime
done  
# wait
echo "Part01 function build finished"


# Function to retry a command up to three times
# If the command fails (returns "Fail"), the script will exit
retry_command() {
    local -r __cmd__="$@"
    local -i __retry__=0

    while ((__retry__ < 3)); do
        output=$($__cmd__)
        if echo "$output" | grep -q "Fail"; then
            echo "Command failed: $__cmd__"
            echo "Retry $__retry__/3"
            ((__retry__++))
            # You may want to sleep for a bit here
            sleep 1
        else
            echo "$output"
            return 0
        fi
    done

    echo "Command failed after 3 attempts: $__cmd__"
    exit 1
}

retry_command "wsk -i action invoke -r /guest/init-security-mongo "
retry_command "wsk -i action invoke -r /guest/init-inside-payment-mongo "
# ========== init-price-mongo ==========
cd ./initPriceMongo/init-price-mongo-owk/
retry_command "bash invoke-action.sh"
cd -
retry_command "wsk -i action invoke -r /guest/init-order-mongo "
# ========== init-station-mongo ==========
cd ./initStationMongo/init-station-mongo-owk/
retry_command "bash invoke-action.sh"
cd -
retry_command "wsk -i action invoke -r /guest/init-payment-mongo "
# ========== init-travel-mongo ==========
cd ./initTravelMongo/init-travel-mongo-owk/
retry_command "bash invoke-action.sh"
cd -
retry_command "wsk -i action invoke -r /guest/init-config-mongo "
retry_command "wsk -i action invoke -r /guest/init-user-mongo "
retry_command "wsk -i action invoke -r /guest/init-train-mongo "
retry_command "wsk -i action invoke -r /guest/init-auth-mongo "
# ========== init-route-mongo-owk ==========
cd ./initRouteMongo/init-route-mongo-owk
retry_command "bash invoke-action.sh"
cd -
retry_command "wsk -i action invoke -r /guest/init-contacts-mongo "
# wait
echo "Done"


# cd initAuthMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-auth-mongo.yml
# cd ..
# echo "FINISHED 1/13"

# cd initConfigMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-config-mongo.yml
# cd ..
# echo "FINISHED 2/13"

# cd initContactsMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-contacts-mongo.yml
# cd ..
# echo "FINISHED 3/13"

# cd initInsidePaymentMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-inside-payment-mongo.yml
# cd ..
# echo "FINISHED 4/13"

# cd initOrderMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-order-mongo.yml
# cd ..
# echo "FINISHED 5/13"

# cd initPaymentMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-payment-mongo.yml
# cd ..
# echo "FINISHED 6/13"

# cd initPriceMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-price-mongo.yml
# cd ..
# echo "FINISHED 7/13"

# cd initRouteMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-route-mongo.yml
# cd ..
# echo "FINISHED 8/13"

# cd initSecurityMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-security-mongo.yml
# cd ..
# echo "FINISHED 9/13"

# cd initStationMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-station-mongo.yml
# cd ..
# echo "FINISHED 10/13"

# cd initTrainMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-train-mongo.yml
# cd ..
# echo "FINISHED 11/13"

# cd initTravelMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-travel-mongo.yml
# cd ..
# echo "FINISHED 12/13"

# cd initUserMongo/
# cp -r $PROJECT_DIR/template ./
# faas-cli up -f init-user-mongo.yml
# cd ..
# echo "FINISHED 13/13"


# echo "DONE"