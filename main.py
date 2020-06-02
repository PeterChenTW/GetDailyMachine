from new_handle_web import GetDailyMachine

if __name__ == '__main__':
    machine = GetDailyMachine()
    machine.open_web()
    done = False
    while not done:
        try:
            machine.get_stocks_data()
            done = True
        except Exception as e:
            machine.driver.close()
            machine.open_web()
            print(f'error {e}')
