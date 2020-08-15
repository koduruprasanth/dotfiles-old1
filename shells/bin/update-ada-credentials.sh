#!/bin/bash

# https://stackoverflow.com/questions/10909685/run-parallel-multiple-commands-at-once-in-the-same-terminal 
trap 'pkill -f "ada credentials update";' SIGINT

ada credentials update --account=209816743619 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=fi-data &
sleep 1 && ada credentials update --account=561812104925 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=fi-devo &
sleep 2 && ada credentials update --account=951099399227 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=fi-prod &
sleep 3 && ada credentials update --account=281425087367 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=ramp-devo &
sleep 4 && ada credentials update --account=201167857541 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=ramp-prod &
sleep 5 && ada credentials update --account=026332220731 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=octopus-devo &
sleep 6 && ada credentials update --account=849081402005 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=octopus-prod &
sleep 7 && ada credentials update --account=706072150461 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=secant-devo &
sleep 8 && ada credentials update --account=749754612141 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=secant-prod &
sleep 9 && ada credentials update --account=631288310615 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=fdap-devo &
sleep 10 && ada credentials update --account=006122757773 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=fdap-prod &
sleep 11 && ada credentials update --account=029040851679 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=alterra-devops &
sleep 12 && ada credentials update --account=651197184252 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=alterra-prod &
sleep 13 && ada credentials update --account=902354312862 --provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --profile=alterra-devo 
