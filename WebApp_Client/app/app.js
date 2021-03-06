'use strict';

var env = {};

if (window) {
    Object.assign(env, window.__env);
}

// Declare app level module which depends on views, and components
angular.module('myApp', [
    'ngRoute',
    'infinite-scroll',
    'myApp.version',
    'myApp.connection',
    'myApp.table',
    'myApp.view',
    'myApp.nodes',
    'myApp.procs'
]).

config(['$locationProvider', '$routeProvider', '$httpProvider', function($locationProvider, $routeProvider, $httpProvider) {
    $locationProvider.hashPrefix('!');
    $httpProvider.interceptors.push('my500Detector');
    $routeProvider
        .when('/tables', {
            templateUrl: 'views/all_tables.html',
            controller: 'allTablesCtrl'
        })
        .when('/connection', {
            templateUrl: 'views/connection.html',
            controller: 'ConnectionCtrl'
        })
        .when('/table/:tableName/:guid/:id', {
            templateUrl: 'views/edit.html',
            controller: 'editController'
        })
        .when('/table/:tableName', {
            templateUrl: 'views/table.html',
            controller: 'TableCtrl'
        })
        .when('/views', {
            templateUrl: 'views/all_views.html',
            controller: 'allViewsController'
        })
        .when('/view/:viewName', {
            templateUrl: 'views/view.html',
            controller: 'viewController'
        })
        .when('/error', {
            templateUrl: 'views/error.html'
        })
	.when('/graph', {
	    templateUrl: 'views/d3test.html',
	    controller: 'nodesController'
	})
	.when('/procs', {
	    templateUrl: 'views/all_procs.html',
	    controller: 'allProcsController'
	})
	.when('/proc/:procName', {
	    templateUrl: 'views/proc.html',
	    controller: 'proceduresController'
	})
        .otherwise({redirectTo: '/connection'});
}]).

factory('my500Detector', function($location, $q) {
    return {
        responseError: function(response) {
            if(response.status === 500) {
                $location.path('/error');
                return $q.reject(response);
            }
            else {
                return $q.reject(response);
            }
        }
    };
}).

constant('__env', env);
