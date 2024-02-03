/*********************************
解锁部分功能
**************************************


[rewrite_local]
https://api-jiaoyu-brain.vas.lutongnet.com:8887/nldmx-mb-api/nldmx/user/get-user url script-response-body https://raw.githubusercontent.com/u188/mon_jd/main/nldmx.js

[mitm]
hostname = api-jiaoyu-brain.vas.lutongnet.com:8887

*************************************/


var obj = JSON.parse($response.body);
obj.data.orderStatus ="true";
obj.data.nickname ="ttt";

$done({ body: JSON.stringify(obj) });