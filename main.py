from handle_web import GetDailyMachine

if __name__ == '__main__':
    machine = GetDailyMachine()
    machine.open_web()
    machine.get_stocks_data()
