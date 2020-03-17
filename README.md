# Eclipse Calculator v0.01

## Requirements
- Running with java 8 (oracle version)
- Maven
## Run the service
```
mvn install
cd target
java -jar mission-analysis-1.0-SNAPSHOT-jar-with-dependencies.jar
```
service is going to run on the **port 4567**

## Requests examples
route propagation/eclipses, POST method
```json
{
  "header": {
    "timeStart": "2011-12-01T16:43:45",
    "duration": 86400
  },
  "satellite": {
  
      "type": "keplerian",
      "sma": "7128137.0",
      "ecc": "0.007014455530245822",
      "inc": "98.55",
      "pa": "90.0",
      "raan": "5.191699999999999",
      "lv": "359.93"
    }
}
```


```json
{
  "header": {
    "timeStart": "2011-12-01T16:43:45",	
    "duration": 86400
  },
  "satellite": {
    "type": "cartesian",
    "x": "-6142438.668",
    "y": "3492467.560",
    "z": "-25767.25680",
    "vx": "505.8479685",
    "vy": "942.7809215",
    "vz": "7435.922231"
  }
}
```
The response is an array of sunlight time interval 
response type :
```json
[
    {
        "start": "2011-12-01T18:09:01.455",
        "end": "2011-12-01T18:41:30.556"
    },
    {
        "start": "2011-12-01T19:48:49.577",
        "end": "2011-12-01T20:21:19.340"
    },
    {
        "start": "2011-12-01T21:28:37.701",
        "end": "2011-12-01T22:01:08.124"
    },
    {
        "start": "2011-12-01T23:08:25.826",
        "end": "2011-12-01T23:40:56.908"
    },
    {
        "start": "2011-12-02T00:48:13.954",
        "end": "2011-12-02T01:20:45.692"
    },
    {
        "start": "2011-12-02T02:28:02.083",
        "end": "2011-12-02T03:00:34.476"
    },
    {
        "start": "2011-12-02T04:07:50.214",
        "end": "2011-12-02T04:40:23.260"
    },
    {
        "start": "2011-12-02T05:47:38.347",
        "end": "2011-12-02T06:20:12.044"
    },
    {
        "start": "2011-12-02T07:27:26.481",
        "end": "2011-12-02T08:00:00.828"
    },
    {
        "start": "2011-12-02T09:07:14.618",
        "end": "2011-12-02T09:39:49.612"
    },
    {
        "start": "2011-12-02T10:47:02.756",
        "end": "2011-12-02T11:19:38.396"
    },
    {
        "start": "2011-12-02T12:26:50.896",
        "end": "2011-12-02T12:59:27.180"
    },
    {
        "start": "2011-12-02T14:06:39.038",
        "end": "2011-12-02T14:39:15.964"
    },
    {
        "start": "2011-12-02T15:46:27.181",
        "end": "2011-12-02T16:19:04.748"
    }
]
```
