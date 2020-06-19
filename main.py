import time

import schedule

from crawler_web import GetDailyMachine


def job():
    machine = GetDailyMachine(show_web=False)
    # print(machine.check_all_done())
    # update stock_list.json
    # machine.update_stocks()

    # get data
    machine.open_web()

    done = False
    error = 0
    while not done:
        try:
            machine.get_stocks_data()
            print(machine.check_all_done())
            time.sleep(5)
            if machine.check_all_done():
                done = True
        except Exception as e:
            error += 1
            if error % 20:
                machine.refresh_driver()
            else:
                machine.open_web()
            print(f'error {e}')
    machine.close_web()
    del machine


start_time = input('you want to start time. 09:00')
schedule.every().day.at('09:00').do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
