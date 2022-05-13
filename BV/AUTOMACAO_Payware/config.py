from email import header
from requests_html import HTMLSession
import os

domain = os.environ["PAYWARE_DOMAIN"]
cookie_name = os.environ["PAYWARE_COOKIE_NAME"]
dsrwid = os.environ["PAYWARE_DSRWID"]

payware_login_url = f"https://{domain}/CMS-ISSUER/loginUser.jsf"
payware_search_url = f"https://{domain}/CMS-ISSUER/modules/issuer/cardHolder/templates/cardHolderTemplate.jsf?openSearch=true"

base_headers = {
    "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='98', 'Google Chrome';v='98'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sser-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}
