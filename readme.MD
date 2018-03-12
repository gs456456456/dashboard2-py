# REST API    

## 开始使用    

REST，即Representational State Transfer的缩写，是目前最流行的一种互联网软件架构。它结构清晰、符合标准、易于理解、扩展方便，正得到越来越多网站的采用。其优点如下：    
- 在RESTful架构中，每一个URL代表一种资源；    
- 客户端和服务器之间，传递这种资源的某种表现层；    
- 客户端通过四个HTTP指令，对服务器端资源进行操作，实现“表现层状态转化”。   

建议开发者使用REST API进行币币交易或者资产提现等操作。    
    
## 请求交互    

REST访问的根URL：`https://www.okex.com/api/v1`     

所有请求基于http的jsonrpc协议,请求头信息中contentType需要统一设置为：`application/json`    
    
    
请求交互说明    
1. 请求参数：根据接口请求参数规定进行参数封装。    
2. 提交请求参数：将封装好的请求参数通过GET或者POST方式提交至服务器。    
3. 服务器响应：服务器首先对用户请求数据进行参数安全校验，通过校验后根据业务逻辑将响应数据以JSON格式返回给用户。    
4. 数据处理：对服务器响应数据进行处理。 

## 请求 
请求放置于http-post的body部分，有以下三个字段：
|参数名|	参数类型|	描述|
| :-----    | :-----   | :-----    | :-----   |
|method|String| API的方法名|
|params|Json Array| API的参数数组，不能为null|
|id|Integer|详细描述看下面*后内容|


* 没有包含“id”成员的请求对象为通知，作为通知的请求对象表明客户端对相应的响应对象并不感兴趣，本身也没有响应对象需要返回给客户端。服务端必须不回复一个通知。
* 如果id成员存在，必须为一个无符号的整形数值，表示本次请求的标识码，远程返回时数据的标识码应该与本次请求标识码相同。

请求示例：
```
{
	"method": "balance.history",
	 "params": [1, "", "",1.511967657e+09,1.5120504e+09,0,100], 
	"id": 123
}
```

## 应答
应答位于"200 ok"的body部分，共有三个参数组成：
|参数名|	参数类型|	描述|
| :-----    | :-----   | :-----    | :-----   |
|result|json object| API调用结果，结果出错时为null|
|error|json object| API调用错误内容，正确时为null|
|id|Integer|Request id|

```
结果正确示例：
{
    "error": null,
    "result": {.....},
    "id": 123
}


结果错误示例：
{
    "error": {
        "code": 1,
        "message": "invalid argument"
    },
    "result": null,
    "id": 123
}
```


## API参考  



System API

System time

示例：

| Request： {    &quot;method&quot;:&quot;server.time&quot;,    &quot;params&quot;:[],    &quot;id&quot;:100}  |
| --- |
| Response:{    &quot;error&quot;:null,    &quot;result&quot;:1511941406,    &quot;id&quot;:100} |



Asset API

用户资产类api，实现针对各种类型用户资产的查询，更新，所有和用户资产相关操作历史记录获取等等。

Asset inquiry

**获取用户资产列表。可以获取特定用户的指定币种资产总额，或者所有币种的资产总额。**

示例：

| Request:{        &quot;method&quot;: &quot;balance.query&quot;,        &quot;params&quot;: [1, &quot;BTC&quot;],        &quot;id&quot;: 123} 或 {        &quot;method&quot;: &quot;balance.query&quot;,        &quot;params&quot;: [1],                                    # 获取user\_id=1的用户所有资产名称资产。        &quot;id&quot;: 123} |
| --- |
| Response:{    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;BTC&quot;: {            &quot;available&quot;: &quot;0&quot;,                                           &quot;freeze&quot;: &quot;0&quot;                                                   }    },    &quot;id&quot;: 1} |



请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| user\_id | Integer | 是 | 用户ID |
| assets | String | 否 | 资产名称，如：&quot;BTC&quot;,&quot;ETH&quot;等。 |

如果只填user\_id，返回该用户的所有资产名称的资产。

返回值：



|  &quot;available&quot;: &quot;0&quot;,                                    # 此币种可用资产数量，以本币种为单位计量。 &quot;freeze&quot;: &quot;0&quot;                                          # 此币种的冻结资产。 |
| --- |

Asset change(用户资产变更)

**更新用户资产列表。比如充值、提现等，都可以改变用户的特定币种资产额。**

示例：

| Request:{    &quot;method&quot;: &quot;balance.update&quot;,     &quot;params&quot;: [1, &quot;BTC&quot;, &quot;deposit&quot;,1, &quot;10.11&quot;, {}],     &quot;id&quot;: 123}   |
| --- |
| Response:{    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;status&quot;: &quot;success&quot;    },    &quot;id&quot;: 123} |

请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| user\_id | Integer | 是 | 用户ID |
| asset | String | 是 | 资产名称，如：&quot;BTC&quot;,&quot;ETH&quot;等。可以为&quot;&quot;，表示所有资产名称。 |
| business | String | 是 | 业务名称，如：&quot;deposit&quot;，&quot;trade&quot;等。可以为&quot;&quot;，表示所有业务名称。&quot;freeze&quot;，表示冻结操作，大于零，表示冻结额度；小于0，表示解冻额度。 |
| business\_id | Integer | 是 | 每一笔变更都要使用新的id提交，如果使用已经用过的id，会返回：&quot;repeat update&quot;，参看下边返回值描述部分。这种重复的情况只针对同一种币种，不同币种是可以有相同id的。不同的用户，针对同一种币种，可以使用相同的business\_id。 |
| change | String | 是 | 资产变更，如果是负数，表示扣除。 |
| detail | Json object | 是 | 附加信息，注意是json object类型！ |



返回值：

| &quot;status&quot;: &quot;success&quot; 如果business\_id使用之前用过的数值，会返回下面错误： {    &quot;method&quot;: &quot;balance.update&quot;,     &quot;params&quot;: [1, &quot;BTC&quot;, &quot;deposit&quot;,3, &quot;10.11&quot;, {}],     &quot;id&quot;: 121}  |
| --- |







Asset history  (用户Asset history)

**获取资产操作历史记录**

示例：

| Request: {    &quot;method&quot;: &quot;balance.history&quot;,     &quot;params&quot;: [1, &quot;USD&quot;, &quot;deposit&quot;,1.511967657e+09,1.5120504e+09,0,100],     &quot;id&quot;: 123}  |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;offset&quot;: 0,        &quot;limit&quot;: 100,        &quot;records&quot;: [            {                &quot;time&quot;: 1511856143.3754101,                &quot;asset&quot;: &quot;USD&quot;,                &quot;business&quot;: &quot;deposit&quot;,                &quot;change&quot;: &quot;100000&quot;,                &quot;balance&quot;: &quot;300000&quot;,                &quot;detail&quot;: {                    &quot;id&quot;: 10003                }            },            {                &quot;time&quot;: 1511856059.013973,                &quot;asset&quot;: &quot;USD&quot;,                &quot;business&quot;: &quot;deposit&quot;,                &quot;change&quot;: &quot;100000&quot;,                &quot;balance&quot;: &quot;200000&quot;,                &quot;detail&quot;: {                    &quot;id&quot;: 10002                }            },            {                &quot;time&quot;: 1511855751.129921,                &quot;asset&quot;: &quot;USD&quot;,                &quot;business&quot;: &quot;deposit&quot;,                &quot;change&quot;: &quot;100000&quot;,                &quot;balance&quot;: &quot;100000&quot;,                &quot;detail&quot;: {                    &quot;id&quot;: 10001                }            }       ]    },    &quot;id&quot;: 123}   |



请求参数：



| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| user\_id | Integer | 是 | 用户ID |
| asset | String | 是 | 资产名称，如：&quot;BTC&quot;,&quot;ETH&quot;等。可以为&quot;&quot;，表示所有资产名称。 |
| business | String | 是 | 业务名称，如：&quot;deposit&quot;，&quot;trade&quot;等。可以为&quot;&quot;，表示所有业务名称。 |
| start\_time | Integer | 是 | 开始时间 |
| end\_time | integer | 是 | 截止时间 |
| offset | integer | 是 | 偏移位置，如果设置为0，表示从最新近一笔业务开始算起，往之前时间的所有交易记录，总笔数不能大于limit；。如果设置为1，表示从次新一笔业务开始算起，往之前时间的所有交易记录总笔数不能大于limit；以此类推..... |
| limit | integer | 是 | 返回的最大交易笔数...... |



返回值：

|  &quot;offset&quot;: 0                 # 偏移位置     &quot;limit&quot;: 100               # 最大数量 &quot;records&quot;:[              # 记录         {            &quot;time&quot;: timestamp,    # 时间戳，业务发生时间。            &quot;asset&quot;: asset,       # 资产名称。            &quot;business&quot;: business, # 业务名称。            &quot;change&quot;: change,     # 资产变更，如果是负数，表示扣除。            &quot;balance&quot;：balance,   # 业务发生后的资产数            &quot;detail&quot;: detail      # 详细信息，json boject        },        ......]  |
| --- |



Asset list 获取平台Asset

**获取平台所有资产类型和精度，prec为精确到小数点后多少位。**

示例：

| Request: { &quot;method&quot;: &quot;asset.list&quot;,  &quot;params&quot;: [],  &quot;id&quot;: 123}  |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: [        {            &quot;name&quot;: &quot;BCH&quot;,            &quot;prec&quot;: 8        },        {            &quot;name&quot;: &quot;BTC&quot;,            &quot;prec&quot;: 6        },        {            &quot;name&quot;: &quot;LTC&quot;,            &quot;prec&quot;: 8        },        ........   ],    &quot;id&quot;: 123}  |



请求参数：（无）



返回值：

| &quot;name&quot;: &quot;LTC&quot;,       # 资产名称&quot;prec&quot;: 8                  # 资产精度，小数点后位数。   |
| --- |



Asset summary

**获取总资产概要。返回平台各种资产的总额。**



示例：

| Request: { &quot;method&quot;: &quot;asset.summary&quot;,  &quot;params&quot;: [&quot;BTC&quot;,&quot;LTC&quot;],  &quot;id&quot;: 123}  |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: [        {            &quot;name&quot;: &quot;BTC&quot;,            &quot;total\_balance&quot;: &quot;6.71592656&quot;,            &quot;available\_count&quot;: 2,            &quot;available\_balance&quot;: &quot;6.71592656&quot;,            &quot;freeze\_count&quot;: 0,            &quot;freeze\_balance&quot;: &quot;0&quot;        },        {            &quot;name&quot;: &quot;LTC&quot;,            &quot;total\_balance&quot;: &quot;0&quot;,            &quot;available\_count&quot;: 0,            &quot;available\_balance&quot;: &quot;0&quot;,            &quot;freeze\_count&quot;: 0,            &quot;freeze\_balance&quot;: &quot;0&quot;        }   ],    &quot;id&quot;: 123}  |





请求参数：



| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| asset list | json array | 否 | 资产名称，如：&quot;BTC&quot;,&quot;ETH&quot;等。如果不填写，表示请求所有资产名称数据。如果币种不存在，返回：&quot;invalid argument&quot; |



返回值：

| &quot;name&quot;: &quot;USD&quot;,&quot;total\_balance&quot;: &quot;1000000&quot;,         # 总资产&quot;available\_count&quot;: 7,                   # &quot;available\_balance&quot;: &quot;976000&quot;,    # 可用资产&quot;freeze\_count&quot;: 1,                   # &quot;freeze\_balance&quot;: &quot;24000&quot;          #冻结资产 |
| --- |



Add Asset

**添加新的资产类型**

method: asset.add\_new

示例：

| Request: {        &quot;method&quot;: &quot;asset.add\_new&quot;,         &quot;params&quot;: [                 &quot;LTC&quot;,                         # &quot;name&quot;:                 20,                              # &quot;prec\_save&quot;:                 8                                 #  &quot;prec\_show:             ],         &quot;id&quot;: 123} Response: {    &quot;error&quot;:null,    &quot;result&quot;:&quot;success&quot;,    &quot;id&quot;:100} |
| --- |



请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| name | string | 是 | 新加资产名，如：&quot;BTC&quot;,&quot;ETH&quot;等。  |
| prec\_save | Integer | 是 | 存储精度（小数点后位数） |
| prec\_show | Integer | 是 | 显示精度（小数点后位数）  |



Trade API

**交易类API，**

Place limit order

**放置限价交易。**

示例：

| Request: { &quot;method&quot;: &quot;order.put\_limit&quot;,  &quot;params&quot;: [1, &quot;BTCUSD&quot;, 1, &quot;10&quot;, &quot;8000&quot;, &quot;0.002&quot;, &quot;0.001&quot;,&quot;&quot;],  &quot;id&quot;: 123}  |
| --- |
| Response: {        &quot;error&quot;: null,        &quot;result&quot;: {        &quot;id&quot;: 1,        &quot;market&quot;: &quot;BTCUSD&quot;,        &quot;source&quot;: &quot;&quot;,        &quot;type&quot;: 1,        &quot;side&quot;: 1,        &quot;user&quot;: 1,        &quot;ctime&quot;: 1512375992.515996,        &quot;mtime&quot;: 1512375992.515996,        &quot;price&quot;: &quot;8000&quot;,        &quot;amount&quot;: &quot;10&quot;,        &quot;taker\_fee&quot;: &quot;0.002&quot;,        &quot;maker\_fee&quot;: &quot;0.001&quot;,        &quot;left&quot;: &quot;10&quot;,        &quot;deal\_stock&quot;: &quot;0&quot;,        &quot;deal\_money&quot;: &quot;0&quot;,        &quot;deal\_fee&quot;: &quot;0&quot;    },    &quot;id&quot;: 123}  |



请求参数：



| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| user\_id | Integer | 是 | 用户ID |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| side | Integer | 是 | 等于1，表示&#39;sell&#39;操作。等于2.，表示&quot;buy&quot;操作。 |
| amount | String | 是 | 申请交易的数量。 |
| price | String | 是 | 交易价格。 |
| taker\_fee | String | 是 | taker手续费 |
| maker\_fee | String | 是 | maker手续费 |
| source | String | 是 |   |



返回值：

| 正确返回：order detail

|         &quot;id&quot;: 1,                                                  # order\_id        &quot;market&quot;: &quot;BTCUSD&quot;,                         # 市场名，matchengine的配置文件里面有配置。        &quot;source&quot;: &quot;&quot;,                                        #         &quot;type&quot;: 1,                                             # 等于1：limit。等于2：market。        &quot;side&quot;: 1,                                              # 等于1，表示&#39;买&#39;交易。        &quot;user&quot;: 1,        &quot;ctime&quot;: 1512375992.515996,        #          &quot;mtime&quot;: 1512375992.515996,       #         &quot;price&quot;: &quot;8000&quot;,                                  # 交易价格。        &quot;amount&quot;: &quot;10&quot;,                                 #         &quot;taker\_fee&quot;: &quot;0.002&quot;,                         #         &quot;maker\_fee&quot;: &quot;0.001&quot;,                       #         &quot;left&quot;: &quot;10&quot;,                                          #         &quot;deal\_stock&quot;: &quot;0&quot;,                               # 出售代币额。        &quot;deal\_money&quot;: &quot;0&quot;,                            #  购买代币额。        &quot;deal\_fee&quot;: &quot;0&quot;                                    #  产生费额。 |
| --- |

 错误返回：（除去基本错误类型）

| code | message | 描述 |
| --- | --- | --- |
| 10 | &quot;balance not enough&quot; | 资产不足。 |
| --- | --- | --- |

  |
| --- |





Place market order

**放置市场交易。**

示例1：卖出操作示例。

| Request: {        &quot;method&quot;: &quot;order.put\_market&quot;,         &quot;params&quot;: [2, &quot;BTCBCC&quot;, 2, &quot;1000&quot;,&quot;0.002&quot;,&quot;&quot;],         &quot;id&quot;: 123} \* 这是一个卖出的操作。 |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;id&quot;: 3,        &quot;market&quot;: &quot;BTCBCC&quot;,        &quot;source&quot;: &quot;&quot;,        &quot;type&quot;: 2,        &quot;side&quot;: 2,        &quot;user&quot;: 2,        &quot;ctime&quot;: 1512441751.935616,        &quot;mtime&quot;: 1512441751.9356339,        &quot;price&quot;: &quot;0&quot;,        &quot;amount&quot;: &quot;1000&quot;,        &quot;taker\_fee&quot;: &quot;0.002&quot;,        &quot;maker\_fee&quot;: &quot;0&quot;,        &quot;left&quot;: &quot;0e-16&quot;,        &quot;deal\_stock&quot;: &quot;0.125&quot;,        &quot;deal\_money&quot;: &quot;1000&quot;,        &quot;deal\_fee&quot;: &quot;0.00025&quot;    },    &quot;id&quot;: 123}  |



示例2：买入操作示例。

| Request: {        &quot;method&quot;: &quot;order.put\_market&quot;,         &quot;params&quot;: [1, &quot;BTCBCC&quot;, 1, &quot;1000&quot;,&quot;0.002&quot;,&quot;&quot;],         &quot;id&quot;: 123} |
| --- |
| Response:如果当前没有足够的卖出者，返回下面错误：{    &quot;error&quot;: {        &quot;code&quot;: 12,        &quot;message&quot;: &quot;no enough trader&quot;    },    &quot;result&quot;: null,    &quot;id&quot;: 123} 但是这个买入申请已经成功挂在系统，如果这时候有卖出者，交易仍然会被撮合。即使每笔卖出的额度不够买入的总额度，交易也会以&quot;分单&quot;的形式被完成。   |



请求参数：



| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| user\_id | Integer | 是 | 用户ID |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| side | Integer | 是 | 等于1，表示&#39;sell&#39;操作。等于2.，表示&quot;buy&quot;操作。 |
| amount | String | 是 | 成交额度。 |
| taker\_fee | String | 是 |   |
| source | String | 是 |   |



返回值：

（参看 &quot;order.put\_limit&quot;方法的返回值）

Cancel order

**取消交易。**

示例：

| Request: {        &quot;method&quot;: &quot;order.cancel&quot;,         &quot;params&quot;: [1, &quot;BTCETH&quot;, 2],         &quot;id&quot;: 123}  |
| --- |
| {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;id&quot;: 27,        &quot;market&quot;: &quot;BTCBCC&quot;,        &quot;source&quot;: &quot;&quot;,        &quot;type&quot;: 1,        &quot;side&quot;: 1,        &quot;user&quot;: 1,        &quot;ctime&quot;: 1512444013.4835889,        &quot;mtime&quot;: 1512444013.4835889,        &quot;price&quot;: &quot;1000&quot;,        &quot;amount&quot;: &quot;10&quot;,        &quot;taker\_fee&quot;: &quot;0.002&quot;,        &quot;maker\_fee&quot;: &quot;0.001&quot;,        &quot;left&quot;: &quot;10&quot;,        &quot;deal\_stock&quot;: &quot;0&quot;,        &quot;deal\_money&quot;: &quot;0&quot;,        &quot;deal\_fee&quot;: &quot;0&quot;    },    &quot;id&quot;: 123}  |

请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| user\_id | Integer | 是 | 用户ID |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| order\_id | Integer | 是 | 要取消交易的id。参看&quot;order.put\_market&quot;和&quot;order.put\_limit&quot;方法的返回结果。 |





返回值：

（正确时，返回order\_detail，参看 &quot;order.put\_limit&quot;方法的返回值）



Order deals（用户）

**获取订单细节。每个订单都对应一个或多个交易，每个交易的信息可以通过这个接口获得。**

这个接口主要是返回交易(deal)的内容

示例：

| Request: {        &quot;method&quot;: &quot;order.deals&quot;,         &quot;params&quot;: [28,0, 100],         &quot;id&quot;: 123}  |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;offset&quot;: 0,        &quot;limit&quot;: 100,        &quot;records&quot;: [            {                &quot;time&quot;: 1512445625.751971,                &quot;user&quot;: 1,                &quot;id&quot;: 25,                &quot;role&quot;: 2,                &quot;price&quot;: &quot;8000&quot;,                &quot;amount&quot;: &quot;0.125&quot;,                &quot;deal&quot;: &quot;1000&quot;,                &quot;fee&quot;: &quot;0.00025&quot;,                &quot;deal\_order\_id&quot;: 2            }       ]    },    &quot;id&quot;: 123}  |

请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| order\_id | Integer | 是 | 交易ID，参看 &quot;order.put\_limit&quot;方法的返回结果。 |
| offset | integer | 是 | 等于0，表示从最近一次交易往之前查找。 |
| limit | Integer | 是 | 最多返回 &quot;records&quot;的数量。 |

返回值：

| 如果order\_id存在，返回交易记录： {                &quot;time&quot;: 1512445625.751971,     # 交易发生时间                &quot;user&quot;: 1,                                # 交易的用户id                &quot;id&quot;: 25,                                  # deal\_id                &quot;role&quot;: 2,                                 # 1.ROLE\_MAKER; 2.ROLE\_TAKER                &quot;price&quot;: &quot;8000&quot;,                        # 交易价格                &quot;amount&quot;: &quot;0.125&quot;,                   # 交易量                &quot;deal&quot;: &quot;1000&quot;,                         # 交易额                &quot;fee&quot;: &quot;0.00025&quot;,                      # 手续费                &quot;deal\_order\_id&quot;: 2                    #             } |
| --- |



Order list （平台）

**获取交易列表。**

示例：

| Request: { &quot;method&quot;: &quot;order.book&quot;,  &quot;params&quot;: [&quot;BTCBCC&quot;,1,0, 100],  &quot;id&quot;: 123}  |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;offset&quot;: 0,        &quot;limit&quot;: 100,        &quot;total&quot;: 1,        &quot;orders&quot;: [            {                &quot;id&quot;: 2,                &quot;market&quot;: &quot;BTCBCC&quot;,                &quot;source&quot;: &quot;&quot;,                &quot;type&quot;: 1,                &quot;side&quot;: 1,                &quot;user&quot;: 1,                &quot;ctime&quot;: 1512440269.446214,                &quot;mtime&quot;: 1512454847.188796,                &quot;price&quot;: &quot;8000&quot;,                &quot;amount&quot;: &quot;10&quot;,                &quot;taker\_fee&quot;: &quot;0.002&quot;,                &quot;maker\_fee&quot;: &quot;0.001&quot;,                &quot;left&quot;: &quot;5.875&quot;,                &quot;deal\_stock&quot;: &quot;4.125&quot;,                &quot;deal\_money&quot;: &quot;33000&quot;,                &quot;deal\_fee&quot;: &quot;33&quot;            }       ]    },    &quot;id&quot;: 123}  |



请求参数：



| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| side | Integer | 是 |   |
| offset | Integer | 是 |   |
| limit | Integer | 是 |   |



返回值：



|                &quot;id&quot;: 2,                &quot;market&quot;: &quot;BTCBCC&quot;,                &quot;source&quot;: &quot;&quot;,                &quot;type&quot;: 1,                                         # 1 --- limit order ;   2 --- market order                &quot;side&quot;: 1,                                           # 1 --- ask         2 --- bid                &quot;user&quot;: 1,                &quot;ctime&quot;: 1512440269.446214,    #put\_order时，创建order时的时间。                &quot;mtime&quot;: 1512454847.188796,                &quot;price&quot;: &quot;8000&quot;,                &quot;amount&quot;: &quot;10&quot;,                &quot;taker\_fee&quot;: &quot;0.002&quot;,                &quot;maker\_fee&quot;: &quot;0.001&quot;,                &quot;left&quot;: &quot;5.875&quot;,                &quot;deal\_stock&quot;: &quot;4.125&quot;,                &quot;deal\_money&quot;: &quot;33000&quot;,                &quot;deal\_fee&quot;: &quot;33&quot;   |
| --- |



Order depth



示例：

| Request: {        &quot;method&quot;: &quot;order.depth&quot;,         &quot;params&quot;: [&quot;BCCBTC&quot;,10,&quot;0&quot;],         &quot;id&quot;: 123}  |
| --- |
| Reponse: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;asks&quot;: [            [                &quot;1000&quot;,                &quot;1&quot;           ]        ],        &quot;bids&quot;: []    },    &quot;id&quot;: 123}  |

请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| limit | Integer | 是 |   |
| interval | String | 是 | 例如：&quot;0&quot;, &quot;0.0001&quot;, &quot;0.001&quot;, &quot;0.01&quot;, &quot;0.1&quot;, &quot;0.5&quot;, &quot;1&quot;, &quot;5&quot;, &quot;10&quot;平台可以设置。 |

返回值：

| &quot;result&quot;: {    &quot;asks&quot;: [        [            &quot;8000.00&quot;,                    # 价格            &quot;9.6250&quot;                       # 量       ]    ],    &quot;bids&quot;: [        [            &quot;7000.00&quot;,            &quot;0.1000&quot;       ]    ]} |
| --- |

Inquire unexecuted orders（用户）

**查询未实施的订单**** 。（ **pending** ：针对特点用户未完成订单查询）**

示例：

| Request: { &quot;method&quot;: &quot;order.pending&quot;,  &quot;params&quot;: [1, &quot;BTCBCC&quot;, 0, 100],  &quot;id&quot;: 123}  |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;limit&quot;: 100,        &quot;offset&quot;: 0,        &quot;total&quot;: 1,        &quot;records&quot;: [            {                &quot;id&quot;: 2,                                 # 这是 order\_id                &quot;market&quot;: &quot;BTCBCC&quot;,                &quot;source&quot;: &quot;&quot;,                &quot;type&quot;: 1,                &quot;side&quot;: 1,                &quot;user&quot;: 1,                &quot;ctime&quot;: 1512440269.446214,                &quot;mtime&quot;: 1512454847.188796,                &quot;price&quot;: &quot;8000&quot;,                &quot;amount&quot;: &quot;10&quot;,                &quot;taker\_fee&quot;: &quot;0.002&quot;,                &quot;maker\_fee&quot;: &quot;0.001&quot;,                &quot;left&quot;: &quot;5.875&quot;,                &quot;deal\_stock&quot;: &quot;4.125&quot;,                &quot;deal\_money&quot;: &quot;33000&quot;,                &quot;deal\_fee&quot;: &quot;33&quot;            }       ]    },    &quot;id&quot;: 123}  |



请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| user\_id | Integer | 是 |   |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| offset | Integer | 是 | 偏移位置，如果设置为0，表示从最新一个订单开始算起，往之前时间的所有交易记录，总笔数不能大于limit；。如果设置为1，表示从次新一个订单开始算起，往之前时间的所有订单记录，总数不能大于limit；以此类推..... |
| limit | Integer | 是 |   |



返回值：



| 返回没有实施订单的order detail记录。 |
| --- |



Unexecuted order details

**查询未实施订单细节。（pending\_detail：针对特定order\_id订单的查询）**

示例：

| Request: { &quot;method&quot;: &quot;order.pending\_detail&quot;,  &quot;params&quot;: [&quot;BTCBCC&quot;,2],  &quot;id&quot;: 123}   |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;id&quot;: 2,        &quot;market&quot;: &quot;BTCBCC&quot;,        &quot;source&quot;: &quot;&quot;,        &quot;type&quot;: 1,        &quot;side&quot;: 1,        &quot;user&quot;: 1,        &quot;ctime&quot;: 1512440269.446214,        &quot;mtime&quot;: 1512454847.188796,        &quot;price&quot;: &quot;8000&quot;,        &quot;amount&quot;: &quot;10&quot;,        &quot;taker\_fee&quot;: &quot;0.002&quot;,        &quot;maker\_fee&quot;: &quot;0.001&quot;,        &quot;left&quot;: &quot;5.875&quot;,        &quot;deal\_stock&quot;: &quot;4.125&quot;,        &quot;deal\_money&quot;: &quot;33000&quot;,        &quot;deal\_fee&quot;: &quot;33&quot;    },    &quot;id&quot;: 123}  |





请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| order\_id | Integer | 是 | 所要查询的订单id |



返回值：



| 返回没有实施订单的order detail记录。 |
| --- |





Inquire executed orders

**查询某个用户的已完成订单。 （某个用户在某个时间段的完成订单）**



示例：

| Request: {        &quot;method&quot;: &quot;order.finished&quot;,         &quot;params&quot;: [1, &quot;BTCBCC&quot;,1.511967657e+09,1.5190504e+09, 0, 100, 2],         &quot;id&quot;: 123}  |
| --- |
| Reponse: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;offset&quot;: 0,        &quot;limit&quot;: 100,        &quot;records&quot;: [            {                &quot;id&quot;: 29,                &quot;ctime&quot;: 1512454847.1887879,                &quot;ftime&quot;: 1512454847.188796,                &quot;user&quot;: 1,                &quot;market&quot;: &quot;BTCBCC&quot;,                &quot;source&quot;: &quot;&quot;,                &quot;type&quot;: 1,                &quot;side&quot;: 2,                &quot;price&quot;: &quot;8000&quot;,                &quot;amount&quot;: &quot;1&quot;,                &quot;taker\_fee&quot;: &quot;0.002&quot;,                &quot;maker\_fee&quot;: &quot;0.001&quot;,                &quot;deal\_stock&quot;: &quot;1&quot;,                &quot;deal\_money&quot;: &quot;8000&quot;,                &quot;deal\_fee&quot;: &quot;0.002&quot;            },            {                &quot;id&quot;: 28,                &quot;ctime&quot;: 1512445625.7519591,                &quot;ftime&quot;: 1512445625.751971,                &quot;user&quot;: 1,                &quot;market&quot;: &quot;BTCBCC&quot;,                &quot;source&quot;: &quot;&quot;,                &quot;type&quot;: 2,                &quot;side&quot;: 2,                &quot;price&quot;: &quot;0&quot;,                &quot;amount&quot;: &quot;1000&quot;,                &quot;taker\_fee&quot;: &quot;0.002&quot;,                &quot;maker\_fee&quot;: &quot;0&quot;,                &quot;deal\_stock&quot;: &quot;0.125&quot;,                &quot;deal\_money&quot;: &quot;1000&quot;,                &quot;deal\_fee&quot;: &quot;0.00025&quot;            }       ]    },    &quot;id&quot;: 123}  |



请求参数：



| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| user\_id | Integer | 是 | 用户ID |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| start\_time | Integer | 是 | 开始时间。 |
| end\_time | Integer | 是 | 截止时间。 |
| offset | Integer | 是 | 偏移位置，如果设置为0，表示从最新一个订单开始算起，往之前时间的所有交易记录，总笔数不能大于limit；。如果设置为1，表示从次新一个订单开始算起，往之前时间的所有满足条件订单记录，总数不能大于limit；以此类推..... |
| limit | Integer | 是 |   |
| side | Integer | 是 | 等于1，表示&#39;卖&#39;操作。等于2.，表示买操作。 |





返回值：



| 返回已经执行订单的order details。 |
| --- |



Executed order details

**已完成订单详情。（针对某个order\_id的已完成订单查询）**

示例：



| Request: {        &quot;method&quot;: &quot;order.finished\_detail&quot;,         &quot;params&quot;: [28],         &quot;id&quot;: 123}   |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;id&quot;: 28,        &quot;ctime&quot;: 1512445625.7519591,        &quot;ftime&quot;: 1512445625.751971,        &quot;user&quot;: 1,        &quot;market&quot;: &quot;BTCBCC&quot;,        &quot;source&quot;: &quot;&quot;,        &quot;type&quot;: 2,        &quot;side&quot;: 2,        &quot;price&quot;: &quot;0&quot;,        &quot;amount&quot;: &quot;1000&quot;,        &quot;taker\_fee&quot;: &quot;0.002&quot;,        &quot;maker\_fee&quot;: &quot;0&quot;,        &quot;deal\_stock&quot;: &quot;0.125&quot;,        &quot;deal\_money&quot;: &quot;1000&quot;,        &quot;deal\_fee&quot;: &quot;0.00025&quot;    },    &quot;id&quot;: 123}  |



请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| order\_id | Integer | 是 | 所要查询的已完成订单order\_id |





返回值：



| 返回指定已完成订单的order detail记录。 |
| --- |







Market API

Market price

**获取指定market的price。**



示例：



| Request: {        &quot;method&quot;: &quot;market.last&quot;,         &quot;params&quot;: [&quot;BTCBCC&quot;],         &quot;id&quot;: 123}  |
| --- |
| Response:  {    &quot;error&quot;: null,    &quot;result&quot;: &quot;8000.00000000&quot;,    &quot;id&quot;: 123}  |



请求参数：



| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| market | String | 否 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |



返回值：



|  &quot;result&quot;: &quot;8000.00000000&quot;,                               # price |
| --- |





Executed history

**market的交易记录。（平台）**

示例：

| Request: {        &quot;method&quot;: &quot;market.deals&quot;,         &quot;params&quot;: [&quot;BTCBCC&quot;,3,0],         &quot;id&quot;: 123} \* 请求BTCBCC最近三次交易。  |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: [        {            &quot;id&quot;: 26,            &quot;time&quot;: 1512454847.188796,            &quot;price&quot;: &quot;8000&quot;,            &quot;amount&quot;: &quot;1&quot;,            &quot;type&quot;: &quot;buy&quot;        },        {            &quot;id&quot;: 25,            &quot;time&quot;: 1512445625.751971,            &quot;price&quot;: &quot;8000&quot;,            &quot;amount&quot;: &quot;0.125&quot;,            &quot;type&quot;: &quot;buy&quot;        },        {            &quot;id&quot;: 24,            &quot;time&quot;: 1512442938.956193,            &quot;price&quot;: &quot;8000&quot;,            &quot;amount&quot;: &quot;0.125&quot;,            &quot;type&quot;: &quot;buy&quot;        }   ],    &quot;id&quot;: 123}   |

请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| limit | Integer | 是 | 返回最多交易数据数量。 |
| last\_id | Integer | 是 | 返回大于order\_id &gt; last\_id的交易数据。 |



返回值：



|    {            &quot;id&quot;: 24,                                  #  order\_id            &quot;time&quot;: 1512442938.956193,     #  order发生的时间。            &quot;price&quot;: &quot;8000&quot;,                       # 交易价格。            &quot;amount&quot;: &quot;0.125&quot;,                  # 交易量。            &quot;type&quot;: &quot;buy&quot;                          # 交易类型。        }  |
| --- |



User Executed history

**用户交易记录。（用户）**

示例：



| Request: { &quot;method&quot;: &quot;market.user\_deals&quot;,  &quot;params&quot;: [1,&quot;BTCBCC&quot;,0,3],  &quot;id&quot;: 123}   |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;offset&quot;: 0,        &quot;limit&quot;: 3,        &quot;records&quot;: [            {                &quot;time&quot;: 1512454847.188796,                &quot;user&quot;: 1,                &quot;id&quot;: 26,                &quot;side&quot;: 2,                &quot;role&quot;: 2,                &quot;price&quot;: &quot;8000&quot;,                &quot;amount&quot;: &quot;1&quot;,                &quot;deal&quot;: &quot;8000&quot;,                &quot;fee&quot;: &quot;0.002&quot;,                &quot;deal\_order\_id&quot;: 2            },            {                &quot;time&quot;: 1512454847.188796,                &quot;user&quot;: 1,                &quot;id&quot;: 26,                &quot;side&quot;: 1,                &quot;role&quot;: 1,                &quot;price&quot;: &quot;8000&quot;,                &quot;amount&quot;: &quot;1&quot;,                &quot;deal&quot;: &quot;8000&quot;,                &quot;fee&quot;: &quot;8&quot;,                &quot;deal\_order\_id&quot;: 29            },            {                &quot;time&quot;: 1512445625.751971,                &quot;user&quot;: 1,                &quot;id&quot;: 25,                &quot;side&quot;: 2,                &quot;role&quot;: 2,                &quot;price&quot;: &quot;8000&quot;,                &quot;amount&quot;: &quot;0.125&quot;,                &quot;deal&quot;: &quot;1000&quot;,                &quot;fee&quot;: &quot;0.00025&quot;,                &quot;deal\_order\_id&quot;: 2            }       ]    },    &quot;id&quot;: 123}  |





请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| user\_id | Integer | 是 | 用户id |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。如果使用不存在的market name，&quot;records&quot;为： [] |
| offset | Integer | 是 | 偏移位置，如果设置为0，表示从最新一个订单开始算起，往之前时间的所有交易记录，总笔数不能大于limit；如果设置为1，表示从次新一个订单开始算起，往之前时间的所有满足条件订单记录，总数不能大于limit；以此类推..... |
| limit | Integer | 是 | 返回最多交易数据数量。 |



返回值：



|              {                &quot;time&quot;: 1512454847.188796,       #  order产生时间。                &quot;user&quot;: 1,                                          #  user\_id                &quot;id&quot;: 26,                                            #  Executed ID                &quot;side&quot;: 1,                                           # side，1：sell，2：buy                &quot;role&quot;: 1,                                           # role，1：Maker, 2: Taker                &quot;price&quot;: &quot;8000&quot;,                &quot;amount&quot;: &quot;1&quot;,                &quot;deal&quot;: &quot;8000&quot;,                &quot;fee&quot;: &quot;8&quot;,                &quot;deal\_order\_id&quot;: 29            },  |
| --- |



KLine

**获取K线数据，可以设定起止时间和采样周期。**

示例：

| Request: { &quot;method&quot;: &quot;market.kline&quot;,  &quot;params&quot;: [&quot;BTCBCC&quot;,1512449633,1512469633,30],  &quot;id&quot;: 123}   |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: [        [            1512449610,            &quot;8000&quot;,            &quot;8000&quot;,            &quot;8000&quot;,            &quot;8000&quot;,            &quot;0&quot;,            &quot;0&quot;,            &quot;BTCBCC&quot;       ],        [            1512449640,            &quot;8000&quot;,            &quot;8000&quot;,            &quot;8000&quot;,            &quot;8000&quot;,            &quot;0&quot;,            &quot;0&quot;,            &quot;BTCBCC&quot;       ]     ......    ],    &quot;id&quot;: 123}  |



请求参数：



| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| start\_time | Integer | 是 | 开始时间。 |
| end\_time | Integer | 是 | 截止时间。 |
| Interval | Integer | 是 | 获取数据周期，每个周期获取一次数据。 |



返回值：

|     &quot;result&quot;: [        [            1512316800,        # 时间            &quot;8000&quot;,                  # open            &quot;8000&quot;,                  # close            &quot;8000&quot;,                  # highest            &quot;8000&quot;,                  # lowest            &quot;4.125&quot;,                 # volume            &quot;33000&quot;,                # amount            &quot;BTCBCC&quot;              # market name       ]    ]  |
| --- |



Market status

**获取过去指定时间段market当前最新涨跌幅，交易量，最高/最低价格等状态。**

示例：



| Request: { &quot;method&quot;: &quot;market.status&quot;,  &quot;params&quot;: [&quot;BTCBCC&quot;,12000],  &quot;id&quot;: 123}   |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;period&quot;: 12000,        &quot;last&quot;: &quot;8000&quot;,        &quot;open&quot;: &quot;8000&quot;,        &quot;close&quot;: &quot;8000&quot;,        &quot;high&quot;: &quot;8000&quot;,        &quot;low&quot;: &quot;8000&quot;,        &quot;volume&quot;: &quot;1&quot;    },    &quot;id&quot;: 123}  |



请求参数：



| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |
| period | Integer | 是 | 查询周期，以秒为单位。即从现在开始往前推的时间，例如：86400，是过去24小时。 |

返回值：

|  &quot;result&quot;: {        &quot;period&quot;: 12000,           #  查询周期，即从现在开始往前推的时间。        &quot;last&quot;: &quot;8000&quot;,              #  最后price        &quot;open&quot;: &quot;8000&quot;,        &quot;close&quot;: &quot;8000&quot;,        &quot;high&quot;: &quot;8000&quot;,             #  最高值        &quot;low&quot;: &quot;8000&quot;,              #  最低值        &quot;volume&quot;: &quot;1&quot;    }, |
| --- |





Market status today

**获取今天market状态。**

示例：



| Request: {         &quot;method&quot;: &quot;market.status\_today&quot;,         &quot;params&quot;: [&quot;BTCBCC&quot;],         &quot;id&quot;: 123}  |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: {        &quot;open&quot;: &quot;8000&quot;,        &quot;last&quot;: &quot;8000&quot;,        &quot;high&quot;: &quot;8000&quot;,        &quot;low&quot;: &quot;8000&quot;,        &quot;volume&quot;: &quot;4.125&quot;,        &quot;deal&quot;: &quot;33000&quot;    },    &quot;id&quot;: 123}  |



请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| market | String | 是 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot; |

返回值：



| 参看 &quot;market.status&quot;方法的返回值。 |
| --- |



Market list

**获取market列表。**

示例：

| Request: { &quot;method&quot;: &quot;market.list&quot;,  &quot;params&quot;: [],  &quot;id&quot;: 123}  |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: [        {            &quot;name&quot;: &quot;DASHBCC&quot;,            &quot;stock&quot;: &quot;BCC&quot;,            &quot;money&quot;: &quot;DASH&quot;,            &quot;fee\_prec&quot;: 4,            &quot;stock\_prec&quot;: 8,            &quot;money\_prec&quot;: 8,            &quot;min\_amount&quot;: &quot;0.0001&quot;        },        {            &quot;name&quot;: &quot;ETHBCC&quot;,            &quot;stock&quot;: &quot;BCC&quot;,            &quot;money&quot;: &quot;ETH&quot;,            &quot;fee\_prec&quot;: 4,            &quot;stock\_prec&quot;: 8,            &quot;money\_prec&quot;: 8,            &quot;min\_amount&quot;: &quot;0.0001&quot;        },        ..........        {            &quot;name&quot;: &quot;BTCETH&quot;,            &quot;stock&quot;: &quot;ETH&quot;,            &quot;money&quot;: &quot;BTC&quot;,            &quot;fee\_prec&quot;: 4,            &quot;stock\_prec&quot;: 0,            &quot;money\_prec&quot;: 0,            &quot;min\_amount&quot;: &quot;1&quot;        }   ],    &quot;id&quot;: 123}  |



请求参数：（无）

返回值：



|          {            &quot;name&quot;: &quot;DASHBCC&quot;,            #  market name            &quot;stock&quot;: &quot;BCC&quot;,                     #  卖方使用代币。            &quot;money&quot;: &quot;DASH&quot;,                 #  买方使用代币。            &quot;fee\_prec&quot;: 4,                        #  手续费精度。            &quot;stock\_prec&quot;: 8,                     #  卖方代币的最大操作精度，小数点后8位。            &quot;money\_prec&quot;: 8,                   #             &quot;min\_amount&quot;: &quot;0.0001&quot;          #  最少的交易数量。        }, |
| --- |



Market summary

**market概要。**

示例：



| Request: { &quot;method&quot;: &quot;market.summary&quot;,  &quot;params&quot;: [&quot;BTCBCC&quot;,&quot;DASHETH&quot;],  &quot;id&quot;: 123}  |
| --- |
| Response: {    &quot;error&quot;: null,    &quot;result&quot;: [        {            &quot;name&quot;: &quot;BTCBCC&quot;,            &quot;ask\_count&quot;: 1,            &quot;ask\_amount&quot;: &quot;5.875&quot;,            &quot;bid\_count&quot;: 0,            &quot;bid\_amount&quot;: &quot;0&quot;        },        {            &quot;name&quot;: &quot;DASHETH&quot;,            &quot;ask\_count&quot;: 0,            &quot;ask\_amount&quot;: &quot;0&quot;,            &quot;bid\_count&quot;: 0,            &quot;bid\_amount&quot;: &quot;0&quot;        }   ],    &quot;id&quot;: 123}  |



请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| markets | String | 否 | market名称，如：&quot;BTCUSD&quot;,&quot;BCCUSD&quot;等。这些名称必须在后台matchengine的配置文件里面配置过，否则返回：&quot;invalid argument&quot;如果不填，返回所有market。 |



返回值：



|         {            &quot;name&quot;: &quot;DASHETH&quot;,            &quot;ask\_count&quot;: 0,            &quot;ask\_amount&quot;: &quot;0&quot;,            &quot;bid\_count&quot;: 0,            &quot;bid\_amount&quot;: &quot;0&quot;        } |
| --- |



Add Market

**添加新的market**

method: market.add\_new

示例：

| Request: {        &quot;method&quot;: &quot;market.add\_new&quot;,         &quot;params&quot;: [                 &quot;BTCBCH&quot;,                               # 市场名                {                                                # &quot;stock&quot;:                    &quot;name&quot;: &quot;BTC&quot;,                       # 货品的资产名                    &quot;prec&quot;: 8                                 # 精度（小数点后位数）                },                {                                                # &quot;money&quot;:                    &quot;name&quot;: &quot;BCH&quot;,                       # 货币的资产名                    &quot;prec&quot;: 8                                 # 精度（小数点后位数）                },               &quot;0.001&quot;                                        # &quot;min\_amount&quot;:              ],         &quot;id&quot;: 123} Response: {    &quot;error&quot;:null,    &quot;result&quot;:&quot;success&quot;,    &quot;id&quot;:100} |
| --- |



请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| name | string | 是 | 新加市场名，如：&quot;BTCETH&quot;等。  |
| stock |   | 是 | 货物（交易对象） 内容看示例标注 |
| money  |   | 是 | 货币（交易使用货币） 内容看示例标注 |





market refresh

method: market.refresh

**添加新的market后，需要调用这个方法，刷新更新内容。**

示例：



| Request: {        &quot;method&quot;: &quot;market.refresh&quot;,         &quot;params&quot;: [&quot;BTCBCH&quot;],         &quot;id&quot;: 123} Response: {    &quot;error&quot;:null,    &quot;result&quot;:&quot;success&quot;,    &quot;id&quot;:100} |
| --- |



请求参数：

| 参数名 | 参数类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| name | string | 是 | 新加市场名，如：&quot;BTCETH&quot;等。  |
