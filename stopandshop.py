"""Test Stop & Shop search. Non-US IPs might be blocked."""
from seleniumbase import SB
import time

with SB(
    uc=True,
    test=True,
    ad_block=True,
    screenshots=True,
    save_screenshots=True
) as sb:

    url = "https://stopandshop.com/"
    sb.activate_cdp_mode(url)

    sb.sleep(6)  # ✅ extra wait for slow CI

    # ✅ Safe element check (no crash)
    if not sb.is_element_present("#brand-logo_link", timeout=10):
        print("❌ Logo not found yet — refreshing page...")
        sb.refresh()
        sb.sleep(6)

    # ✅ Final safe wait
    sb.wait_for_element("input[type='search']", timeout=20)

    query = "Fresh Turkey"
    required_text = "Turkey"

    search_box = 'input[type="search"]'
    sb.click(search_box)
    sb.sleep(2)
    sb.press_keys(search_box, query)
    sb.sleep(2)

    sb.click("button.search-btn")
    sb.sleep(6)

    print('*** Stop & Shop Search for "%s":' % query)
    print('    (Results must contain "%s".)' % required_text)
    print('    (Results cannot contain "Out of Stock")')

    unique_item_text = []
    item_selector = "div.product-tile_content"

    sb.wait_for_element(item_selector, timeout=20)
    items = sb.find_elements(item_selector)

    for item in items:
        sb.sleep(0.1)
        if "Out of Stock" not in item.text:
            if required_text in item.text:
                if item.text not in unique_item_text:
                    unique_item_text.append(item.text)
                    print("* " + item.text)

    # ✅ Always save final screenshot
    sb.save_screenshot("final_results.png")
