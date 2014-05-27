#!/usr/bin/python3

import logging
import subprocess
import re

from bs4 import BeautifulSoup

subprocess.call("wget https://en.wikipedia.org/wiki/List_of_cognitive_biases -O page.html", shell=True)

def rm_brackets(string):
    new_string = ""
    for sub_string in string.split("["):
        if "]" in sub_string:
            l = sub_string.split("]")
            for s in l[1:]:
                new_string += s
        else:
            new_string += sub_string
    return new_string

def build_tables():
    tables = {}
    with open("page.html") as f:
        soup = BeautifulSoup(f.read())
        logging.debug("Listing heading with tables, prepended with ! if ignored")
        for t in soup.select(".wikitable"):
            heading = t.find_previous("h2").text[:-6]
            rows = []
            logging.debug(" - " + heading)
            for row in t.find_all("tr"):
                parts = row.find_all("td")
                if parts:
                    name = rm_brackets(parts[0].text)
                    desc = rm_brackets(parts[1].text)
                    rows.append((name, desc))
                    logging.debug("    - " + name + ": " + desc)
            tables[heading] = rows
    return tables

def main():
    tables = build_tables()
    for table in tables.keys():
        with open("out/"+table.replace(" ", "-")+".csv", "w") as f:
            f.write("Name\tDescription\n")
            for name, desc in tables[table]:
                f.write("{}\t{}\n".format(name, desc))

if __name__ == "__main__":
    main()
