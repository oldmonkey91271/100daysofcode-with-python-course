from datetime import datetime, timedelta

# Repeat until the use selects to quit
while (1):
    what2do = input("\nPlease choose, start timer (s), else quit...")
    if (what2do.upper() == 'S'):
        starttime = datetime.now()
        print("Starting timer... " + str(starttime))
        input("Hit any key to stop timer.")
        stoptime = datetime.now()
        print("Ellapsed time is " + str(stoptime - starttime))
    else:
        print("Bye bye!")
        break
