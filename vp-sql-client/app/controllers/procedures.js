'use strict';

angular.module('myApp.procs', ['ngCookies']).


controller('proceduresController', ['$scope', '$cookies', '$location', 'callDB', function($scope, $cookies, $location, callDB) {
    $scope.loc = $location.path().replace("/view", "");
    $scope.proc = $scope.loc.replace("/proc/", "");
    $scope.error = "";
    $scope.data = "";

    var token = $cookies.get('token');
    var call = "sp/" + $scope.proc;
    var datasPromise = callDB('GET', call, {'Authorization': token}, {});
    datasPromise.then(function(response) {
        $scope.data = response.data[$scope.proc][0];
	var a = /CREATE/.exec();
	console.log(a);
	console.log(RegExp.$1);
	// console.log(RegExp.$2);
	// if (/CREATE PROCEDURE/i.test($scope.data)) {
	//     console.log("yolo");
	// }
    }, function(error) {
        $scope.error = error;
    });

    $scope.alter = function() {
	var data = {"query": $scope.data};
	call = "sp/new";
	var promise = callDB('POST', call, {'Authorization': token}, data);
	
	promise.then(function(response) {
            Materialize.toast('Update  successful!', 4000);
	}, function(error) {
            $scope.error = error;
	});
    }
}]).

controller('allProcsController', ['$scope', '$cookies', 'callDB', function($scope, $cookies, callDB) {
    $scope.procs = [];
    $scope.error = "";

    var token = $cookies.get('token');
    var call = "sp"
    var promise = callDB('GET', call, {'Authorization': token}, {});

    promise.then(function(response) {
        $scope.procs = response.data.names;
    }, function(error) {
        $scope.error = error;
    });
}]);
