from ads_communication_module import read_twincat_variable,write_twincat_variable



def fast_loop(period, event_f, lock, plc, fHandle):
    while not event_f.wait(period):
        with lock:
            var = read_twincat_variable(fHandle, plc)
            print(var)



def slow_loop(period, event_s, lock, plc):
    while not event_s.wait(period):
        with lock:
            write_twincat_variable("MAIN.iCounter", 0, plc)
            print('counter 0')
