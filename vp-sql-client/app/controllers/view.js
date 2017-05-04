'use strict';

angular.module('myApp.view', ['ngCookies']).


controller('viewController', ['$scope', '$cookies', '$location', 'callDB', function($scope, $cookies, $location, callDB) {
    $scope.loc = $location.path().replace("/view", "");
    $scope.view = $scope.loc.replace("/", "");
    $scope.error = "";
    $scope.datas = [];

    var token = $cookies.get('token');
    var call = $scope.view;
    var datasPromise = callDB('GET', call, {'Authorization': token}, {});
    datasPromise.then(function(response) {
        $scope.datas = response.data;
    }, function(error) {
        $scope.error = error;
    });
}]).

controller('allViewsController', ['$scope', '$cookies', 'callDB', function($scope, $cookies, callDB) {
    $scope.views = [];
    $scope.error = "";

    var token = $cookies.get('token');
    var call = "rpc/views";
    var promise = callDB('GET', call, {'Authorization': token}, {});

    promise.then(function(response) {
        $scope.views = response.data;
    }, function(error) {
        $scope.error = error;
    });
}]);
