from typing import List

from models.amiami.enums import (
    ItemCategory1Enum,
    ItemCategory2Enum,
    ItemCategory3Enum,
    ItemTypeEnum,
)
from models.amiami.utils import AmiAmiQueryArgs
from scrapers.amiami import AmiAmiScraper

if __name__ == "__main__":
    print("Init scraper...")
    amiami = AmiAmiScraper(always_scrap_details=False)
    # Request args
    batch_args: List[AmiAmiQueryArgs] = [
        AmiAmiQueryArgs(
            num_pages=5,
            types=[ItemTypeEnum.NEW],
            category1=ItemCategory1Enum.CARD_GAMES,
        ),
        AmiAmiQueryArgs(
            num_pages=1,
            types=[ItemTypeEnum.PRE_ORDER, ItemTypeEnum.PRE_OWNED],
            category2=ItemCategory2Enum.FOREIGN_FIGURES,
        ),
        AmiAmiQueryArgs(
            num_pages=2,
            types=[ItemTypeEnum.BACK_ORDER, ItemTypeEnum.NEW, ItemTypeEnum.PRE_OWNED],
            category3=ItemCategory3Enum.GUNDAM_TOYS,
        ),
    ]

    print("Starting scraping...")
    for args in batch_args:
        # Scrap website
        timestamp, filename = amiami.run_scraping(args)
        # timestamp, filename = (
        #     "20250318_000540",
        #     "20250318_000540-categories=s_st_condition_flg.json",
        # )

        # Enrich format
        amiami.run_enrich(timestamp, filename)
    print("End scraping")
