Router.configure({
	layoutTemplate: 'main_layout'
});


Router.map(function(){
	this.route('home', {
		path: '/',
		template: 'home'
	})
	this.route('postdata', {
		path: '/postdata',
		template: 'postdata'
	})

	this.route('listdata', {
		path: '/listdata',
		template: 'listdata'
	})

	this.route('listalldata', {
		path: '/listalldata',
		template: 'listalldata'
	})

	this.route('search', {
		path: '/search',
		template: 'search'
	})

	this.route('searchquery', {
		path: '/searchquery',
		template: 'searchquery'
	})
})