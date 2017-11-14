require 'elasticsearch/model'

class Blog < ApplicationRecord
  include Elasticsearch::Model
    index_name 'blogs'
    document_type 'post'
    mappings dynamic: 'true' do
    end

  def as_indexed_json(options={})
		{
   	 "title"    => _source.title,
   	 "img"      => _source.img,
   	 "desc"     => _source.desc,
   	 "url"      => _source.url,
   	 "date"     => _source.date,
   	 "content"  => _source.content,
		 "author"   => _source.author
  	}
	end
end
Elasticsearch::Model.client = Elasticsearch::Client.new host: '192.168.0.7:9200', log: true
