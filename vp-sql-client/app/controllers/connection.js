/**
 * Created by Anis Bennabi on 12/04/2017.
 */
'use strict';

angular.module('myApp.connection', ['ngCookies'])

    .controller('ConnectionCtrl', ['$scope', '$cookies', 'callDB', function($scope, $cookies, callDB) {
        $scope.user = '';
        $scope.password = '';
        $scope.server = '';
        $scope.dbname = '';

        // Post token
        $scope.getToken = function() {
            console.log($scope.user);
            var data = {
                user: $scope.user,
                password: $scope.password,
                dbname: $scope.dbname,
                server: $scope.server
            };
	    var call = "change_credz";
            var promise = callDB('POST', call, {'Content-Type': 'application/x-www-form-urlencoded'}, data);
            promise.then(function(response) {
                $scope.datas = response.data;
                $scope.user = '';
                $scope.password = '';
                $scope.server = '';
                $scope.dbname = '';
                $cookies.put('token', $scope.datas.token);
                Materialize.toast('Connection  successful!', 4000);
            }, function(error) {
                $scope.error = error;
                Materialize.toast('Connection failed!', 4000);
            });
        };

    }]);
