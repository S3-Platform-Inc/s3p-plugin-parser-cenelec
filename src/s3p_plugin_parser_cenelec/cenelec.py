import datetime
import time
import dateparser
from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from s3p_sdk.types import S3PRefer, S3PDocument, S3PPlugin
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class CENELEC(S3PParserBase):
    """
    A Parser payload that uses S3P Parser base class.
    """
    committees = {
        "CEN/WS XFS - eXtensions for Financial Services": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:17555,25&cs=1ABEB9AFD1ACEE65BC4462323688C13E0",
        "CEN/TC 224 - Personal identification and related personal devices with secure element, systems, operations and privacy in a multi sectorial environment": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:6205,25&cs=1BEC25E62B2D3FAE470A24A21A7315A0B",
        "CEN/TC 389 - Innovation Management": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:671850,25&cs=1DF3ADFA491644ECD21D2F9F2927627EE",
        "CEN/TC 434 - Electronic Invoicing": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:1883209,25&cs=18F2559A05E966F8D6BA2CD11622D2977",
        "CEN/CLC/JTC 13 - Cybersecurity and Data Protection": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:2307986,25&cs=1ED41A3D97E9C0D226A9087045F5D181C",
        "CEN/CLC/JTC 19 - Blockchain and Distributed Ledger Technologies": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:2702172,25&cs=16E2ADC46E2536C73D74C407A6FE4B3FD",
        "CEN/CLC/JTC 21 - Artificial Intelligence": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:2916257,25&cs=1827B89DA69577BF3631EE2B6070F207D",
        "CEN/CLC/JTC 22 - Quantum Technologies": "https://standards.cencenelec.eu/dyn/www/f?p=205:7:0::::FSP_ORG_ID:3197951&cs=15741D1431D56DC6C1EC9D1C3C9B8A385",
        "CEN/CLC/JTC 24 - Digital Product Passport - Framework and System": "https://standards.cencenelec.eu/dyn/www/f?p=205:7:0::::FSP_ORG_ID:3342699&cs=1798F43FAA14922B642266F24B912DC61"
    }

    def __init__(self, refer: S3PRefer, plugin: S3PPlugin, web_driver: WebDriver, max_count_documents: int = None,
                 last_document: S3PDocument = None):
        super().__init__(refer, plugin, max_count_documents, last_document)

        # Тут должны быть инициализированы свойства, характерные для этого парсера. Например: WebDriver
        self._driver = web_driver
        self._wait = WebDriverWait(self._driver, timeout=20)

    def _parse(self) -> None:

        for committee in self.committees:
            print(committee)
            self._driver.get(self.committees[committee])
            time.sleep(1)
            web_links = self._driver.find_elements(By.XPATH, '//tr/td/strong/a')
            for link_el in web_links:
                link = link_el.get_attribute('href')

                self._driver.execute_script("window.open('');")
                self._driver.switch_to.window(self._driver.window_handles[1])
                self._driver.get(link)
                time.sleep(1)

                desc = self._driver.find_element(By.ID, 'DASHBOARD_LISTPROJECT').find_elements(By.TAG_NAME, 'td')
                title = desc[1].text
                abstract = desc[3].text
                pub_date = dateparser.parse(desc[6].text)

                ics = desc[7].text

                doc = S3PDocument(
                    id=None,
                    title=title,
                    abstract=abstract,
                    text=None,
                    link=link,
                    storage=None,
                    other={'ics': ics},
                    published=pub_date,
                    loaded=None
                )

                self._find(doc)

                self._driver.close()
                self._driver.switch_to.window(self._driver.window_handles[0])
