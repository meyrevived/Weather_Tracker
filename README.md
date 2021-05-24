# Weather_Tracker

An application that monitors the weather in several cities.  The name of the cities and their monitored frequency should be define in a configuration file. For each city, the application should invoke a REST API call (based on its own frequency), parse the result  and print it into the console. 

## Details
The following properties are collected and printed: 

- Time (The timestamp of the collected sample) 
- City name 
- Temperature (in Celsius) 
- Wind speed  

The samples occur simultaneously and do not block each other. 
When the current sample’s temperature result is higher or lower than the previous one in X  percent (configurable, see threshold property bellow), a warning message is added to the printout. 

The data should be collected from https://openweathermap.org/ site 

An example of a configuration JSON format file (frequency unit is seconds): 
```json
[ 
{ 
"city_id": 2643743, 
"city_name": "London", 
"frequency": 20, 
“threshold”:10 
}, 
{ 
"city_id": 293397, 
"city_name": "Tel Aviv", 
"frequency": 60, 
“threshold”:2 
} 
] 
```
