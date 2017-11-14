require 'elasticsearch/model'

class Area < ApplicationRecord
	include Elasticsearch::Model
	index_name 'areas'
	document_type 'city'
	mappings dynamic: 'true' do
	end

	def as_indexed_json(option={})
		{
				"province" => _source.province,
				"city"     => _source.city,
				"prov_pos" => _source.prov_pos,
				"city_pos" => _source.city_pos,
				"count"    => _source.count.to_s
		}
	end
end
Elasticsearch::Model.client = Elasticsearch::Client.new host: '192.168.0.7:9200', log: true
