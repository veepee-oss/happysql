'use strict';

angular.module('myApp').

factory('callDB', ['$http', '$q', '__env', function($http, $q, __env) {

    return function(method, url, headers, data) {
        console.log("Headers:", headers);
	return $q(function(resolve, reject) {
	    setTimeout(function() {
		$http({
		    method: method,
		    url: __env.apiUrl + __env.baseUrl + url,
		    // url: url,
		    headers: headers,
		    data: $.param(data)
		}).then(function successCallback(response) {
		    console.log(response);
		    resolve(response);
		}, function errorCallback(response) {
		    console.log(response);
		    reject(response);
		});

	    }, 1000);
	});
    };
}]);
