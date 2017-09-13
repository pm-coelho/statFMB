import os
from .statFMB import APP_ROOT
from openpyxl import Workbook
from datetime import date

#PAY ATENTION IF PRODUCTION SERVER IS WINDOWS
#             find_folder might need atention also
UPLOAD_FOLDER = os.path.join(APP_ROOT,"tmp/")
VALIDATED_FOLDER = os.path.join(APP_ROOT,"validated/")

def save_unvalidated_file(new_file,filename):
    destination = "".join([UPLOAD_FOLDER,filename])
    print(filename)
    print (destination)
    new_file.save(destination)


def get_file_path(filename, validated):
    if validated == True:
        folder = find_folder(filename)
    else:
        folder = UPLOAD_FOLDER

    if file_exists(filename,validated):
        path = "".join([folder,filename])
    elif file_exists(filename + ".xls", validated):
        path = "".join([folder,filename + ".xls"])
    elif file_exists(filename + ".xlsx",validated):
        path = "".join([folder,filename + ".xlsx"])
    else:
        path = None

    print("OUTPUT from get_file_path: {}".format(path))
    return path


#NOTE: using /
def get_relative_folder(filename):
    full_path = get_file_path(filename,True).split("/")
    validated_path = VALIDATED_FOLDER.split("/")
    relative_folder_list = full_path[len(validated_path)-2:-1]

    relative_path = os.path.join(*relative_folder_list) + "/"
    return relative_path


def delete_file(filename,validated):
    path = get_file_path(filename,validated)
    if path != None:
        os.remove(path)
    else:
        print("PATH IS NONE")


def file_exists(filename, validated):
    if validated == True:
        folder = find_folder(filename)
    else:
        folder = UPLOAD_FOLDER

    path = "".join([folder,filename])
    if os.path.exists(path):
        return True
    else:
        return False


def copy_to_validated_folder(filename):
    unvalidated_path = get_file_path(filename = filename,validated = False)
    print(unvalidated_path)
    destination_folder = find_folder(filename = filename, create = True)
    print(destination_folder)
    extension = unvalidated_path[-4:]
    if extension == "xlsx":
        extension = ".xlsx"
    print(extension)

    destination = destination_folder + filename + extension

    print(destination)

    if unvalidated_path and destination_folder:
        os.rename(unvalidated_path,destination)
        print("=> file {} transfered to validated.".format(filename+extension))
    else:
        return None

    return destination


#NOTE: using /
def find_folder(filename, create = False):
    date = get_date(filename)
    year_folder = os.path.join(VALIDATED_FOLDER,date.strftime("%Y"))
    month_folder = os.path.join(year_folder, date.strftime("%B"))
    day_folder = os.path.join(month_folder, date.strftime("%d"))

    print ("Y: {}".format(year_folder))
    print ("M: {}".format(month_folder))
    print ("D: {}".format(day_folder))
    folder = None
    if os.path.isdir(year_folder):
        if os.path.isdir(month_folder):
            if os.path.isdir(day_folder):
                folder = day_folder + "/"
            else:
                if create:
                    os.mkdir(day_folder)
                    print("=> directory {} created".format(day_folder))
                    folder = find_folder(filename, create = create)
        else:
            if create:
                os.mkdir(month_folder)
                print("=> directory {} created".format(month_folder))
                folder = find_folder(filename, create = create)
    else:
        if create:
            os.mkdir(year_folder)
            print("=> directory {} created".format(year_folder))
            folder = find_folder(filename, create = create)

    print("OUTPUT of find_folder: {}".format(folder))
    return folder


def get_date(filename):
    try:
        year = int("20" + filename.split("_")[0].split("-")[2])
        month = int(filename.split("_")[0].split("-")[1])
        day = int(filename.split("_")[0].split("-")[0])
        date_r = date(year,month,day)
        return date_r
    except Exception as err:
        print(err)
        return None
