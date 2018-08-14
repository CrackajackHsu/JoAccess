# joaccess

## Data Stream
```
+------------------------------------+       +--------------------------------+
|PaaS  A                             |       |             PaaS  B            |
|                                    |       |                                |
|                                    |       |                                |
|                                    |       |                                |
|                                    |       |                                |
+--------+-----+---------------------+       +-------------+-----+------------+
         | WAN |                                           | WAN |
         |     |                                           |     |
         |     |                                           |     |
         |     |                                           |     |
         |     |                                           |     |
         |     |                                           |     |
         |     |                                           |     |
         |     |                                           |     |
+--------+-----v-------+                          +--------+-----+------+
|Adapter A             |                          |   Adapter B         |
|                      |      +-------------------+                     |
|                      |      |                   |                     |
+------------+---------+      |                   +---------------------+
             |                |
             |                |
             |                |
             |                |
             |                |
        +----+----------------+--+                           +---------------+
        |Access                  +---------------------------+               |
        |                        | Serial                    | controller    |
        |                        +---------------------------+               |
        |                        |                           |               |
        |                        |                           +-+-----------+-+
   +----+                        +------------+                |           |
   |    |                        |            |                |           |
   |    +----------+-----------+-+            |          +-----+--+  +-----+---+
   |               |           |              |          | sensor |  | module  |
   |               |           |              |          +--------+  +---------+
   |               |           |              |
   |               |           |              |
+--+-------+  +----+-----+  +--+-------+  +---+------+
|module    |  |sensor    |  |module    |  |sensor    |
|          |  |          |  |          |  |          |
+----------+  +----------+  +----------+  +----------+

```
## Data Request
Access(Client) -> Adapter(Server)

## RESTful
### Connect
#### URL
http://127.0.0.1:8080/access/
#### method
POST
#### sample
- Request 
```
{
    "name":"Access001",
    "callback_url":"http://127.0.0.1:5000/callback", 
    "device":[
        {
            "id":1,
            "type":"TYPEA",
            "name":"NAMEA"
        },
        {
            "id":2,
            "type":"TYPEB",
            "name":"NAMEB"
        }
    ]
}
```
- Response
```
{
    "result":"OK",
    "status":200
}
```

### Publish
#### URL
http://127.0.0.1:8080/access/{name}/device/{id}
#### method
POST
#### sample
- Request 
```
{
   "data":{
      "item1":"value1",
      "item2":"value2"
   },
   "time":"YYYY-MM-DDThh:mm:ss.mmm"
}
```
- Response
```
{
    "result":"OK",
    "status":200
}
```

### Async Execute Result
#### URL
http://127.0.0.1:8080/access/{name}/device/{id}/task/{id}
#### method
PUT
#### sample
- Request 
```
{
   "data":{
      "item1":"value1",
      "item2":"value2"
   },
   "time":"YYYY-MM-DDThh:mm:ss.mmm"
}
```
- Response
```
{
    "result":"OK",
    "status":200
}
```

## Data Callback
Adapter(Client) -> Access(Server)

### Connect ACK
#### URL
http://127.0.0.1:8080/callback/
#### method
PUT
#### sample
- Request 
```
{
    "type":"CONNACK",
    "name":"<ADAPER_NAME>",
    "service":"<SERVICE_NAME>",
    "service_key":"<KEY>",
    "device":[
        {
            "id":1
            "type":"<TYPEA>",
            "alias":"<ALIASA>",
            "last_value":"<111>"
        },
        {
            "id":2
            "type":"<TYPEB>",
            "alias":"<ALIASB>",
            "last_value":"<222>"
        }
    ]
}
```
- Response
```
{
    "type":"CONNACK",
    "result":"OK",
    "status":200
}
```

### Execute
#### URL
http://127.0.0.1:8080/callback/device/{id}
#### method
PUT
#### sample
- Request 
```
{
   "data":{
      "task":1,
      "option":{

      }
   },
   "noblock":false
}
```
- Response (Block Mode)
```
{
    "result":"OK",
    "status":200,
    "device":
    {
        "id":1,
        "result":"OK"
        "errcode":0,
        "option":0,
        "data":1,
        "time":"<YYYY-MM-DDThh:mm:ss.mmm>"
    }
}
```
- Response (NoBlock Mode)
```
{
    "result":"OK",
    "status":200
}
```

# About Access

## Data Stream
```
+-----------------------------------------+
|                         +---------------+                  +---------------+
|                         |               +------------------+               |
|                         |handler        |Serial            | controller    |
|        Access           |               +------------------+               |
|                         +---------------+                  |               |
|                                         |                  +-+-----------+-+
+-----------+ +----------+ +--------------+                    |           |
|           | |          | |              |                    |           |
|handler    | |handler   | |handler       +---+                |           |
|           | |          | |              |   |          +-----+--+  +-----+---+
+--+--------+-+----+-----+-+---+----------+   |          | sensor |  | module  |
   |               |           |              |          +--------+  +---------+
   |               |           |              |
   |               |           |              |
   |               |           |              |
+--+-------+  +----+-----+  +--+-------+  +---+------+
|module    |  |sensor    |  |module    |  |sensor    |
|          |  |          |  |          |  |          |
+----------+  +----------+  +----------+  +----------+
```

### Communication Module
### Master Role
- Access Program
### Slave Role
- Module handler Program
- Sendor handler Program
- Controller handler Program
### Base Protocol
- TCP/IP
#### Master 
TCP Server
#### Slave 
- TCP Client

## Application Protocol
### format
- JSON
### [mount]
- Request
```
{"SLAVE":"Test", "TYPE":"mount", "data":{}}
```
- response
```
{
   "TYPE":"mount",
   "version":"v0.01",
   "errcode":0,
   "result":"OK",
}
```

### [unmount]
- Request
```
{"SLAVE":"Test", "TYPE":"unmount"}
```
- response
```
{
   "TYPE":"unmount",
   "errcode":0,
   "result":"OK",
}
```

### [pull] 
*Only Request/Response Mode*
- Request(hold)
```
{"SLAVE":Test, "TYPE":"poll"}
```
- response
```
{
   "TYPE":"pull",
   "errcode":100,
   "result":"Timeout"
}
```

### [push]
*Keepalive mode only*
- without request
- response
```
{
   "TYPE":"push",
   "errcode":0,
   "result":"OK"
   "data":{}
}
```

### [publish]
- Request
```
{
   "SLAVE":"Test",
   "TYPE":"publish",
   "data":{
      "item1":"value1",
      "item2":"value2"
   }
}
```
- response
```
{
   "TYPE":"publish",
   "errcode":0,
   "result":"OK"
}
```

### [receipt]
- Request
```
{
   "SLAVE":"Test",
   "TYPE":"receipt",
   "data":{
      "item1":"value1",
      "item2":"value2"
   }
}
```
- response
```
{
   "TYPE":"receipt",
   "errcode":0,
   "result":"OK"
}
```

## Slave [publish] Detail
|Slave|Item|DataType|Format|
|:---|:---|:---|:---|
|TEST|value|STRING|-|
|TIME|value|DATE|ISO8601|
|CPUTEMP|value|DOUBLE|%0.2f|
|DHT11|temperature|INT|0 to 50 degrees Celsius with +-2 degrees accuracy|
|DHT11|humidity|INT|20 to 80% with 5% accuracy|

## Slave [pull/push] Detail
|Slave|Item|DataType|Sync|
|:---|:---|:---|:---|
|TEST|value|STRING|-|
|BUZZER|data|OBJECT|async|
|DIGITAL|value|STRING|sync|

- BUZZER e.g.
```
{
   "data":[
      {
         "pos":0,
         "delay":10,
         "ferq":0
      },
      {
         "pos":1,
         "delay":100,
         "ferq":440
      }
   ]
}
```

- DIGITAL e.g.
```
{
   "data":{
      "value":"8.8.8.8."
   }
}
```
