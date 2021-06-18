#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

options = Options()
options.binary = "/usr/bin/firefox"

driver = webdriver.Firefox(options=options,executable_path="/usr/bin/geckodriver")
driver.get("http://quizlet.com")
assert "Quizlet" in driver.title
input("Press enter when you've logged in and opened the Quizlet set.")
terms = driver.find_elements_by_css_selector("[aria-label='Term']")
term_data = {}
for term in terms:
    items = term.find_elements_by_class_name("TermText")
    key = items[0].get_attribute("innerText")
    value = items[1].get_attribute("innerText")
    term_data[key] = value

input("Open the match game, press enter")
start_button = driver.find_element_by_css_selector("[aria-label='Start game']")
start_button.click()
cards = driver.find_elements_by_class_name("MatchModeQuestionGridTile")
card_data = {}
for card in cards:
    text = card.find_element_by_class_name("MatchModeQuestionGridTile-text").get_attribute("aria-label")
    card_data[text] = card

card_keys = list(card_data.keys())
for card in card_keys:
    try:
        match = term_data[card]
        card_data[card].click()
        card_data[match].click()
        card_data.pop(card)
        card_data.pop(match)
    except:
        pass
input("Press enter to quit")
driver.close()
