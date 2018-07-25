CACHE=perceval-init
RAW2FILE=./raw2file.py
ES="http://bitergia:bitergia@172.17.0.1:9200"
echo Using $ES as the Elasticsearch endpoint. Adjust it to your endpoint.
$RAW2FILE -g  -p -e $ES -i test_google_hits-raw -f $CACHE/raw/google_hits6.json
$RAW2FILE -g  -p -e $ES -i test_apache-raw -f $CACHE/raw/apache6.json
$RAW2FILE -g  -p -e $ES -i test_twitter-raw -f $CACHE/raw/twitter6.json
$RAW2FILE -g  -p -e $ES -i test_remo_activities-raw -f $CACHE/raw/remo_activities6.json
