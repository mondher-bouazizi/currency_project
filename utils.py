from google_images_download import google_images_download
import itertools
import os
import shutil

chromedriver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"


def set_chromedriver(chrome_driver_dir):
    if os.path.exists(chrome_driver_dir):
        global chromedriver
        chromedriver = chrome_driver_dir


def collect_banknote_images(country, num_images = 20, download_dir = "downloads\\currencies", print_urls = False, m_words=['banknote', 'money bill', 'currency']):
    """
    Collect a set of images of banknotes for a given country
    :param country: the name of the country whose banknotes are to be collected
    :param num_images: number of images per keyword, note that we have 3 default keywords, so for each country, 3 x num_images are collected
    :param download_dir: where the images are to be saved, a subfolder named after the country will be created automatically
    :param print_urls: whether or not the URL of the image is to be printed
    :param m_words: m_words: keywords meaning "bacnknote"
    :return: NOTHING
    """
    keywords = [country + " " + m for m in m_words]

    output_temp_dir = "downloads\\temp\\currencies\\" + country

    response = google_images_download.googleimagesdownload()
    for keyword in keywords:
        arguments = {"keywords":keyword, "limit":num_images, "print_urls":print_urls, "chromedriver":chromedriver, "output_directory":output_temp_dir}
        response.download(arguments)

    # this is where the final files will be saved
    download_dir = download_dir + "\\" + country
    import os
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    folders = [output_temp_dir + "\\" + country + " " + m for m in m_words]
    for folder in folders:
        src_files = os.listdir(folder)
        for file_name in src_files:
            full_file_name = os.path.join(folder, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, download_dir)

    # delete the temp folder
    shutil.rmtree(output_temp_dir)


def collect_multi_banknote_images(countries, num_images = 20, download_dir = "downloads\\currencies\\", print_urls = False, m_words=['banknote', 'money bill', 'currency']):
    """
    Collect a set of images of banknotes for a set of countries
    :param countries: is a list of all the countries whose banknotes are to be collected
    :param num_images: number of images per keyword, note that we have 3 default keywords, so for each country, 3 x num_images are collected
    :param download_dir: where the images are to be saved, a subfolder named after each country will be created automatically
    :param print_urls: whether or not the URL of the image is to be printed
    :param m_words: keywords meaning "bacnknote"
    :return: NOTHING
    """
    for country in countries:
        collect_banknote_images(country, num_images, download_dir, print_urls, m_words)


def clean_folder_names(country, download_dir = "downloads\\currencies\\"):
    c_dir = download_dir + country

    i = 0

    for filename in os.listdir(c_dir):
        src = c_dir + "\\" + filename
        dst = c_dir + "\\" + str(i).zfill(3) + ".jpg"
        os.rename(src, dst)
        i += 1