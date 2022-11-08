import os
import sys
import shutil
import zipfile
import requests
import configparser

ini = configparser.ConfigParser()
ini.read('WinSeleniumChromeDriverUpdater.ini')


def get_chrome_version():
    windowsCmdScript = "reg query \"HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon\" /v version"
    # get chrome version
    chrome_version = os.popen(
        windowsCmdScript).read().split("REG_SZ")[1].strip()
    print("Google Chrome instalado: " + chrome_version)
    return chrome_version


def get_latest_chromedriver_version(chrome_version=""):
    if (chrome_version != ""):
        chrome_version = '_' + chrome_version.split('.')[0]

    # get latest chromedriver version
    latest_chromedriver_version = requests.get(
        ini['chromedriver_urls']['latest'] + chrome_version).text
    print("Ultimo chromedriver para v" + chrome_version +
          ": " + latest_chromedriver_version)
    return latest_chromedriver_version


def download_chromedriver(chrome_version):
    print("Baixando chromedriver " + chrome_version + "...")

    try:
        # download chromedriver
        chromedriver_zip = requests.get(ini['chromedriver_urls']['download'].replace(
            ':chromedriver_version', chrome_version))

        # save chromedriver zip file
        with open(ini['chromedriver_urls']['chromedriverZipName'], 'wb') as f:
            f.write(chromedriver_zip.content)

        # unzip chromedriver zip file to the same folder
        with zipfile.ZipFile(ini['chromedriver_urls']['chromedriverZipName'], 'r') as zip_ref:
            zip_ref.extractall()

        # delete zip file
        os.remove(ini['chromedriver_urls']['chromedriverZipName'])

        # return if exists file 'chromedriverFileName' on folder
        if (os.path.isfile(ini['chromedriver_urls']['chromedriverFileName'])):
            print("Chromedriver " + chrome_version + " baixado!")
            return True
        else:
            print("Falha ao baixar chromedriver " + chrome_version + "!")
            return False
    except:
        return False


def copy_chromedriver_to_paths():
    userPath = os.path.expanduser('~')

    for path in ini['pathsToCopy']:
        path = ini['pathsToCopy'][path].replace(':userPath', userPath)
        # If path not exists, create it
        if not os.path.exists(path):
            os.makedirs(path)
        print("Copiando chromedriver para " + path + "...")
        shutil.copy(ini['chromedriver_urls']['chromedriverFileName'],
                    path + "\\" + ini['chromedriver_urls']['chromedriverFileName'])
        print("ChromeDriver copiado para " + path)


def main():
    try:
        chrome_version = get_chrome_version()
        chromedriver_chrome_version = get_latest_chromedriver_version(
            chrome_version)
        chromedriver_latest_version = get_latest_chromedriver_version()

        print("")
        if (download_chromedriver(chromedriver_chrome_version) == False):
            download_chromedriver(chromedriver_latest_version)

        copy_chromedriver_to_paths()
    except Exception as e:
        print('Error: ' + str(e))


if __name__ == "__main__":
    main()

sys.exit()
