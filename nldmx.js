/*********************************
解锁部分功能
**************************************


[rewrite_local]
https://api-jiaoyu-brain.vas.lutongnet.com:8887/nldmx-mb-api/nldmx/user/get-free-trial-info url script-response-body https://raw.githubusercontent.com/u188/mon_jd/main/nldmx.js

[mitm]
hostname = api-jiaoyu-brain.vas.lutongnet.com:8887

*************************************/


var obj = JSON.parse($response.body);
obj.data.freeTrialFlag ="true";

$done({ body: JSON.stringify(obj) });