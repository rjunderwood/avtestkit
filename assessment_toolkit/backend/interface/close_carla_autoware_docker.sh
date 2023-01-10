#!/bin/bash

docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker stop %%
