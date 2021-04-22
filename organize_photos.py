import os;
import re;
import collections
from datetime import datetime
from PIL import Image
from PIL import UnidentifiedImageError
from shutil import copyfile
from pathlib import Path

# DECOMENTEAZA INAINTE DE FOL:
#unorganized_dir = "D:\\Poze\\unorganized"
#organized_dir = "D:\\Poze\\organized"


#get-date function
def imgDate(fn):
    "returns the image date from image (if available)\nfrom Orthallelous"
    std_fmt = '%Y:%m:%d %H:%M:%S.%f'
    # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeDigitized)
            (306, 37520), ]  # (DateTime, SubsecTime)
    exif = Image.open(fn)._getexif()
 
    for t in tags:
        dat = exif.get(t[0])
        sub = exif.get(t[1], 0)
 
        # PIL.PILLOW_VERSION >= 3.0 returns a tuple
        dat = dat[0] if type(dat) == tuple else dat
        sub = sub[0] if type(sub) == tuple else sub
        if dat != None: break
 
    if dat == None: return None
    full = '{}.{}'.format(dat, sub)
    T = datetime.strptime(full, std_fmt)
    #T = time.mktime(time.strptime(dat, '%Y:%m:%d %H:%M:%S')) + float('0.%s' % sub)
    return T

#get the directory
directory = os.fsencode(unorganized_dir)

# variables
list_of_photos = dict()

not_photos = 0
not_dated_photos = 0
dated_photos = 0

# populate list of photos
for filename in os.listdir(directory):
    #get files full location
    file_location = os.path.join(directory, filename)
    date = None
    try:
        #get files date
        date = imgDate(file_location)
    except:
        not_photos += 1
    #test if files date is empty
    if (date == None):
        date_from_name = re.findall("\d{8}", str(filename))
        #test if date is not in name
        if (not date_from_name):
            not_dated_photos += 1
            #Create a default datetime to compare with
            date = datetime(1000, 1, 1)

        #if date is in the name use that date
        else: 
            year = int(date_from_name[0][0:4])
            month = int(date_from_name[0][4:6])
            day = int(date_from_name[0][6:8])
            if (month >= 1 and month <= 12 and day >= 1 and day <= 31 and year > 2000 and year < 2030):
                date = datetime(year, month, day)
                dated_photos += 1
            else:
                not_dated_photos += 1
                #Create a default datetime to compare with
                date = datetime(1000, 1, 1)
    else: 
        dated_photos += 1
    #make a dict with filename&location as key and date as value
    list_of_photos[(filename, file_location)] = date

# order photos by date
sorted_photos = sorted(list_of_photos.items(), key=lambda kv: kv[1])
ordered_dict_of_photos = collections.OrderedDict(sorted_photos)

last_date = datetime(1000, 1, 1)
last_path = organized_dir + "\\idk"
i = 0
for k,v in ordered_dict_of_photos.items():    
    i += 1
    if (i % 100 == 0):
        print(i)
    time_difference = v - last_date
    last_date = v
    #########################
    if (time_difference.days < 2):
        path = last_path + "\\" + k[0].decode("utf-8") 
        copyfile(k[1], path)
    else:
        year = str(v.year)
        month = v.month
        if (month < 10):
            month = "0" + str(month)
        day = v.day
        if (day < 10):
            day = "0" + str(day)
        new_path = organized_dir + '\\' + str(year) + '\\' + str(month) + '-' + str(day)
        last_path = new_path
        path = new_path + '\\' + k[0].decode("utf-8")
        Path(new_path).mkdir(parents=True, exist_ok=True)
        copyfile(k[1], path)


# print (list_of_photos)
# print (sorted_dict)
print ('Elements in folder: ', len(list_of_photos))

print ('Photos: ', dated_photos)
print ('Not photos: ', not_photos) 
print ('Not dated: ', not_dated_photos) 
#print ('Total: ', dated_photos + not_dated_photos + not_photos)