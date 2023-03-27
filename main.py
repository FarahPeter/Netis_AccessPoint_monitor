import tkinter as tk
import threading

import requests
from ast import literal_eval
import time
import json

def find_between( s, first, last=None):
    try:
        if (last!=None):
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        else:
            start = s.index(first) + len(first)
            return s[start:]
    except ValueError:
        return ""


#get wirless client list
def GetData():
    #get data from router
    #you get the header
    headers = {}
    data = 'wl_link=0&'
    response = requests.post('http://192.168.1.254/cgi-bin/skk_get.cgi', headers=headers, data=data)
    #find wirless client list
    data=find_between(str(response.text),"'apLinkList':[",",]")
    #convert it to an array
    data="["+data+"]"
    data=(literal_eval(data))

    dataDic={}
    for i in range (len(data)):
        dataDic[str(data[i]["mac"])]=data[i]
    #print(dataDic)

    return dataDic
#newData=GetData()


def sort_dict_by_tx_rx_packets(dictionary):
    sorted_list = sorted(dictionary.items(), key=lambda x: int(x[1]['tx_packets']) + int(x[1]['rx_packets']), reverse=True)
    sorted_dict = {}
    for item in sorted_list:
        sorted_dict[item[0]] = item[1]
    return sorted_dict




def WriteToJSON(ar):
    # putting data in JSON file
    with open("customnames" + '.json', 'w') as f:
        json.dump(ar, f)




def OpenAll():
    root = tk.Tk()
    root.wm_title("All Names")
    root.geometry("600x800")



    try:
        f = open('customnames.json')
        datajson = json.load(f)
    except:
        WriteToJSON({})
        datajson = {}
    if (len(datajson)<1):
        x=tk.Label(root, text="No Data", fg="red", pady=0, padx=10, font=10, width=15)
        x.grid(row=0, column=0, columnspan=1)
    else:
        tk.Label(root, text="MAC", fg="black", pady=0, padx=10, font=10, width=15).grid(row=0, column=0,columnspan=1)
        tk.Label(root, text="Name", fg="black", pady=0, padx=10, font=10, width=15).grid(row=0, column=1,columnspan=1)
        row=1
        for i in datajson:
            tk.Label(root, text=str(i), fg="black", pady=0, padx=10, font=10, width=15).grid(row=row, column=0, columnspan=1)
            tk.Label(root, text=datajson[str(i)], fg="black", pady=0, padx=10, font=10, width=15).grid(row=row, column=1,columnspan=1)
            row=row+1

    root.mainloop()


def SaveToJson():
    root = tk.Tk()
    root.wm_title("Mac_Names")
    root.geometry("600x800")


    def getMacs():
        try:
            Data = GetData()
        except:
            Data={}
        row = 0
        try:
            f = open('customnames.json')
            datajson = json.load(f)
        except:
            WriteToJSON({})
            datajson={}
        macListInOrder=[]
        nameListInOrder=[]
        for i in Data:
            maclabel = (tk.Label(root, text=str(i), fg="black", pady=0, padx=10, font=10, width=15))
            maclabel.grid(row=row, column=0, columnspan=1)
            hostName = (tk.Label(root, text=Data[i]["host"], fg="black", pady=0, padx=10, font=10, width=25,wraplength=250))
            hostName.grid(row=row, column=1, columnspan=1)
            nameListInOrder.append((tk.Entry(root, fg="black",font=10, width=20)))
            try:
                nameListInOrder[row].insert(0, datajson[str(i)])
            except:
                nameListInOrder[row].insert(0, "")
            nameListInOrder[row].grid(row=row, column=2, columnspan=1)

            macListInOrder.append(i)
            row = row + 1

        def getinputs(macs,names,datajson):
            nameListInOrderActuale = []
            for i in range(len(names)):
                nameListInOrderActuale.append(nameListInOrder[i].get())
            for i in range (len(names)):
                datajson[str(macs[i])]=nameListInOrderActuale[i]
            WriteToJSON(datajson)

        submit = tk.Button(root, text="Save", width=20, fg="black",command=lambda: getinputs(macListInOrder,nameListInOrder,datajson))
        submit.grid(row=row, column=0)

    getMacs()


    root.mainloop()

def popupmsg(msg,tit="Warning!",size="300x80"):

    popup = tk.Tk()
    popup.geometry(size)
    popup.wm_title(tit)
    popup.resizable(width=0, height=0)
    label = tk.Label(popup, text=msg, font="NORM_FONT", wraplength=500)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    popup.mainloop()









#UI
master = tk.Tk()
master.wm_title("Netis router client checker")
master.geometry("900x400")
#master.resizable(width=0, height=0)

host =tk.Label(master,text="Host",fg="black",pady=0, padx=10, font=10,width=20)
host.grid(row=0,column=0,columnspan =1)
sentPackets =tk.Label(master,text="Transmitted packets/3s",fg="black",pady=0, padx=10, font=10,width=17)
sentPackets.grid(row=0,column=1,columnspan =1)
receivedPackets =tk.Label(master,text="Received packets/3s",fg="black",pady=0, padx=10, font=10,width=17)
receivedPackets.grid(row=0,column=2,columnspan =1)
mac =tk.Label(master,text="Mac",fg="black",pady=0, padx=10, font=10,width=15)
mac.grid(row=0,column=3,columnspan =1)
name =tk.Label(master,text="Name",fg="black",pady=0, padx=10, font=10,width=15)
name.grid(row=0,column=4,columnspan =1)




def FindPacketsPerSecond():
    oldData = {}
    while True:
        packetsPerSecondData = {}
        try:
            f = open('customnames.json')
            datajsonmain = json.load(f)
        except:
            WriteToJSON({})
            datajsonmain = {}

        try:
            newData=GetData()
        except:
            try:
                specialMap.destroy()
            except:
                pass
            newData={}
            specialMap=(tk.Label(master, text="No or Wrong internet connection", fg="red", pady=0, padx=10, font=10, width=25,wraplength=250))
            specialMap.grid(row=1, column=0, columnspan=1)

        for i in oldData:
            try:
                newdic={"id":newData[str(i)]["id"],"host":newData[str(i)]["host"],"tx_packets":str(int(newData[str(i)]["tx_packets"])-int(oldData[str(i)]["tx_packets"])),"rx_packets":str(int(newData[str(i)]["rx_packets"])-int(oldData[str(i)]["rx_packets"]))}
                packetsPerSecondData[str(i)]=newdic
            except Exception as e:
                pass
        oldData={}
        for i in newData:
            oldData[str(i)]=newData[str(i)]
        #print(packetsPerSecondData)
        #print(sort_dict_by_tx_rx_packets(packetsPerSecondData))
        sorted = sort_dict_by_tx_rx_packets(packetsPerSecondData)
        if (len(sorted)>0):
            #print(oldMap)
            for i in oldMap:
                for j in oldMap[i]:
                    #print(j)
                    j.destroy()
        oldMap={}
        if (len(sorted)>0):
            for i in map:
                oldMap[i]=map[i]
        map={"hostout":[],"sentPacketsout":[],"receivedPacketsout":[],"macout":[],"name":[]}
        row=1
        for i in sorted:
            #print("Host: " +str(sorted[i]["host"])+" ; Mac: " +str(i)+" ; transmitted packets/10s: "+str(sorted[i]["tx_packets"]) +" ; received packets/10s: "+str(sorted[i]["rx_packets"]))
            #print(str(sorted[i]["host"]) + " ; sent packets/10s: " + str(sorted[i]["tx_packets"]) + " ; received packets/10s: " + str(sorted[i]["rx_packets"])+" ; "+str(i))
            map["hostout"].append(tk.Label(master, text=str(sorted[i]["host"]), fg="black", pady=0, padx=10, font=10, width=25,wraplength=250))
            map["hostout"][row-1].grid(row=row, column=0, columnspan=1,)
            map["sentPacketsout"].append(tk.Label(master, text=str(sorted[i]["tx_packets"]), fg="black", pady=0, padx=10, font=10, width=15))
            map["sentPacketsout"][row-1].grid(row=row, column=1, columnspan=1)
            map["receivedPacketsout"].append(tk.Label(master, text=str(sorted[i]["rx_packets"]), fg="black", pady=0, padx=10, font=10, width=15))
            map["receivedPacketsout"][row-1].grid(row=row, column=2, columnspan=1)
            map["macout"].append(tk.Label(master, text=str(i), fg="black", pady=0, padx=10, font=10, width=15))
            map["macout"][row-1].grid(row=row, column=3, columnspan=1)
            try:
                map["name"].append(tk.Label(master,width=15,text=datajsonmain[str(i)]))
            except:
                map["name"].append(tk.Label(master, width=15, text=""))
            map["name"][row - 1].grid(row=row, column=4, columnspan=1)
            row=row+1

        #print("----------")
        time.sleep(3)


(threading.Thread(target=FindPacketsPerSecond)).start()


menubar = tk.Menu(master)

SaveName = tk.Menu(menubar, tearoff=0)
SaveName.add_command(label="Save Names",command=lambda: SaveToJson())
SaveName.add_command(label="View all",command=lambda: OpenAll())
menubar.add_cascade(label="Data", menu=SaveName)


helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Info",command=lambda: popupmsg("Halibe check","More info about App","200x130"))
menubar.add_cascade(label="Help", menu=helpmenu)


aboutmenu=tk.Menu(menubar, tearoff=0)
aboutmenu.add_command(label="Version",command=lambda: popupmsg("Last Updated 26/3/2023\n \n V1","Version","200x120"))
aboutmenu.add_command(label="About",command=lambda: popupmsg("By Peter Farah","About","200x80"))
menubar.add_cascade(label="About", menu=aboutmenu)


master.config(menu=menubar)
master.mainloop()
