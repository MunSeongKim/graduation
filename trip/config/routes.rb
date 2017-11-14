Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html

	root 'test#index'
#	root 'trip#index'
#	post '/result' => 'trip#result'
	get '/province' => 'test#province'
	get '/city' => 'test#city'
	get '/search' => 'test#search'
	get '/search/:key(.:format)' => 'test#search'
#	get '/result' => 'trip#result'
end
