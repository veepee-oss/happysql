'use strict';

angular.module('myApp').

factory('callDB', ['$http', '$q', function($http, $q) {

    return function(method, url, headers, data) {

	return $q(function(resolve, reject) {
	    setTimeout(function() {

		$http({
		    method: method,
		    url: url,
		    headers: headers,
		    data: $.param(data)
		}).then(function successCallback(response) {
		    console.log(response.data);
		    resolve(response.data);
		}, function errorCallback(response) {
		    console.log(response);
		    reject(response)
		});

	    }, 1000);
	});
    };
}]);
