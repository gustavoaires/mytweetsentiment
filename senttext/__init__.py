# -*- coding: latin-1 -*-
from collecting.datacollect import APICollect
from textprocessor import portugueseprocessor as pln
import json


def main():
    # CONSUMER_KEY = '4jtRRPl3WvYyzPvRnNKRaaLGr'
    # CONSUMER_SECRET = 'dFr8l0HDQ2RA3sQhiTjkMvJs9ML38BLkEoofDNr50tBEOCmZNA'
    # OAUTH_TOKEN = '98992106-OsffZtvTWPxeHCkA5G9golyjU4inlvb7XB6g0oDva'
    # OAUTH_TOKEN_SECRET = 'eD0RE8AyfTDmyYnOKfWLo3XvjILKktRJOIoQnlmHCmbip'

    tweets = []
    input_file = open('dataset_until_22_05.json', 'r')
    output_file = open('dataset_until_22_05_pln.json', 'w')

    # query = "previdencia social OR reforma da previdencia OR reforma da presidencia ' \
    #         'OR previdencia since:2017-05-23 until:2017-05-24"
    # scrape = datacollect.ScrapeCollect()
    # tweets = scrape.scrape_tweets(query, 20)

    # api = APICollect(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    # tweets = api.rest_tweets(query=query, limit=5)
    #
    # for tweet in tweets:
    #     json.dump(tweet, output_file)
    #     output_file.write("\n")

    cleaner = pln.TextCleaner()
    named = pln.NamedEntity()

    print 'reading'
    for line in input_file:
        tweets.append(json.loads(line))

    print 'writing'
    for tweet in tweets[:10]:
        text = tweet['text']
        text = text.lower()
        text = named.removeTwitterUsername(text)
        text = cleaner.removeStopwords(text)
        text = cleaner.removeSymbols(text)
        text = cleaner.removeLinks(text)
        text = cleaner.removeSufPort(text)
        text = cleaner.removeAccent(text)
        tweet['text'] = text
        json.dump(tweet, output_file)
        output_file.write("\n")

main()
