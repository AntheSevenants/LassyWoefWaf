import re

from lxml import etree
from woef.Countries import Countries

country_re = re.compile("<Country>(.*?)<\/Country>")


def get_country_from_cmdi_file_lxml(cmdi_path):
    # Return value
    country = Countries.UNKNOWN

    root = etree.parse(cmdi_path)
    # I HATE NAMESPACES
    country_nodes = root.xpath(
        "//*[local-name() = 'Source']/*[local-name() = 'Country']")

    if len(country_nodes) > 0:
        element_text = country_nodes[0].text
        if element_text == "NL":
            country = Countries.NETHERLANDS
        elif element_text == "B":
            country = Countries.BELGIUM

    return country


def get_country_from_cmdi_file(cmdi_path):
    # Return value
    country = Countries.UNKNOWN

    with open(cmdi_path, "rt") as reader:
        for line in reader:
            if "<Country>" in line:
                element_text = country_re.search(line).group(1)

                if element_text == "NL":
                    country = Countries.NETHERLANDS
                elif element_text == "B":
                    country = Countries.BELGIUM

                return country

        return country
