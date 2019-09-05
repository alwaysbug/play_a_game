import time
# 初始化下一期数
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config import CONFIG
from send_mail import Mail

logNexPre = 0

# 基础投入
baseMoney = 1

# 费率
fee = 1.96

# 总资产
totalMoney = 100

# 最大承受某一结果出现的重复次数
maxrepeat = 2

# 初始化某一结果出现的重复次数
repeat = 0

# 上一期投入
logLastMoney = 0

# 下一期投入
nexMoney = 0

# 上一期预测的单双
logLastResult = True

# 下一期预测的单双
nexResult = True

# 交易次数
count = 0

# 开启调试
debug = False


# 到了下一期
def getResult(p):
    return True if p == '单' else False


def boolToStr(p):
    return '单' if p == True else '双'


def shopIn(m, r):
    try:
        if m == 0:
            m = baseMoney

        if debug:
            print('【买入】' + str(m) + '预测结果:' + boolToStr(r))
            return True

        if r:
            browser.find_element_by_xpath("//div[contains(@class,'betNumber')]/ul/li/a[text()='单']").click()
            time.sleep(0.1)
            browser.find_element_by_xpath("//div[contains(@class,'Panel')]/a[text()='确认选号']").click()
            time.sleep(0.5)

            buy(m, r)
            return True
        else:
            browser.find_element_by_xpath("//div[contains(@class,'betNumber')]/ul/li/a[text()='双']").click()
            time.sleep(0.1)
            browser.find_element_by_xpath("//div[contains(@class,'Panel')]/a[text()='确认选号']").click()
            time.sleep(0.5)

            buy(m, r)
            return True
    except Exception as e:
        return False


def buy(m, r):

    moneyInput = browser.find_element_by_xpath(
        "//div[contains(@class,'selectList')]/table/tbody/tr/td/i/input[contains(@class,'eachPrice')]")
    browser.execute_script("arguments[0].click()", moneyInput)
    time.sleep(0.1)

    moneyInput.clear()
    moneyInput.send_keys(str(m))
    time.sleep(0.1)

    moneyInput.send_keys(Keys.ENTER)

    touzhu = browser.find_element_by_xpath("//div[contains(@class,'Bet')]/a[text()='立即投注']")
    browser.execute_script("arguments[0].click()", touzhu)

    time.sleep(1)
    if checkNum(m):
        browser.find_element_by_xpath("//div[contains(@class,'layermbtn')]/span[text()='确认投注']").click()
        print('【买入】' + str(m) + '预测结果:' + boolToStr(r))
        return True
    else:
        cancel = browser.find_element_by_xpath("//button[contains(@class,'layermend')]")
        browser.execute_script("arguments[0].click()", cancel)
        buy(m, r)
    return False


def checkNum(m):
    try:
        strNum = browser.find_element_by_xpath("//div[@id='CheckBetLayer']/ul/li[last()]/em/em").text
        money = int(strNum)
        if m == money:
            return True
        else:
            return False
    except Exception as e:
        return False


def closeDialog():
    # 弹框关闭按钮
    if isCloseElementExist():
        confirmBtn = browser.find_element_by_xpath("//div[contains(@class,'layermbtn')]/span[@type='1']")
        browser.execute_script("arguments[0].click()", confirmBtn)


def isCodeElementExist():
    try:
        browser.find_element_by_xpath("//input[contains(@class, 'userInput') and @tag='验证码']")
        return True
    except Exception as e:
        return False


def isCloseElementExist():
    try:
        browser.find_element_by_xpath("//div[contains(@class,'layerConfirm')]/h3[text()='温馨提示']")
        return True
    except Exception as e:
        return False


def isConfirmElementExist():
    try:
        browser.find_element_by_xpath("//div[contains(@class,'layerBet')]/h3[text()='投注确认']")
        return True
    except Exception as e:
        return False


def isMoneyElementExist():
    try:
        browser.find_element_by_xpath("//span[contains(@class,'userMoney')]/em")
        return True
    except Exception as e:
        return False


def getTreasure():
    if debug:
        print('当前余额' + str(totalMoney))
        return str(totalMoney)
    if not isMoneyElementExist():
        icon = browser.find_element_by_xpath("//span[contains(@class,'userMoney')]/i")
        browser.execute_script("arguments[0].click()", icon)
        treasure = browser.find_element_by_xpath("//span[contains(@class,'userMoney')]/em").text
        print('当前余额' + treasure)
        return treasure
    else:
        treasure = browser.find_element_by_xpath("//span[contains(@class,'userMoney')]/em").text
        print('当前余额' + treasure)
        return treasure


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(chrome_options=options, executable_path='/usr/local/chromedriver/chromedriver')
browser.implicitly_wait(10)
browser.get('https://5008117.com')

login = browser.find_element_by_xpath("//a[@href='/login']")
browser.execute_script("arguments[0].click()", login)

browser.find_element_by_xpath("//input[contains(@class, 'userInput') and @tag='账号']").send_keys(
    CONFIG['mobile'])
browser.find_element_by_xpath("//input[contains(@class, 'userInput') and @tag='密码']").send_keys(
    CONFIG['password'])

if isCodeElementExist():
    code = input('输入验证码:\n')
    browser.find_element_by_xpath("//input[contains(@class, 'userInput') and @tag='验证码']").send_keys(code)

browser.find_element_by_xpath("//a[text()='登 录']").click()
# 关闭通知
browser.find_element_by_xpath("//div[contains(@class, 'noticeDialogBody')]/div/i").click()
# 进入快三页面
browser.find_element_by_xpath("//a[@href='/lottery/K3/1407']").click()

while True:
    if isConfirmElementExist():
        continue
    time.sleep(0.3)
    closeDialog()

    # 当前期数
    currPer = browser.find_element_by_xpath("//div[contains(@class,'openText')]/b").text.strip()
    # 下一期数
    nexPer = browser.find_element_by_xpath("//div[contains(@class,'timerText')]/b").text.strip()

    if currPer == logNexPre:
        # 获取最新一期期号
        periods = browser.find_element_by_xpath(
            "//div[contains(@class,'openNumList')]/table/tbody[last()]/tr[1]/td/i").text.strip()
        if periods != currPer:
            # 检测到还未更新上一期结果，退出本次循环
            continue

        # 判断是单是双
        period = browser.find_element_by_xpath(
            "//div[contains(@class,'openNumList')]/table/tbody[last()]/tr[1]/td/em[last()]").text.strip()
        print('--------' + currPer + '--------' + period)

        # 判断上一期是否盈利
        isWin = logLastResult == getResult(period)

        # 打印日志
        if isWin:
            print('【盈利】投入[' + boolToStr(logLastResult) + ']金额:' + str(logLastMoney))
        else:
            print('【亏损】投入[' + boolToStr(logLastResult) + ']金额:' + str(logLastMoney))

        # 计算下期投入
        if isWin:
            # 盈利
            # 重置投入
            nexMoney = baseMoney
        else:
            # 亏损，加倍投入
            if logLastMoney == 0:
                logLastMoney = 1
            nexMoney = logLastMoney * 2

        if nexMoney >= 8:
            nexMoney = 8

        if isWin:
            totalMoney = totalMoney + logLastMoney * fee - nexMoney
        else:
            # 计算当前余额
            totalMoney = totalMoney - logLastMoney - nexMoney

        # 处理黑幕次数
        if isWin:
            repeat = 0
        else:
            repeat += 1
        if repeat >= maxrepeat:
            nexResult = True if not logLastResult else False
            repeat = 0
        try:
            tre = float(getTreasure().strip())
        except Exception:
            tre = 999

        if tre < nexMoney:
            browser.quit()
            print('资金不足')
            Mail.send('资金不足')
            break

        # 投入操作
        while True:
            if shopIn(nexMoney, nexResult):
                break
            else:
                browser.refresh()
                time.sleep(0.5)
                shopIn(nexMoney, nexResult)

        # 记录本次投入
        logLastMoney = nexMoney
        # 记录下期预测的结果
        logLastResult = nexResult
        # 记录下一期数
        logNexPre = nexPer

        count += 1
    else:
        # 记录下一期数
        logNexPre = nexPer
        # 没到下一期，那就继续监听，直到下一期
        continue
