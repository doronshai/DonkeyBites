#!/bin/bash 
set -x

DT="$(date +%s )"
HUMANDATE="$(date +"%d-%m-%Y-%H-%M" )"
CLIENT=${1}
SCRIPT_HOME="/home/DonkeyBites/instaCharts"

if [ -f ${SCRIPT_HOME}/${CLIENT}_output.log ]; then
  rm -rf ${SCRIPT_HOME}/${CLIENT}_output.log
fi

touch ${SCRIPT_HOME}/${CLIENT}_output.log

#RUN_AGAIN='True'
#while [ "$RUN_AGAIN" == "True" ]
#do
#  python3 /home/InstaPy/get_amount_of_FOLLOWERS_${CLIENT}.py > ${SCRIPT_HOME}/${CLIENT}_output.log 2>&1
#  if grep -Fxq "Traceback" ${SCRIPT_HOME}/${CLIENT}_output.log
#  then
#    RUN_AGAIN=False
#    echo "--- Check was succesful ----"
#  else
#    echo "==== Run again as the output is not valid"
#  fi
#done

python3 /home/InstaPy/get_amount_of_FOLLOWERS_${CLIENT}.py > ${SCRIPT_HOME}/${CLIENT}_output.log 2>&1

FOLLOWING=$(less ${SCRIPT_HOME}/${CLIENT}_output.log  | grep FOLLOW | awk '{print $6}')
FOLLOWERS=$(less ${SCRIPT_HOME}/${CLIENT}_output.log  | grep FOLLOW | awk '{print $10}')

jq --arg DT "$DT" --arg HUMANDATE "$HUMANDATE" --arg FOLLOWERS "$FOLLOWERS" --arg FOLLOWING "$FOLLOWING" '.data.entries[.data.entries| length] |= . + {"Date": $DT, "HumanDate": $HUMANDATE, "Followers": $FOLLOWERS, "Following": $FOLLOWING }' ${SCRIPT_HOME}/${CLIENT}_followers.json > ${SCRIPT_HOME}/${CLIENT}_followers_temp.json

rm -rf ${SCRIPT_HOME}/${CLIENT}_followers.json
mv ${SCRIPT_HOME}/${CLIENT}_followers_temp.json ${SCRIPT_HOME}/${CLIENT}_followers.json

rm -rf ${CLIENT}_index.html
sed -e "s/__CLIENT__/${CLIENT}/" ${SCRIPT_HOME}/INITIAL_index.html > ${SCRIPT_HOME}/${CLIENT}_index.html
mkdir -p /var/www/html/${CLIENT}/
cp -f ${SCRIPT_HOME}/${CLIENT}_index.html /var/www/html/${CLIENT}/index.html

cp -f ${SCRIPT_HOME}/${CLIENT}_followers.json /var/www/html/${CLIENT}/followers.json
