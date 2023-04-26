import PN532_UART as NFC

# pn532 = NFC.PN532("/dev/ttyUSB0")
pn532 = NFC.PN532("COM3")

ic, ver, rev, support = pn532.get_firmware_version()
print('\nFound PN532 with firmware version: {0}.{1}'.format(ver, rev))

menu_options = {
    1: 'Read UID',
    2: 'Read Mifare sector 0',
    3: 'Read NTAG 2xx (first 16 sectors)',
    4: 'Exit',
}


def read_uid():
    print('Reading...')
    print('CRTL+C or remove tag to stop')

    uid = True
    while uid:
        try:
            uid = pn532.read_passive_target(timeout=1000)
        except RuntimeError as e:
            print(str(e))
            return
        except KeyboardInterrupt:
            return

        if uid:
            print("".join("%02X:" % i for i in uid)[:-1])
        else:
            print("No card in the field!")


def read_mifare():
    print('Reading...')
    uid = pn532.read_passive_target(timeout=1000)
    if uid:
        print("uid:", "".join("%02X:" % i for i in uid)[:-1], "\n")

        for i in range(4):
            try:
                if pn532.mifare_classic_authenticate_block(uid, i):
                    block = pn532.mifare_classic_read_block(i)
                    if block:
                        print("block %02d =" % i, ("".join("%02X:" % j for j in block))[:-1])
                    else:
                        print("block %02d" % i, "read error")
                else:
                    print("block %02d" % i, "authentication error")
            except Exception as e:
                print(str(e))
    else:
        print("No card in the field!")


def read_ntag():
    print('Reading...')
    uid = pn532.read_passive_target(timeout=1000)
    if uid:
        print("uid:", "".join("%02X:" % i for i in uid)[:-1], "\n")

        for i in range(16):
            try:
                block = pn532.ntag2xx_read_block(i)
                readable = ""

                if block:
                    for j in block:
                        if 31 < j < 128:
                            readable += chr(j)
                        else:
                            readable += '.'
                    print("block %02d" % i, ("".join("%02X:" % j for j in block))[:-1], readable)
                else:
                    print("block %02d" % i, "None")
            except RuntimeError:
                break
    else:
        print("No card in the field!")


def print_menu():
    print('\n')
    for key in menu_options.keys():
        print(key, '--', menu_options[key])
    print()


def main():

    while True:
        print_menu()
        try:
            option = int(input('Enter your choice: '))
        except KeyboardInterrupt:
            continue
        except ValueError:
            option = None

        if option == 1:
            read_uid()
        elif option == 2:
            read_mifare()
        elif option == 3:
            read_ntag()
        elif option == 4:
            print('Bye!')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')


main()
