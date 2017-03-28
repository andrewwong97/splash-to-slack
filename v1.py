from selenium import webdriver
import time, requests, json


def get_current_rsvps():
	driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])

	driver.get("https://splashthat.com/login")

	username = driver.find_element_by_name("data[User][email]")
	password = driver.find_element_by_name("data[User][password]")

	username.send_keys("YOUR_SPLASH_LOGIN_EMAIL")
	password.send_keys("YOUR_PASSWORD")

	driver.find_element_by_name("submit").click()

	driver.find_element_by_css_selector("div#view-event-by-list").click()

	time.sleep(1)

	rsvps = driver.find_element_by_css_selector("td.rsvps-number")
	n = rsvps.get_attribute('innerHTML')

	driver.quit()
	return n


def post_to_slack(current_rsvps):
	payload = {
		"text": "Current RSVPs: " + current_rsvps
	}

	requests.post("YOUR_SLACK_INCOMING_WEBHOOK", data=json.dumps(payload))


if __name__ == '__main__':
	post_to_slack(get_current_rsvps())



