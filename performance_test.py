#!/usr/bin/env python
# **********************************************************************
# Copyright (c) 2020 Telefonaktiebolaget LM Ericsson, Sweden.
# All rights reserved.
# The Copyright to the computer program(s) herein is the property of
# Telefonaktiebolaget LM Ericsson, Sweden.
# The program(s) may be used and/or copied with the written permission
# from Telefonaktiebolaget LM Ericsson or in accordance with the terms
# and conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
# **********************************************************************

import time
from datetime import datetime, timedelta
from threading import Thread

def threaded_method(name):
    start_time = datetime.now()
    timeout = timedelta(seconds=5)
    now = datetime.now()
    while now - start_time <= timeout:
        now = datetime.now()
        print(f"this is thread {name} and so far it has been {now - start_time} seconds")
        time.sleep(1)


if __name__ == "__main__":
    thread1 = Thread(target=threaded_method, args=["thread1"])
    thread2 = Thread(target=threaded_method, args=["thread2"])

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()