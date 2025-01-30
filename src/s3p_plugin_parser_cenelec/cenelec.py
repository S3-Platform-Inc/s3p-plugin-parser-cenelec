import time
import dateparser
from s3p_sdk.exceptions.parser import S3PPluginParserOutOfRestrictionException, S3PPluginParserFinish
from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from s3p_sdk.types import S3PRefer, S3PDocument, S3PPlugin, S3PPluginRestrictions
from s3p_sdk.types.plugin_restrictions import FROM_DATE
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class CENELEC(S3PParserBase):
    """
    A Parser payload that uses S3P Parser base class.
    """

    def __init__(self,
                 refer: S3PRefer,
                 plugin: S3PPlugin,
                 restrictions: S3PPluginRestrictions,
                 web_driver: WebDriver,
                 committees: dict[str, str]):
        super().__init__(refer, plugin, restrictions)

        # Тут должны быть инициализированы свойства, характерные для этого парсера. Например: WebDriver
        self._driver = web_driver
        self.committees = committees
        self._wait = WebDriverWait(self._driver, timeout=20)

    def _parse(self) -> None:

        for committee in self.committees:
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
                pub_date = pub_date.replace(tzinfo=None)

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

                try:
                    self._find(doc)
                except S3PPluginParserOutOfRestrictionException as e:
                    if e.restriction == FROM_DATE:
                        self.logger.debug(f'Document is out of date range `{self._restriction.from_date}`')
                        raise S3PPluginParserFinish(self._plugin,
                                                    f'Document is out of date range `{self._restriction.from_date}`',
                                                    e)

                self._driver.close()
                self._driver.switch_to.window(self._driver.window_handles[0])
