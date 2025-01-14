
# reads bmp header and returns the 54 bit headerdef
def main():
    def read_header(bmp):
        with open(bmp, 'rb') as file:
            # read the first 138 bytes
            header = file.read(138)
            print(header)

    read_header('cp-logo.bmp')

if __name__ == "__main__":
    main()

