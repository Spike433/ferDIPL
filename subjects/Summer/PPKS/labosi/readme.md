# Setup

1. Download InteliJ to open project
2. clone code and press  ```ctrl+alt+shift+s``` to download JDK 17 
3. [use example 9 (HTTP Server)](https://www.fer.unizg.hr/predmet/ppks/materijali#%23!p_rep_142256!_-220788) to see modifications I made
4. only job of the server is to provide `GET`
method and read coordinates from `lat_long_time.txt`
5. openStreetMap.html is used to consume data from server

## Run server

- httpserver --> PersonsHTTPGetServer (`shift+f10`)

## Run frontend

- just open openStreetMap.html

# Troubleshooting 
## Filter button not working

- change values from `9:07` to `9:15` and then move end or start towards `9:10` to see it in action, otherwise it won't work
