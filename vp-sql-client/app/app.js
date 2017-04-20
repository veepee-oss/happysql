'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
    'ngRoute',
    'infinite-scroll',
    'myApp.version',
    'myApp.connection',
    'myApp.table',
    'myApp.view'
])

.config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
    $locationProvider.hashPrefix('!');
    $routeProvider
	.when('/tables', {
	    templateUrl: 'views/all_tables.html',
	    controller: 'allTablesCtrl'
	})
        .when('/connection', {
            templateUrl: 'views/connection.html',
            controller: 'ConnectionCtrl'
        })
	.when('/table/:tableName/:id', {
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
	.otherwise({redirectTo: '/connection'});
}]);
