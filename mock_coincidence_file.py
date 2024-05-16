from time import sleep
from random import randrange


def main():
    with open("c_ab.log", "a") as f:
        while True:
            f.write(f"{randrange(100, 1500)}\n")
            f.flush()
            sleep(0.5)


if __name__ == "__main__":
    main()
