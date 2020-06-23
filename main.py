import time

import schedule

from crawler_web import GetDailyMachine


def job():
    done = False
    error = 0
    machine = GetDailyMachine(show_web=False)
    # print(machine.check_all_done())
    # update stock_list.json
    # machine.update_stocks()

    # get data
    machine.open_web()

    while not done:
        try:
            machine.get_stocks_data()
            time.sleep(100)
            print(machine.check_all_done())
            if machine.check_all_done():
                print('over!')
                done = True
        except Exception as e:
            error += 1
            if error % 20:
                machine.refresh_driver()
            else:
                machine.open_web()
            print(f'error {e}')
    machine.close_web()
    del machine, done, error


start_time = input('you want to start time. 09:00:')
schedule.every().day.at(start_time).do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
