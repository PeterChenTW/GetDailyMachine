if __name__ == '__main__':
    from crawler_web import GetDailyMachine

    machine = GetDailyMachine(show_web=False)
    machine.check_all_done()
