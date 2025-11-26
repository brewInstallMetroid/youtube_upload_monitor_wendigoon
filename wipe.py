#!/usr/bin/env python3
import sys

def main():
        
    options = ["goon", "gang", "cast", "all"]


    try:
        if len(sys.argv) != 2 or sys.argv[1] not in options:
            raise IndexError

        if sys.argv[1] == "goon":
            with open("goon_storage.txt", "w") as goon_write:
                goon_write.write("")
                print("GOON FILE WIPED SUCCESSFULLY")

        elif sys.argv[1] == "gang":
            with open("gang_storage.txt", "w") as gang_write:
                gang_write.write("")
                print("GANG FILE WIPED SUCCESSFULLY")

        elif sys.argv[1] == "cast":
            with open("cast_storage.txt", "w") as cast_write: 
                cast_write.write("")
                print("CAST FILE WIPED SUCCESSFULLY")

        elif sys.argv[1] == "all":
            with open("goon_storage.txt", "w") as goon_write:
                with open("gang_storage.txt", "w") as gang_write:
                    with open("cast_storage.txt", "w") as cast_write:
                        goon_write.write("")
                        gang_write.write("")
                        cast_write.write("")
                        print("ALL FILES WIPED SUCCESSFULLY")
                              
    except IndexError:
        print("IMPROPER USAGE!")
        exit("Usage: ./wipe.py goon OR gang OR cast OR all")


if __name__ == "__main__":
    main()
                