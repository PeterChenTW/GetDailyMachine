if __name__ == '__main__':
    from crawler_web import GetDailyMachine
    import os

    machine = GetDailyMachine(show_web=False)
    check_set = set(machine.stocks) - set([i[:4] for i in os.listdir(machine.daily_path)] + list(machine.no_data))
    print(check_set)
