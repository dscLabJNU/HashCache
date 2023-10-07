rm -rf virtualenv
virtualenv virtualenv > /dev/null

source virtualenv/bin/activate

pip install boto3 -i https://pypi.tuna.tsinghua.edu.cn/simple > /dev/null
echo "============ Now build prediction-pipeline workflow ============"
functions=("resize" "predict" "render")
for function in ${functions[@]}
do
    cd $function
    zip -r $function.zip __main__.py > /dev/null
    mv $function.zip ../
    echo "============ build "$function" successful! ============"
    cd ..
    zip -r $function.zip virtualenv/ > /dev/null
done