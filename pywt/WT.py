# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 14:44:21 2018

@author: Knapstad

This file is licensed under the terms of the MIT license.

This connector contains the class Webtrends.
with the methods:

    get_profiles : gets the awailable profileIds
    get_reports : gets the awailable reports on a profile Id
    fetch_report : gets the specified report

This class need some configuration to run, theese configurations can be edited
in the "secrets/config.json" file that is generated when you import the module.
or directly in the config_ dictionary that is imported from this file.

"""


import requests
from typing import Dict
import json
import os

try:
    with open(os.path.join("secrets", "config.json"), "r") as F:
        config_ = json.load(F)
except FileNotFoundError as exc:
    print(exc, """Configfile not found, make shure there is a file called
          "config.json" in the secrets folder""")

proxies = config_["proxies"]
verify = config_["verify"]


class Analytics():
    """ Defines Webtrends class
    Sets variables:
    self.analytics_url  = "https://ws.webtrends.com/v3/Reporting/"
    self.format = config_["analytics"]["format_"]
    self.profiles = None
    self.reports = None
    self.profile =config_["analytics"]["profile"]
    self.language = "en-GB"
    self.verify = config_["verify"]
    self.auth = config_["analytics"]["auth"]
    self.proxies= config_["proxies"]
    """

    def __init__(self) -> None:
        self.analytics_url: str = "https://ws.webtrends.com/v3/Reporting/"
        self.format: str = config_["analytics"]["format_"]
        self.profiles: Dict[str, str] = None
        self.reports: Dict[str, str] = None
        self.profile: str = config_["analytics"]["profile"]
        self.language: str = config_["analytics"]["language"]
        self.verify: str = config_["verify"]
        self.auth: str = config_["analytics"]["auth"]

    def __str__(self) -> str:
        represetation = (
                f"""
                profile = {self.profile}
                format = {self.format}
                language = {self.language}
                verify = {self.verify}
                auth = {self.auth}
                profiles = {self.profiles}
                reports = {self.reports}
                """)
        return represetation

    def get_profiles(self) -> requests.models.Response:
        """Returns a list of all available profiles """
        url = str(self.analytics_url + "profiles/?format=" + self.format +
                  "&language=" + self.language)
        print(url)
        with requests.Session() as session:
                profiles = session.get(url, proxies=proxies, verify=verify,
                                       auth=auth)
                # retry if authentification fails
                if str(profiles) == "<Response [401]>":
                    profiles = session.get(url, proxies=proxies, verify=verify,
                                           auth=auth)
        self.profiles = profiles
        return profiles

    def get_reports(self, profile: str = None) -> requests.models.Response:

        """ Returns available reports for given profile """

        if not profile:
            profile = self.profile
        url = self.analytics_url+"profiles/"+profile+"/reports"
        with requests.Session() as session:
            reports = session.get(url, proxies=proxies, verify=verify,
                                  auth=auth)
            # retry if authentification fails
            if str(reports) == "<Response [401]>":
                reports = session.get(url, proxies=proxies, verify=verify,
                                      auth=auth)
        return reports

    def fetch_report(self,
                     profile: str = None,
                     report: str = "key",
                     start: str = None,
                     end: str = None,
                     sort: str = None,
                     format_: str = None,
                     period_type: str = None,
                     measures: str = None,
                     language: str = None,
                     range_: str = None,
                     search: str = None,
                     sort_by: str = None,
                     totals: str = None) -> 'response json':
        """
        Description:
        Returns the selected report

        Args:
            profile:
                The profile id of the profile you want to get data from
                defaults to self.profile

            report:
                The report id of the report you want to get, defaults to "key"
                for keymetrics

            start:
                The startdate of the period you want to get data from.
                Valid formats are '(year)m(month)d(day)h(hour)' '(year)w(week)'
                i.e. 2018m04d11h23 , 2018m04d11, 2018w05.
                there are also time macros available: CURRENT_HOUR, CURRENT_DAY
                CURRENT_DAY_MIDNIGHT, CURRENT_MONTH and CURRENT_YEAR
                i.e. CURRENT_MONTH-1 gets the previous month

            end:
                Use the end parameter to specify the ending day of a date range
                You must also supply the beginning day in the start parameter.
                end is an optional parameter. If endis not supplied, the data
                returned will only be from the time specified by start_period.
                Supplying only start is the same as supplying start
                and end with the same value.

            sort:
                Specify what measure to sort the returned data by
                If you don't provide a measure, the report is sorted by
                the first measure

            format_:
                Specify what format you want the data retured as.
                if no format is spesified format_ defaults to self.format.
                if self.format is None default is json
                Valid values:
                JSON format_ = "json"
                XML  format_ = "xml"
                XML2 format_ = "xml2" (XPath-friendly for dynamic applications)
                HTML format_ = "html"
                CSV  format_ = "csv"

            period_type:
                Specify the periodisation of the returned data.
                Valid values:
                    indv: Return every period in the period range individually
                    trend: Return the result trended (only the first dimension)
                    agg: Aggregate all values

            measures:
                Use the measures parameter to specify the measures to return.
                If you do not use this parameter, or if you specify a measureID
                for which there is no measure, all measures are returned.
                i.e  to return the two first measures use measures=1*2

            language:
                Use the language parameter with a language ID, such as en or
                locale ID, such as en-GB to specify language and locale
                preferences for translating and formatting dates and numbers in
                report data. Defaults to "en-GB"

            range:
                Define the number of rows you want
                i.e range = "start row" * "end row"
                range_="100" to get the first 100 rows,
                range="101*200" to get row 101 to 200

            search:
                Use the search parameter for reports to return only records
                containing the search string in their dimension value

            totals:
                The totals parameter specifies whether, or how,
                totals for measures are returned:

                "all" (default) all totals
                "only" only the totals
                "none" no totals
                """

        if not profile:
            profile = self.profile
        if not language:
            language = self.language
        if not format_:
            format_ = self.format
        if not auth:
            auth = self.auth
        if report == "key":
            url = self.analytics_url+"profiles/"+str(profile)+"/KeyMetrics/"
        else:
            url = (str(self.analytics_url) + "profiles/" + profile +
                   "/reports/" + str(report) + "/?format=" + format_ +
                   "&start_period=" + start + "&end_period=" + end +
                   "&sort_by=" + sort + "&period_type=" +
                   period_type + "&measures=" + measures +
                   "&language=" + language + "&range="+range_ +
                   "search=" + search + "&totals=" + totals)

        with requests.Session() as session:
                print(url)
                report = session.get(url, proxies=proxies, verify=verify,
                                     auth=auth)
                # retry if authentification fails
                if str(report) == "<Response [401]>":
                    report = session.get(url, proxies=proxies, verify=verify,
                                         auth=auth)
        return report
