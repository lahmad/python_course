import re
import argparse

def calculate_sum(filename):
    """ Reads the file and count the numbers encountered in the file using re
        Args:
            filename (str): The relative path for the file to open
        Returns:
            int: Sum of the numbers
    """
    if filename is None:
        print("Filename cannot be empty / null")
        return

    total_sum = 0
    try:
        file_handler = open(filename)
        for line in file_handler:
            line = line.rstrip()
            numbers = re.findall("[0-9]+", line)

            for number in numbers:
                number = int(number)
                total_sum += number
    except:
        print("File {} cannot be found".format(filename))
        raise FileNotFoundError("File {} cannot be found".format(filename))
    finally:
        if not file_handler:
            file_handler.close()

    return total_sum

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="File name")
    parser.add_argument("--file", help="Relative path of file")
    args = parser.parse_args()
    if args.file is None:
        print("Need to enter the relative file regex_sum_42.txt or regex_sum_175111.txt")
    else:
        try:
            sum_of_numbers = calculate_sum(args.file)
            print("Sum of numbers is  %d" % (sum_of_numbers))
        except:
            print("Error : quiting")
