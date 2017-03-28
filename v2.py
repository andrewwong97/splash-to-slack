#!/usr/bin/env python
import time, requests, json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("email", help="splash username")
parser.add_argument("password", help="splash password")
parser.add_argument("slackhook", help="slack POST webhook")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=1)
args = parser.parse_args()

payload = {
	'data[User][email]': args.email,
	'data[User][password]': args.password
}

def get_stats():
	with requests.Session() as s:
		p = s.post('https://splashthat.com/login', data=payload)

		r = s.get('https://splashthat.com/address_book/event_api_search?&abc_id=&clear=true&contact_id=&dir=desc&end_date=&event_ids=&event_type_ids=&export_fields=&filters=&force=true&group_id=&limit=25&list_ids=&location=&location_mode=&method=all&page=1&preload=false&sort_by=saved&splash_themes_version=1&start_date=&tag_ids=&text_filter=&view_type=list&vip=&visible=true')
		d = json.loads(r.text)
		
	stats = {}	
	for i in d['data']['results'][-1]['stats']:
		stats[i] = d['data']['results'][-1]['stats'][i]
	return stats

def get_rsvps():
	with requests.Session() as s:
		p = s.post('https://splashthat.com/login', data=payload)

		r = s.get('https://splashthat.com/address_book/event_api_search?&abc_id=&clear=true&contact_id=&dir=desc&end_date=&event_ids=&event_type_ids=&export_fields=&filters=&force=true&group_id=&limit=25&list_ids=&location=&location_mode=&method=all&page=1&preload=false&sort_by=saved&splash_themes_version=1&start_date=&tag_ids=&text_filter=&view_type=list&vip=&visible=true')
		d = json.loads(r.text)
			
	return d['data']['results'][-1]['stats']['rsvp_attending']


def post_to_slack(**kwargs):
	s = ""
	for i in kwargs:
		if str(kwargs[i]) != '-':
			s += i + ": " + str(kwargs[i]) + "\n"
	s = s.rstrip()

	d = {
		"text": s
	}

	requests.post(args.slackhook, data=json.dumps(d))


if __name__ == '__main__':
	post_to_slack(RSVPs=get_rsvps())
