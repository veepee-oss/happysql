'use strict';

angular.module('myApp.table', ['ngCookies']).

controller('TableCtrl', ['$scope', '$cookies', '$location', 'callDB', function($scope, $cookies, $location, callDB) {
    $scope.loc = $location.path().replace("/table", "");
    $scope.table = $scope.loc.replace("/", "");
    $scope.error = "";
    $scope.datas = [];
    $scope.columns = [];
    $scope.query = "";
    $scope.order = "";
    $scope.reverse = false;
    $scope.loaded = false;

    $scope.lastCalls = [];
    
    $scope.limit = 20;
    $scope.offset = 0;

    $scope.sortBy = function(value) {
        $scope.reverse = !$scope.reverse;
        $scope.sort = value;
        console.log(value);
    };

    $scope.token = $cookies.get('token');

    var call = "http://localhost:8080" + $scope.loc + "/columns";
    var columnPromise = callDB('GET', call, {'Authorization': $scope.token}, {});
    $scope.lastCalls.push("GET " + call);
    columnPromise.then(function(data) {
        $scope.columns = data;
        if ($scope.loaded == false) {
            $('.preloader-background').delay(1700).fadeOut('slow');

            $('.preloader-wrapper')
                .delay(1700)
                .fadeOut();
            $scope.loaded = true;
        }

    }, function(error) {
        $scope.error = error;
    });

    $scope.addMoreItems = function() {
	var call = "http://localhost:8080" + $scope.loc + "?limit=" + $scope.limit + "&offset=" + $scope.offset;
        var datasPromise = callDB('GET', call, {'Authorization': $scope.token}, {});
	$scope.lastCalls.push("GET " + call);
	console.log($scope.lastCalls);
        $scope.offset += $scope.limit
        datasPromise.then(function(data) {
            if (data.length === 0) {
                $scope.offset -= $scope.limit
            } else {
                $scope.datas = $scope.datas.concat(data);
            }
        }, function(error) {
            $scope.error = error;
            $scope.offset -= $scope.limit
        });
    };

    $scope.deleteElement = function(index) {
        var a = confirm("Do you really want to delete element with id " + index + "?");
        if (a === false) {
            return ;
        }
        var headers = {'Authorization': $scope.token, 'Content-Type': 'application/x-www-form-urlencoded'};
        var data = {'Id': index}
 	var call = "http://localhost:8080/" + $scope.table;
	var promise = callDB('DELETE', call, headers, data)
	$scope.lastCalls.push("DELETE " + call);
        promise.then(function(data) {
            Materialize.toast('Object successfully destroyed !', 4000);
        }, function(error) {
            Materialize.toast(error, 4000);
        });
    };
}]).

controller('allTablesCtrl', ['$scope', '$cookies','callDB', function($scope, $cookies, callDB) {
    $scope.tables = [];
    $scope.error = "";

    var token = $cookies.get('token');
    var promise = callDB('GET', "http://localhost:8080/tables", {'Authorization': token}, {});

    promise.then(function(data) {
        $scope.tables = data
    }, function(error) {
        $scope.error = error;
    });
}]).

controller('editController', ['$scope', '$cookies', '$location', 'callDB', function($scope, $cookies, $location, callDB) {
    $scope.data = {};
    var split = $location.path().split('/');
    $scope.table = split[2];
    $scope.id = split[3];

    var token = $cookies.get('token');
    var promise = callDB('GET', "http://localhost:8080/" + $scope.table + "?Id=" + $scope.id, {'Authorization': token}, {});
    promise.then(function(data) {
        $scope.data = data[0]
    }, function(error) {
        $scope.error = error;
    });

    $scope.submit = function() {
	console.log($scope.data);
	var headers = {
	    'Content-Type': 'application/x-www-form-urlencoded',
	    'Authorization': $cookies.get('token')
	};

	var promise = callDB('PUT', "http://localhost:8080/" + $scope.table + "/" + $scope.id, headers, $scope.data);

	promise.then(function(data) {
	    Materialize.toast('Object successfully changed !', 4000);
	}, function(error) {
	    Materialize.toast(error, 4000);
	});
    }
}]);
