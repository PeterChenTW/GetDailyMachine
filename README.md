## 
 modify config.ini

##提升準確率 
 需要修改pytesseract config 
## 驗證碼似乎只會出現 
 2346789ACDEFGHJKLNPQRTUVXYZ
https://my.oschina.net/u/2396236/blog/1621590


### DB information
### 透過 ssh -N -L 3306:localhost:3306 username@阿里IP
    IP:localhost
    Port:3306
    User: root 
    Password: password
    DB: stock

2020/5/31
1. error
    error: (-215:Assertion failed) dims <= 2 && step[0] > 0 in function 'locateROI'
    time sleep one second after bot has saved the captcha

    OSError: [Errno 23] Too many open files in system
    sudo ulimit -n 4096
    ulimt -a -> 可以看limit

2. 更新股票代碼的方式
https://leemeng.tw/beautifulsoup-cheat-sheet.html

3. 新增 exceed deal

2020/06/01
1. auto save captcha if the captcha pass

2020/06/02
更新版本: 移除pyautogui
把錯的captcha 存入 captcha_data/error

todo: linux use method
https://www.cnblogs.com/ZFBG/p/10997040.html

2020/06/03
add mysql
https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html

selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: crashed.
  (chrome not reachable)
  (The process started from chrome location /Applications/Google Chrome.app/Contents/MacOS/Google Chrome is no longer running, so ChromeDriver is assuming that Chrome has crashed.)
