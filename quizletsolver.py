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
while True:
    input("Press enter when you've logged in and opened the Quizlet set. You may need to scroll down to load all the terms.")
    terms = driver.find_elements_by_css_selector("[aria-label='Term']")
    term_data = {}
    for term in terms:
        items = term.find_elements_by_class_name("TermText")
        key = items[0].get_attribute("innerText")
        value = items[1].get_attribute("innerText")
        term_data[key] = value

    print("Total terms: " + str(len(term_data)))
    is_correct = input("If this is not correct, press `r` and then enter to restart the scan. If it is correct, press enter.")
    if is_correct == "r":
        continue

    input("Press enter when the match game has loaded (do not start it yet! This program will do that for you)")
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
            print("Found match ", card, ", ", match)
        except:
            print("Card skipped (for now)")
            pass
    input("Press enter to run another set, press ^C or whatever to quit")
driver.close()
