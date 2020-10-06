from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
import json
import os, shutil

input_folder = r"C:\Users\SHRIKRISHNA\PycharmProjects\django_project\newproject\input_file"
out_folder = r"C:\Users\SHRIKRISHNA\PycharmProjects\django_project\Done"
import pandas as pd
# Create your views here.
def index(request):
    #return HttpResponse("HELLO Krishna")
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        myfilter = request.POST["filter_selection"]
        filter_value = request.POST["filter_name"]
        print(myfile.name, myfilter, filter_value)
        fs = FileSystemStorage(location=r"input_file")
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        #print(filename)
        for f_name in os.listdir(input_folder):
            if f_name.endswith('.json'):
                with open(os.path.join(input_folder, f_name)) as f:
                    json_data = json.load(f)
        #print(json_data)
        img_url = "https://d3kl9es5azf7m3.cloudfront.net/11cimages/player/default/00.png"
        finaldf = pd.DataFrame()
        for i, player_details in enumerate(json_data["data"]["site"]["tour"]["match"]["players"]):
            # dict = {}
            for key, value in player_details.items():
                # if key == "artwork":
                #   for item in player_details[key]:
                #      print(item["src"])
                # dict["artwokr"] =item["src"]
                finaldf.loc[i, "pic_url"] = img_url
                if key == "credits":
                    print(player_details[key])
                    # dict["credit"] = player_details[key]
                    finaldf.loc[i, "credit"] = player_details[key]
                if key == "name":
                    print(player_details[key])
                    # dict["name"] = player_details[key]
                    finaldf.loc[i, "name"] = player_details[key]
                if key == "type":
                    position = player_details[key]["name"]
                    if position == "ALL":
                        position = "AR"

                    print(player_details[key]["name"])
                    # dict["type"] = player_details[key]["name"]
                    finaldf.loc[i, "type"] = position

                if key == "squad":
                    # dict["squad"] = player_details[key]["name"]
                    finaldf.loc[i, "squad"] = player_details[key]["name"]

        def scname(string):
            temp = []

            for index in range(len(string.split()) - 1):
                if (len(string.split()) - 1) == 0:
                    temp.append(string.split()[index])
                else:
                    temp.append(string.split()[index][0:1].upper())

            return " ".join(temp)

        finaldf["ShortName"] = finaldf.apply(lambda row: scname(row["name"]), axis=1)
        if myfilter == "True":
             finaldf = finaldf[finaldf["squad"]==filter_value]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename='+myfile.name+'.csv'
        finaldf.to_csv(path_or_buf=response, index=False)
        #finaldf.to_csv(r"C:\Users\SHRIKRISHNA\Desktop\arun11challeger\NOR vs SER.csv", index=False)

        # move file from input folder to Done folder
        for file in os.listdir(input_folder):
            if os.path.exists(os.path.join(out_folder, file)):
                continue
            else:
                shutil.move(os.path.join(input_folder, f_name), out_folder)

        return response
        # return render(request, 'fileupload.html', {
        #     'uploaded_file_url': uploaded_file_url, 'response':response
        # })
    return render(request, "fileupload.html", )