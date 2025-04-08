from DrissionPage import ChromiumPage
import datetime
import time

# 打开调试端口连接浏览器（务必先运行带 --remote-debugging-port 的浏览器）
page = ChromiumPage(9224)

# 设置抢购时间（格式：年-月-日 时:分:秒.微秒）
kill_time = "2025-04-08 12:00:00.000000"

# 打开购物车页面（跳过点击）
print(" 正在跳转到购物车页面...")
page.get("https://cart.jd.com/cart_index")
print(" 成功进入购物车页面，等待加载...")

# 等待购物车加载完成
try:
    page.wait.ele_displayed('x://input[@type="checkbox" and contains(@clstag, "cart_check_all")]', timeout=2)
    print(" 购物车已加载完成。")
except Exception as e:
    print(f" 等待购物车页面失败：{e}")
    page.get_screenshot('error_cart_wait.png')
    exit()

#  抢购主循环
while True:
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(f" 当前时间：{now}")

    if now > kill_time:
        try:
            # 全选购物车商品
            checkbox = page.ele('x://input[@type="checkbox" and contains(@clstag, "cart_check_all")]')
            while checkbox and checkbox.attr('clstag').split('|')[-1].startswith('0'):
                checkbox.click()
                time.sleep(0.01)
                checkbox = page.ele('x://input[@type="checkbox" and contains(@clstag, "cart_check_all")]')
            print(" 已全选购物车商品，准备点击结算...")

            # 点击“去结算”
            page.ele('去结算').click()
            print(" 点击去结算成功，等待提交订单...")

            # 等待提交订单按钮
            page.wait.ele_displayed('x://*[@id="order-submit"]/b', timeout=3)
            page.ele('x://*[@id="order-submit"]/b').click()
            print(" 已点击提交订单，准备支付...")

            # 尝试点击“立即支付”
            page.ele('立即支付', timeout=5).click()
            print(" 已点击立即支付按钮")

            # （可选）自动输入支付密码 —— 自行开启
            # page.ele('x://*[@id="validateShortFake"]').input("123456")
            # page.ele('x://*[@id="baseMode"]/div/div[2]/div/div[2]/div/div/div[1]').click()

            break
        except Exception as e:
            print(f" 抢购出错：{e}")
            page.get_screenshot('error_during_kill.png')
            input(" 抢购失败，请手动处理后按下回车继续...")

    # 整分钟刷新，保持登录活跃
    if datetime.datetime.now().second == 0:
        try:
            page.refresh()
            print(" 页面已刷新，保持登录状态")
            page.wait.ele_displayed('x://input[@type="checkbox" and contains(@clstag, "cart_check_all")]', timeout=5)
        except:
            continue

#  成功提示
input(" 恭喜你，抢购流程已完成！按任意键退出...")
