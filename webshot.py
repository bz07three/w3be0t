from selenium import webdriver
from selenium.webdriver.edge.service import Service
from tqdm import trange
import os

print("""
$$\      $$\           $$\                 $$\                  $$\     
$$ | $\  $$ |          $$ |                $$ |                 $$ |    
$$ |$$$\ $$ | $$$$$$\  $$$$$$$\   $$$$$$$\ $$$$$$$\   $$$$$$\ $$$$$$\   
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
def process_website(driver, website):
    try:
        driver.get(website)
        driver.execute_script("document.body.style.zoom='0.5'")
        title = driver.title
        web=remove_http_prefix(website)
        if title == "":
            picture_name = "空白"
        else:
            picture_name = str(title)
        driver.save_screenshot('screenshot/{}_{}.png'.format(picture_name,str(web)))
    except Exception as e:
        pass



if __name__ == "__main__":
    formatting("web.txt")
    websites = read()
    driver = init()

    # 处理网站并发截图
    for _ in trange(len(websites)):
        process_website(driver, websites[_])

    driver.quit()
