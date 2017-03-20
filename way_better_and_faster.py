#!/usr/bin/env python
import time, requests, json

# WAYYY faster
def fast_get_stats():
	payload = {
		'data[User][email]': 'YOUR_SPLASH_LOGIN_EMAIL',
		'data[User][password]': 'YOUR_PASSWORD'
	}

	with requests.Session() as s:
		p = s.post('https://splashthat.com/login', data=payload)
		r = s.get('https://splashthat.com/address_book/event_api_search?&abc_id=&clear=true&contact_id=&dir=desc&end_date=&event_ids=&event_type_ids=&export_fields=&filters=&force=true&group_id=&limit=25&list_ids=&location=&location_mode=&method=all&page=1&preload=false&sort_by=saved&splash_themes_version=1&start_date=&tag_ids=&text_filter=&view_type=list&vip=&visible=true')
		d = json.loads(r.text)
		
	stats = {}	
	for i in d['data']['results'][-1]['stats']:
		stats[i] = d['data']['results'][-1]['stats'][i]
	return stats

def post_to_slack(data):
	s = ""
	for i in data:
		if str(data[i]) != '-':
			s += i + ": " + str(data[i]) + "\n"
	s = s[:-2]

	payload = {
		"text": s
	}

	requests.post("YOUR_SLACK_INCOMING_WEBHOOK", data=json.dumps(payload))


if __name__ == '__main__':
	post_to_slack(fast_get_stats())



