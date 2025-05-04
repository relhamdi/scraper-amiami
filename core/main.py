from json import load as json_load
from os.path import exists, join
from random import uniform as rand_uniform
from re import search as re_search
from time import sleep
from typing import Dict, List, Optional, Tuple

from config import (
    AMIAMI_API_ROOT,
    AMIAMI_USER_AGENT,
    AMIAMI_USER_KEY,
    DATA_LIST_FILE,
    ITEMS_PER_PAGE,
    OUTPUT_DIR,
    WEB_DATA_DIR,
    AmiAmiCodeTypeLiteral,
)
from curl_cffi import requests
from models.amiami.enums import (
    ItemCategory1Enum,
    ItemCategory2Enum,
    ItemSortingEnum,
    ItemTypeEnum,
)
from models.amiami.index import (
    AmiAmiItem,
    AmiAmiItemOutput,
    AmiAmiItemResponse,
    AmiAmiItemsResponse,
)
from models.amiami.utils import AmiAmiItemOutputDump, AmiAmiItemsDump, AmiAmiQueryArgs
from utils.date_util import get_current_date
from utils.json_util import save_model_to_json


class AmiAmiScraper:
    def __init__(
        self,
        always_scrap_details: bool = False,
        extra_headers: Optional[Dict[str, str]] = None,
    ):
        """
        Main class for scraping AmiAmi

        Args:
            always_scrap_details (bool, optional): If True, scrap item details to get more data.
                Note: Always the case for pre-owned items.
                Defaults to False.
            extra_headers (Optional[Dict[str, str]], optional): Extra request headers.
                Defaults to None.
        """
        self.always_scrap_details = always_scrap_details
        self.headers = {
            "X-User-Key": AMIAMI_USER_KEY,
            "User-Agent": AMIAMI_USER_AGENT,
        }
        if extra_headers is not None:
            self.headers.update(extra_headers)

    def _crawl_items_on_page(
        self,
        page: int,
        args: AmiAmiQueryArgs,
    ) -> AmiAmiItemsResponse:
        """
        Crawl all items on a given page.

        Args:
            page (int): Page number.
            args (AmiAmiQueryArgs): Request args.

        Returns:
            AmiAmiItemsResponse: Received data.
        """
        params = {
            "pagecnt": page,
            "pagemax": ITEMS_PER_PAGE,
            "lang": "eng",
            "age_confirm": 1,
            "s_keywords": args.keyword or "",
            "s_cate1": args.category1 if args.category1 else "",
            "s_cate2": args.category2 if args.category2 else "",
            "s_sortkey": args.sort_key if args.sort_key else "",
            # "mcode": "",
            # "ransu": "",
            # "s_cate_tag": 14
        }
        for type in args.types:
            params[type] = "1"

        # Get items on given page
        url = f"{AMIAMI_API_ROOT}/items"
        print(f"> Crawling '{url}' with params={params}")
        response = requests.get(
            url,
            params=params,
            headers=self.headers,
            impersonate="chrome110",
        )
        response.raise_for_status()
        data = response.json()
        return AmiAmiItemsResponse(**data)

    def _scrap_items(self, args: AmiAmiQueryArgs) -> List[AmiAmiItem]:
        """
        Scrap all items according to query.

        Args:
            args (AmiAmiQueryArgs): Request args.

        Returns:
            List[AmiAmiItem]: List of raw items obtained.
        """
        # Prepare sorting option
        if args.sort_key is None:
            if ItemTypeEnum.PRE_OWNED in args.types and len(args.types) == 1:
                args.sort_key = ItemSortingEnum.PREOWNED
            else:
                args.sort_key = ItemSortingEnum.RECENT_UPDATE

        # Crawl items in pages
        results: List[AmiAmiItem] = []
        page = 1
        while True:
            response = self._crawl_items_on_page(page, args)
            # If no more pages
            if not response.api_success or not response.items:
                break
            results.extend(response.items)

            # If all wanted pages were scraped
            if args.num_pages and page >= args.num_pages:
                break

            page += 1
            sleep(rand_uniform(0, 2))

        return results

    def _crawl_item_details(
        self,
        code: str,
        code_type: AmiAmiCodeTypeLiteral,
    ) -> AmiAmiItemResponse:
        """
        Crawl details page for the given item.

        Args:
            code (str): Item code.
            code_type (AmiAmiCodeTypeLiteral): Item code type.

        Returns:
            AmiAmiItemResponse: Received data.
        """
        params = {code_type: code}

        # Crawl details page for given item
        url = f"{AMIAMI_API_ROOT}/item"
        response = requests.get(
            url,
            params=params,
            headers=self.headers,
            impersonate="chrome110",
        )
        response.raise_for_status()
        data = response.json()

        # Longer timeout between two different pages (quicker if related items)
        if code_type == "gcode":
            sleep(rand_uniform(0, 2))
        else:
            sleep(rand_uniform(0, 1))

        return AmiAmiItemResponse(**data)

    def _map_item_details_to_final(
        self,
        api_response: AmiAmiItemResponse,
    ) -> AmiAmiItemOutput:
        """
        Map the detailed item into its final enriched format.

        Args:
            api_response (AmiAmiItemResponse): API data.

        Returns:
            AmiAmiItemOutput: Final item.
        """
        item_tags_sources = (
            api_response.embedded_data.makers
            + api_response.embedded_data.series_titles
            + api_response.embedded_data.original_titles
            + api_response.embedded_data.character_names
        )
        final_item = api_response.item.minify()

        # Generate item tags
        final_item.tags = [item.name for item in item_tags_sources]

        # Retrieve Item and Box condition if possible (for pre-owned items)
        match = re_search(
            r"\(Pre-owned ITEM:([A-CJ][+-]?)/BOX:([ABC]|N)\)",
            api_response.item.sname,
        )
        if match:
            final_item.item_condition, final_item.box_condition = match.groups()

        return final_item

    def _scrap_item(
        self,
        code: str,
        code_type: AmiAmiCodeTypeLiteral,
        check_alts: bool = True,
    ) -> List[AmiAmiItemOutput]:
        """
        Scrap an item's details page and its related items.

        Args:
            code (str): Item code.
            code_type (AmiAmiCodeTypeLiteral): Item code type.
            check_alts (bool, optional): If True, will scrap the items related to the current one.
                Useful to get alternative pre-owned items.
                Defaults to True.

        Returns:
            List[AmiAmiItemOutput]: List of final items obtained.
        """
        results: List[AmiAmiItemOutput] = []

        # Crawl details for given item
        try:
            response = self._crawl_item_details(code, code_type)
        except Exception as e:
            if "429" in str(e):
                raise Exception("HTTP 429, try again later")
            print(e)
            return results
        if not response.api_success or not response.item:
            print(f"Error on '{code}', nothing found.")
            return results

        # Map item to final format
        results.append(self._map_item_details_to_final(response))
        if check_alts:
            # Crawl related items pages
            print("Checking related items...")
            for other_item in response.embedded_data.other_items:
                # Check_alts to false to avoid getting items twice (and entering an infinite loop)
                results.extend(
                    self._scrap_item(other_item.scode, "scode", check_alts=False)
                )

        return results

    def run_scraping(self, args: AmiAmiQueryArgs) -> Tuple[str, str]:
        """
        Main scraping method.
        Get all data from multiple pages according to a query.

        Args:
            args (AmiAmiQueryArgs): Request args.

        Returns:
            Tuple[str, str]: (timestamp, filename), where:
                - timestamp: Stringified date used in the raw data dump (acts as an ID)
                - filename: Full filename where the items were dumped
        """
        print("Run scraping...")
        results = self._scrap_items(args)

        print(f"Saving {len(results)} items...")
        timestamp = get_current_date()
        filename = f"{timestamp}-{args.stringify()}.json"
        with open(join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            save_model_to_json(
                f,
                AmiAmiItemsDump(items_length=len(results), items=results),
            )

        print(f"Data saved to '{filename}'")
        return timestamp, filename

    def run_enrich(self, timestamp: str, filename: str):
        """
        Main enriching method.
        Format raw items to final format.
        Can be relaunched from last saved checkpoint if an error occurred.

        Args:
            timestamp (str): Date used in the file to enrich.
            filename (str): Filename where raw data is located.
        """
        print("Run enrich...")
        # Open raw data file
        filepath = join(OUTPUT_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            base_data_parsed = AmiAmiItemsDump(**json_load(f))
        amiami_items = base_data_parsed.items

        # Open output file, if any, and retrieve checkpoint variables
        new_filename = f"{timestamp}-mapped_items.json"
        new_filepath = join(WEB_DATA_DIR, new_filename)
        try:
            with open(new_filepath, "r", encoding="utf-8") as f:
                result_data_parsed = AmiAmiItemOutputDump(**json_load(f))
            start_index = result_data_parsed.current_index
            result_mapped: List[AmiAmiItemOutput] = result_data_parsed.items
        except FileNotFoundError:
            start_index = -1
            result_mapped: List[AmiAmiItemOutput] = []
        else:
            print("> Data retrieved from file")

        # Loop over items to scrap their details pages (start at next item from checkpoint)
        for index in range(start_index + 1, len(amiami_items)):
            item = amiami_items[index]

            print(
                f"({index + 1}/{len(amiami_items)}) On item {item.gcode}",
                f"https://www.amiami.com/eng/detail/?gcode={item.gcode}",
            )
            # Scrap details for pre-owned or if requested
            if item.is_preowned or self.always_scrap_details:
                print("> Scraping item details...")
                mapped_items = self._scrap_item(item.gcode, "gcode")

                if not mapped_items:
                    print("No items found, mapping from original data...")
                    mapped_items.append(item.minify())
                    with open(join(OUTPUT_DIR, "_errors.txt"), "a") as f:
                        f.write(
                            f"> {get_current_date()} - On file {timestamp}: "
                            + f"Error at index {index} / gcode {item.gcode}\n",
                        )

                # Using date from general scraping as it is more precise
                for mapped_item in mapped_items:
                    mapped_item.release_date = item.releasedate
                result_mapped.extend(mapped_items)

            else:
                print("> Skipping details scraping...")
                result_mapped.append(item.minify())

            print("Saving items...\n")

            with open(new_filepath, "w", encoding="utf-8") as f:
                save_model_to_json(
                    f,
                    AmiAmiItemOutputDump(
                        current_index=index,
                        items_length=len(result_mapped),
                        items=result_mapped,
                    ),
                )

        # Save final filepath (if not there yet)
        if exists(DATA_LIST_FILE):
            with open(DATA_LIST_FILE, "r") as f:
                existing_files = set(f.read().splitlines())
        else:
            existing_files = set()

        with open(DATA_LIST_FILE, "a") as f:
            if new_filename not in existing_files:
                f.write(new_filename + "\n")


if __name__ == "__main__":
    print("Init scraper...")
    amiami = AmiAmiScraper(always_scrap_details=False)
    # Request args
    batch_args: List[AmiAmiQueryArgs] = [
        AmiAmiQueryArgs(
            num_pages=5,
            types=[ItemTypeEnum.NEW],
            category2=ItemCategory2Enum.CHARACTER,
        ),
        AmiAmiQueryArgs(
            num_pages=1,
            types=[ItemTypeEnum.PRE_ORDER, ItemTypeEnum.PRE_OWNED],
            category2=ItemCategory2Enum.FOREIGN,
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
