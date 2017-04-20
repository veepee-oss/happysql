'use strict';

angular.module('myApp.view', ['ngCookies']).


controller('viewController', ['$scope', '$cookies', '$location', 'callDB', function($scope, $cookies, $location, callDB) {
    $scope.loc = $location.path().replace("/view", "");
    $scope.view = $scope.loc.replace("/", "");
    $scope.error = "";
    $scope.datas = [];

    var token = $cookies.get('token');

    var datasPromise = callDB('GET', "http://localhost:8080" + $scope.loc, {'Authorization': token}, {});
    datasPromise.then(function(data) {
	$scope.datas = data
    }, function(error) {
	$scope.error = error;
    });
}]).

controller('allViewsController', ['$scope', '$cookies', 'callDB', function($scope, $cookies, callDB) {
    $scope.views = [];
    $scope.error = "";

    var token = $cookies.get('token');
    var promise = callDB('GET', "http://localhost:8080/rpc/views", {'Authorization': token}, {});

    promise.then(function(data) {
	$scope.views = data
    }, function(error) {
	$scope.error = error;
    });
}]);

