# -*- coding: utf-8 -*-
import elasticsearch

es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])

data = {
	"doc": {
		"body": "서울 대공원 나들이 ㄱㄱ"
		}
	}

#response = es.transport.perform_request(method='GET', url='/blogs/queries/_percolate', body=data)
#print(response)
#area = response['matches']
#for a in response['matches']:
#	print(a['_id'])


query = {
	"aggs": {
		"provinces": {
			"terms": {
				"field": "province.keyword",
				"order": { "sum_cnt": "desc" },
				"size": 20
			},
			"aggs": {
				"sum_cnt": {
					"sum": {
						"field": "count"
					}
				},
				"prov_pos" : {
					"top_hits" : {
						"size": 1,
						"_source": {
							"includes": ["prov_pos"]
						}
					}
				}
			}
		}
	}
}
'''
response = es.search(index='areas', doc_type='city', size=0, body=query)
data = response['aggregations']['provinces']['buckets']
for d in data:
	print(d['key'])
	print(d['sum_cnt']['value'])
	print(d['prov_pos']['hits']['hits'][0]['_source']['prov_pos'])


'''

data = {
	"test": "test1"
	}
try:
	(res_code, res, a) = es.create(index='test', doc_type='test1', id='1', body=data)
	print(res_code+"::"+res)
except elasticsearch.TransportError as err:
	print(err)

