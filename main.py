import time

from crawler_web import GetDailyMachine

if __name__ == '__main__':
    while True:
        machine = GetDailyMachine(show_web=False)
        # print(machine.check_all_done())
        # update stock_list.json
        # machine.update_stocks()

        # get data
        machine.open_web()

        done = False
        while not done:
            try:
                machine.get_stocks_data()
                print(machine.check_all_done())
                time.sleep(5)
                if machine.check_all_done():
                    done = True
            except Exception as e:
                machine.refresh_driver()
                # machine.open_web()
                print(f'error {e}')
        machine.close_web()
        del machine
        time.sleep(60 * 60 * 24)
