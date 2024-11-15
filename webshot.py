from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from tqdm import trange
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

print("""
$$\      $$\           $$\                 $$\                  $$\     
$$ | $\  $$ |          $$ |                $$ |                 $$ |    
$$ |$$$\ $$ | $$$$$$\  $$$$$$\   $$$$$$\ $$$$$$\   $$$$$$\ $$$$$$\   
$$ $$ $$\$$ |$$  __$$\ $$  __$$\ $$  _____|$$  __$$\ $$  __$$\\_$$  _|  
$$$$  _$$$$ |$$$$$$$$ |$$ |  $$ |\$$$$$$\  $$ |  $$ |$$ /  $$ | $$ |    
$$$  / \$$$ |$$   ____|$$ |  $$ | \____$$\ $$ |  $$ |$$ |  $$ | $$ |$$\ 
$$  /   \$$ |\$$$$$$$\ $$$$$$$  |$$$$$$$  |$$ |  $$ |\$$$$$$  | \$$$$  |
\__/     \__| \_______|\_______/ \_______/ \__|  \__| \______/   \____/ 
                                    欢迎使用webshot，如有问题及时联系或提交issue
                                                            by:mongoMan
""")
# 设置配置
opt = webdriver.EdgeOptions()
opt.add_argument('--ignore-certificate-errors')  # 忽略证书错误
opt.add_argument('--ignore-ssl-errors')  # 忽略SSL错误
opt.add_argument('--allow-insecure-localhost')  # 允许不安全的本地主机
opt.add_argument('--headless')
opt.add_argument('--disable-gpu')
opt.add_experimental_option('excludeSwitches', ['enable-logging'])


# 初始化
def init():
    path = "Driver/msedgedriver.exe"
    service = Service(service=path)
    driver = webdriver.Edge(service=service, options=opt)
    return driver


# 格式化网址
def formatting(file_path):
    temp_file_path = file_path + '.tmp'
    with open(file_path, 'r') as file, open(temp_file_path, 'w') as temp_file:
        for line in file:
            if "http://" not in line and "https://" not in line:
                line = "http://" + line
            temp_file.write(line)
    os.replace(temp_file_path, file_path)


# 读取网址
def extract_domain(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain
    except ValueError:
        return "Invalid URL"


def read():
    pathweb = "web.txt"
    websites = []
    with open(pathweb, 'r') as f:
        for line in f:
            websites.append(line.strip())
    return websites


def remove_http_prefix(url):
    if url.startswith("http://"):
        return url[len("http://"):]
    elif url.startswith("https://"):
        return url[len("https://"):]
    else:
        return url


# 处理单个网站的截图
def process_website(website):
    driver = init()
    try:
        driver.get(website)
        domain = extract_domain(website)
        driver.implicitly_wait(2)  # 等待页面加载
        driver.execute_script("document.body.style.zoom='0.5'")
        title = driver.title
        web = remove_http_prefix(website)
        if title == "":
            picture_name = "空白"
        else:
            picture_name = str(domain)
        screenshot_path = 'screenshot/{}.png'.format(str(picture_name))
        driver.save_screenshot(screenshot_path)
    except Exception as e:
        print(f"处理网站 {website} 时出错：{str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    formatting("web.txt")
    websites = read()

    # 确保screenshot文件夹存在
    if not os.path.exists('screenshot'):
        os.makedirs('screenshot')

    # 处理网站并发截图
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_website, website) for website in websites]
        for future in as_completed(futures):
            future.result()  # 可以在这里处理每个任务的结果，如果有的话
