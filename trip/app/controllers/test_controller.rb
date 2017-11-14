class TestController < ApplicationController
	def index
		res = Blog.search(
								query: { match_all: {} }, 
								sort: { "date": "desc" }, 
								size: 10
				)
		@result = res.results
	end
	
	def province
		res = Area.search(
							size: 0,
							aggs: {
								"provinces": {
									terms: {
										field: "province.keyword",
										order: { "sum_cnt": "desc" },
										size: 20
									},
									aggs: {
										"sum_cnt": {
											sum: { "field": "count" }
										},
										"prov_pos": {
											top_hits: {
												size: 1,
												_source: { includes: ["prov_pos"] }
											}
										}
									}
								}
							})
		render json: res.aggregations['provinces']['buckets']
	end

	def city
		res = Area.search	query: { 
												bool: {
													must: { 
														match_all: {} 
													}, 
													filter: {
														range: {
															"count": {
																"gt": 0
															}
														}
													}
												}
											},	
											sort: { "count": "desc"	}, size: 200
		render json: res.results
	end

	def search
		key = params[:key]

		resPost = Blog.search(
											query: { match_phrase: { content: key } }, 
											sort: { "_score": "desc" }, 
											size: 10
							)
		resCity = Area.search query: { match: { city: { type: "phrase_prefix", query: key } } }

		res = { 
			"posts" => resPost,
			"city" => resCity
		}
		render json: res
	end

end





