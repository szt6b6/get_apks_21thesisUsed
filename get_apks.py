from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
prefs = {'download.default_directory': 'apks', #存储位置
        "download.prompt_for_download": False,
        'profile.default_content_settings.popups': 0,  # 设置为0，禁止弹出窗口
}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(chrome_options=options) # if chromedirver.exe not in path，指定chromedirver.exe路径， executable_path='C:/path/to/chromedriver.exe'
with open(r"urls.txt") as f, open("apk_links.txt", "w+") as ff:
    packages = f.readlines()
    for package in packages:
        package = package.replace("\n", "")
        link = "https://apkcombo.com/de-de/apk-downloader/?device=&arches=&sdkInt=28&sa=1&lang=en&dpi=480&q=" + package
        driver.get(link)

        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "download-item"))) #等动态链接被输出
        except Exception:
            print(package + " not found")
            continue

        element = driver.find_element_by_xpath(
            '''//*[@id="apkcombo-server-tab"]/div/a''') # 定位直链元素

        apk_name = str(element.text.split("\n")[0].encode("ascii", "ignore")) # 获得apk 名字
        apk_link = element.get_attribute('href') # 获得 apk 链接
        print(apk_name + " : " + apk_link + "\n")

        ff.writelines(apk_name + " : " + apk_link + "\n") # 追加写名字：链接到文件

        
ff.close()
f.close()

driver.quit()



