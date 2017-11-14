class TripController < ApplicationController
	def index
		res = Blog.search query: { match_all: {} },	sort: { "date": "desc" }, size: 10
		@result = res.results
 	end

	def province
		res = Area.search( size: 0, aggs: { "provinces": { terms: { field: "province.keyword", order: { "sum_cnt": "desc" }, size: 20 }, aggs: { "sum_cnt": { sum: { field: "count" } } } } } )
		render json: res.aggregations['provinces']['buckets']
	end

	def result
		@key = params[:key]
		response = Blog.search query: { term: { body: @key } }
		@result = response.results
		render action: 'index'
	end
end
