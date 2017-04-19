'use strict';

// ROW_NUMBER() OVER (ORDER BY ID)

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

    $scope.limit = 50;
    $scope.offset = 0;

    $scope.sortBy = function(value) {
	$scope.reverse = !$scope.reverse;
	$scope.sort = value;
	console.log(value);
    };

    var token = $cookies.get('token');

    var columnPromise = callDB('GET', "http://localhost:8080" + $scope.loc + "/columns", {'Authorization': token}, {});
    columnPromise.then(function(data) {
	$scope.columns = data
    }, function(error) {
	$scope.error = error;
    });

    $scope.addMoreItems = function() {
	var datasPromise = callDB('GET', "http://localhost:8080" + $scope.loc +
				  "?limit=" + $scope.limit + "&offset=" + $scope.offset,
				  {'Authorization': token}, {});
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
    }

    $scope.deleteElement = function(index) {
	var a = confirm("Do you really want to delete element with id " + index + "?");
	if (a === false) {
	    return ;
	}
	var headers = {'Authorization': $scope.token, 'Content-Type': 'application/x-www-form-urlencoded'};
	var data = {'Id': index}
	var promise = callDB('DELETE', "http://localhost:8080/" + $scope.table, headers, data)
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
    $scope.data = {}
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
}]).

controller('viewController', ['$scope', '$cookies', '$location', 'callDB', function($scope, $cookies, $location, callDB) {
    $scope.loc = $location.path().replace("/view", "");
    $scope.view = $scope.loc.replace("/", "");
    $scope.error = "";
    $scope.datas = [];

    var token = $cookies.get('token');

    var datasPromise = callDB('GET', "http://localhost:8080/rpc" + $scope.loc, {'Authorization': token}, {});
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
    var promise = callDB('GET', "http://localhost:8080/views", {'Authorization': token}, {});

    promise.then(function(data) {
	$scope.views = data
    }, function(error) {
	$scope.error = error;
    });
}]);
