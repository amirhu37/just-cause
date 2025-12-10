from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
options.add_argument("--headless")

url_usd = "https://www.tgju.org/profile/price_dollar_rl/history"
url_gold = "https://www.tgju.org/profile/geram18/history"

all_rows = []

with Firefox(options=options) as driver:
    driver.get(url_gold)

    wait = WebDriverWait(driver, 15)

    # Wait until table loads fully
    wait.until(EC.presence_of_element_located((By.ID, "DataTables_Table_0")))

    # get header (only once)
    header = driver.find_elements(By.CSS_SELECTOR, "#DataTables_Table_0 thead th")
    header_text = [h.text for h in header]
    all_rows.append(header_text)

    for page in range(24):
        print(f"on page: {page+1}")
        # wait until processing indicator disappears
        try:
            wait.until(
                EC.presence_of_element_located((By.ID, "DataTables_Table_0"))
            )
            wait.until(EC.presence_of_all_elements_located((By.ID, "DataTables_Table_0_next")))
        except Exception as e:
            print(f"Exception \n : {e}")

        # extract body rows
        rows = driver.find_elements(By.CSS_SELECTOR, "#DataTables_Table_0 tbody tr")

        for r in rows:
            # print(r.tag_name)
            cells = [c.text for c in r.find_elements(By.CSS_SELECTOR, "td")]
            all_rows.append(cells)

        # click next
        print(f"page {page+1} extracted")
        try:

            next_btn = driver.find_element(By.ID, "DataTables_Table_0_next")

            driver.execute_script("arguments[0].click();", next_btn)

            # next_btn.click()
            print(f"buttom {next_btn.text} clicked")
        except Exception as e:
            print(f"Exception {e}\n{e.args}")
            break

        # wait for table redraw
        time.sleep(1)

print(all_rows)
try : 
    df = pd.DataFrame(all_rows[1:], columns=all_rows[0])
    df.to_csv("gold.csv", index=False)
    print(df)
except Exception as e:
    print(f"Exception occured :\n {e}")