import datetime

from s3p_sdk.plugin.config import (
    PluginConfig,
    CoreConfig,
    TaskConfig,
    trigger,
    MiddlewareConfig,
    modules,
    payload, RestrictionsConfig
)
from s3p_sdk.plugin.types import SOURCE
from s3p_sdk.module import (
    WebDriver,
)

config = PluginConfig(
    plugin=CoreConfig(
        reference='cenelec',         # уникальное имя источника
        type=SOURCE,                            # Тип источника (SOURCE, ML, PIPELINE)
        files=['cenelec.py', ],        # Список файлов, которые будут использоваться в плагине (эти файлы будут сохраняться в платформе)
        is_localstorage=False,
        restrictions=RestrictionsConfig(
            maximum_materials=50,
            to_last_material=None,
            from_date=None,
            to_date=None,
        )
    ),
    task=TaskConfig(
        trigger=trigger.TriggerConfig(
            type=trigger.SCHEDULE,
            interval=datetime.timedelta(days=1),    # Интервал перезапуска плагина
        )
    ),
    middleware=MiddlewareConfig(
        modules=[
            modules.TimezoneSafeControlConfig(order=1, is_critical=True),
            modules.SaveOnlyNewDocuments(order=2, is_critical=True)
        ],
        bus=None,
    ),
    payload=payload.PayloadConfig(
        file='cenelec.py',                 # python файл плагина (точка входа). Этот файл должен быть указан в `plugin.files[*]`
        classname='CENELEC',               # имя python класса в указанном файле
        entry=payload.entry.EntryConfig(
            method='content',
            params=[
                payload.entry.ModuleParamConfig(key='web_driver', module_name=WebDriver, bus=True),
                payload.entry.ConstParamConfig(key='committees', value={
                    "CEN/WS XFS - eXtensions for Financial Services": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:17555,25&cs=1ABEB9AFD1ACEE65BC4462323688C13E0",
                    "CEN/TC 224 - Personal identification and related personal devices with secure element, systems, operations and privacy in a multi sectorial environment": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:6205,25&cs=1BEC25E62B2D3FAE470A24A21A7315A0B",
                    "CEN/TC 389 - Innovation Management": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:671850,25&cs=1DF3ADFA491644ECD21D2F9F2927627EE",
                    "CEN/TC 434 - Electronic Invoicing": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:1883209,25&cs=18F2559A05E966F8D6BA2CD11622D2977",
                    "CEN/CLC/JTC 13 - Cybersecurity and Data Protection": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:2307986,25&cs=1ED41A3D97E9C0D226A9087045F5D181C",
                    "CEN/CLC/JTC 19 - Blockchain and Distributed Ledger Technologies": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:2702172,25&cs=16E2ADC46E2536C73D74C407A6FE4B3FD",
                    "CEN/CLC/JTC 21 - Artificial Intelligence": "https://standards.cencenelec.eu/dyn/www/f?p=205:32:0::::FSP_ORG_ID,FSP_LANG_ID:2916257,25&cs=1827B89DA69577BF3631EE2B6070F207D",
                    "CEN/CLC/JTC 22 - Quantum Technologies": "https://standards.cencenelec.eu/dyn/www/f?p=205:7:0::::FSP_ORG_ID:3197951&cs=15741D1431D56DC6C1EC9D1C3C9B8A385",
                    "CEN/CLC/JTC 24 - Digital Product Passport - Framework and System": "https://standards.cencenelec.eu/dyn/www/f?p=205:7:0::::FSP_ORG_ID:3342699&cs=1798F43FAA14922B642266F24B912DC61"
                })
            ]
        )
    )
)

__all__ = ['config']
