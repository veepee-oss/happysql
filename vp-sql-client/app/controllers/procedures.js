'use strict';

angular.module('myApp.procs', ['ngCookies']).


controller('proceduresController', ['$scope', '$cookies', '$location', 'callDB', function($scope, $cookies, $location, callDB) {
    $scope.loc = $location.path().replace("/view", "");
    $scope.proc = $scope.loc.replace("/proc/", "");
    $scope.error = "";
    $scope.datas = [];

    var token = $cookies.get('token');
    var call = "sp/" + $scope.proc;
    var datasPromise = callDB('GET', call, {'Authorization': token}, {});
    datasPromise.then(function(response) {
        $scope.datas = response.data[$scope.proc];
    }, function(error) {
        $scope.error = error;
    });
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
