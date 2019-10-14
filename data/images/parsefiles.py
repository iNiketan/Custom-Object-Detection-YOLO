import os
img_path = "~/Downloads/volkswagen_logo/data/images"
file_list = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]
file_train = open('train.txt', 'w')

for file in file_list:
    file_train.writelines(img_path + "/" + file + "\n")
