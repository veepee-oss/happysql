'use strict';

angular.module('myApp.table', ['ngCookies', 'ngclipboard']).controller('TableCtrl', ['$scope', '$cookies', '$location', 'callDB', function ($scope, $cookies, $location, callDB) {
    $scope.loc = $location.path().replace("/table", "");
    $scope.table = $scope.loc.replace("/", "");
    $scope.error = "";
    $scope.datas = [];
    $scope.columns = [];
    $scope.query = "";
    $scope.order = "";
    $scope.reverse = false;
    $scope.loaded = false;
    $scope.guid = "";

    $scope.lastCalls = [];

    $scope.limit = 20;
    $scope.offset = 0;

    $scope.sortBy = function (value) {
        $scope.reverse = !$scope.reverse;
        $scope.sort = value;
        console.log(value);
    };

    $scope.token = $cookies.get('token');
    var columnCall = $scope.table + "/columns";
    var columnPromise = callDB('GET', columnCall, {'Authorization': $scope.token}, {});
    $scope.lastCalls.push("GET " + columnCall);
    columnPromise.then(function (response) {
        $scope.columns = response.data;
        $scope.guid = response.headers('X-Guid');
        if ($scope.guid === '') {
            Materialize.toast('No primary key found. Read Only mode!', 4000);
        }
        console.log($scope.guid);
        if ($scope.loaded === false) {
            $('.preloader-background').delay(1700).fadeOut('slow');
            $('.preloader-wrapper')
                .delay(1700)
                .fadeOut();
            $scope.loaded = true;
        }
    }, function (error) {
        Materialize.toast('You should reauthenticate!', 4000);
    });

    $scope.addMoreItems = function () {
        var call = $scope.table + "?limit=" + $scope.limit + "&offset=" + $scope.offset;
        var datasPromise = callDB('GET', call, {'Authorization': $scope.token}, {});
        $scope.lastCalls.push("GET " + call);
        console.log($scope.lastCalls);
        $scope.offset += $scope.limit;
        datasPromise.then(function (response) {
            if (response.length === 0) {
                $scope.offset -= $scope.limit;
            } else {
                $scope.datas = $scope.datas.concat(response.data);
            }
        }, function (error) {
            $scope.error = error;
            $scope.offset -= $scope.limit;
        });
    };

    $scope.deleteElement = function (index) {
        var a = confirm("Do you really want to delete element with id " + index + "?");
        if (a === false) {
            return;
        }
        var headers = {'Authorization': $scope.token, 'Content-Type': 'application/x-www-form-urlencoded'};
        var data = {};
        data[$scope.guid] = index;
        var call = $scope.table;
        var promise = callDB('DELETE', call, headers, data);
        $scope.lastCalls.push("DELETE " + call);
        promise.then(function (response) {
            Materialize.toast('Object successfully destroyed !', 4000);
        }, function (error) {
            Materialize.toast('Operation failed!', 4000);
        });
    };

}]).controller('allTablesCtrl', ['$scope', '$cookies', 'callDB', function ($scope, $cookies, callDB) {
    $scope.tables = [];
    $scope.error = "";

    var token = $cookies.get('token');
    var call = "tables";
    var promise = callDB('GET', call, {'Authorization': token}, {});

    promise.then(function (response) {
        $scope.tables = response.data;
    }, function (error) {
        Materialize.toast('Operation failed!', 4000);
    });

}]).controller('editController', ['$scope', '$cookies', '$location', 'callDB', function ($scope, $cookies, $location, callDB) {
    $scope.data = {};
    var split = $location.path().split('/');
    $scope.table = split[2];
    $scope.guid = split[3];
    $scope.id = split[4];

    var token = $cookies.get('token');
    var call = $scope.table + "?" + $scope.guid + "=" + $scope.id;
    var promise = callDB('GET', call, {'Authorization': token}, {});
    promise.then(function (response) {
        $scope.data = response.data[0];
        console.log($scope.data);
    }, function (error) {
        Materialize.toast('Operation failed!', 4000);
    });

    $scope.submit = function () {
        console.log($scope.data);
        var headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': $cookies.get('token')
        };

        var call = $scope.table + "/" + $scope.id;
        var promise = callDB('PUT', call, headers, $scope.data);

        promise.then(function (response) {
            Materialize.toast('Object successfully changed !', 4000);
        }, function (error) {
            Materialize.toast('Operation failed!', 4000);
        });
    };
}]);
