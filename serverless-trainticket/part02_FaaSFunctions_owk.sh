set -e

buildFunction(){
    func_dir=$1
    runtime=$2
    echo "BUILDING $func_dir..."
    cd $func_dir
    rm -rf .gradle
    owk_function_dir=$(find ./ -name "*owk")
    cd $owk_function_dir
    bash build-action.sh $runtime 2>&1 > /dev/null
    cd ../..
    echo "FINISHED $func_dir"
}


runtime=$1
if [ -z "$runtime" ]; then
    echo "lack of param 'runtime'"
    exit
fi


echo "Part02 FaaS Backend Deployment"
PROJECT_DIR=$(cd $(dirname $0); pwd)
cd src/backend/FaaS/

#### Parallel build
cd Part01/
echo "Part1 function build start"
function_dirs=$(ls)
for func_dir in ${function_dirs[@]}
do   
    buildFunction $func_dir $runtime &
done  
wait
echo "Part1 function build finish"
cd ..

cd Part02/
echo "Part2 function build start"
function_dirs=$(ls)
for func_dir in ${function_dirs[@]}
do   
    buildFunction $func_dir $runtime &
done  
wait
echo "Part2 function build finish"
cd ..

cd Part03/
echo "Part3 function deployment start"
function_dirs=$(ls)
for func_dir in ${function_dirs[@]}
do   
    buildFunction $func_dir $runtime &
done  
wait
echo "Part3 function build finished"
cd ..

#### Uncomment the follwing to open the serial build
# cd getLeftTicketOfInterval/
# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 1/13"

# cd getLeftTripTickets/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 2/13"

# cd getPriceByRouteIdAndTrainType/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 3/13"

# cd getRouteByRouteId/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 4/13"

# cd getRouteByTripId/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 5/13"

# cd getSoldTickets/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 6/13"

# cd getToken/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 7/13"

# cd getTrainTypeByTrainTypeId/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 8/13"

# cd getTrainTypeByTripId/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 9/13"

# cd queryAlreadySoldOrders/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 10/13"

# cd queryConfigEntityByConfigName/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 11/13"

# cd queryForStationIdByStationName/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 12/13"

# cd queryForTravel/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 13/13"

# echo "Part1 function deployment finish"
# cd ..

# cd Part02/
# echo "Part2 function deployment start"

# cd checkSecurity/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 1/10"

# cd checkSecurityAboutOrder/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 2/10"

# cd createNewContacts/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 3/10"

# cd createOrder/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 4/10"

# cd dipatchSeat/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 5/10"

# cd findContactsByAccountId/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 6/10"

# cd getContactsByContactsId/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 7/10"

# cd getTripAllDetailInfo/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 8/10"

# cd getUserByUserId/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 9/10"

# cd preserveTicket/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 10/10"


# echo "Part2 function deployment finish"
# cd ..
# cd Part03/
# echo "Part3 function deployment start"


# cd calculateRefund/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 1/10"

# cd cancelTicket/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 2/10"

# cd createThirdPartyPaymentAndPay/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 3/10"

# cd drawBack/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 4/10"

# cd getOrderById/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 5/10"

# cd getStationIdListByNameList/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 6/10"

# cd modifyOrder/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 7/10"

# cd payForTheOrder/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 8/10"

# cd queryOrdersForRefresh/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 9/10"

# cd saveOrderInfo/

# owk_function_dir=$(find ./ -name "*owk")
# cd $owk_function_dir
# bash build-action.sh >/dev/null
# cd ../..
# echo "FINISHED 10/10"


# echo "Part3 function deployment finish"
# cd $PROJECT_DIR

# echo "Done"