#!/usr/bin/env python3
import atexit
from datetime import datetime
import json
import os
from lxml import html
import requests
from typing import Dict, List, NoReturn


APP_NAME: str = "pySearch"
USER_CACHE_DIR: str = os.path.expanduser("~") + f"/.cache/{APP_NAME}"
if not os.path.isdir(USER_CACHE_DIR):
    os.makedirs(USER_CACHE_DIR)

CACHE: Dict
USER_CACHE_FILE: str = f"{USER_CACHE_DIR}/{APP_NAME}.json"
if os.path.isfile(USER_CACHE_FILE):
    with open(USER_CACHE_FILE, "r", encoding="utf-8") as _:
        CACHE = json.loads(_.read())
else:
    CACHE = {}

MAX_CACHE_AGE_DAYS: int = 31
PYPI_MAX_RES_PER_PAGE: int = 20
TIMEOUT: int = 15


def search_request(
        query: str,
) -> requests.Response:
    """
    *Search Request*
    :param query: The full search query.
    :return: A `requests.Response` object.
    """
    return requests.get(
        f"https://pypi.org/search/?{query}",
        timeout=TIMEOUT
    )


def process_response(response: requests.Response) -> List[List]:
    """
    *Process Response*
    :param response: A `requests.Response` object.
    :return: A list of tuples containing the name, version, description and release date of the packages.
    """
    def extract_first(elem: html.HtmlElement, class_name: str) -> html.HtmlElement:
        if r := elem.find_class(class_name):
            return r[0].text_content().strip()

    root = html.fromstring(response.text)
    elements = root.find_class("package-snippet")
    return [[
        extract_first(_, "package-snippet__name"),
        extract_first(_, "package-snippet__version"),
        extract_first(_, "package-snippet__description"),
        extract_first(_, "package-snippet__released"),
    ] for _ in elements]


def search_request_and_process(
        q: str,
        page: int,
        no_cache: bool = False
) -> List[List]:
    """
    *Search Request and Process*
    :param q: The search query.
    :param page: The search query.
    :param no_cache: Bypasses the cache if set to `True`.
    :return: A list of tuples containing the name, version, description and release date of the packages.
    """
    query = f"{q=!s}&{page=!s}"
    data = None
    if query in CACHE and no_cache is False:
        delta = datetime.now() - datetime.fromtimestamp(CACHE[query]["update_date"])
        if delta.days < MAX_CACHE_AGE_DAYS:
            data = CACHE[query]["data"]
    if data is None:
        data = process_response(response=search_request(query=query))
        CACHE.update({
            query: {
                "update_date": int(datetime.now().timestamp()),
                "data": data,
            }
        })
    return data


def search(
        q: str,
        page: int = 0,
        # limit: int = 5,
        no_cache: bool = False,
) -> NoReturn:
    """
    *Search*
    :param q: The search query.
    :param page: The search query.
    # :param limit: The maximal number of results to display.
    :param no_cache: Bypasses the cache if set to `True`.
    """
    print("☁️ Fetching results...\n", flush=True)
    data = search_request_and_process(q=q, page=page, no_cache=no_cache)
    for name, version, description, date in data:
        msg = f"🐍 {name} v.{version}\n📅 {date}\n📋 {description}\n"
        print(msg, flush=True)


@atexit.register
def save_cache() -> None:
    """
    *Save Cache*
    """
    with open(USER_CACHE_FILE, "w", encoding="utf-8") as _:
        json.dump(CACHE, _, indent=2)
