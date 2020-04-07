import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox

def toBinary(dec): #function returning binary number, for converting octets to binary
    return bin(int(dec))[2:].zfill(8)
def toDecimal(bin): #function returning decimal number, for converting octets to decimal
    return str(int(bin,2))
def subnetBinary(prefix): #function for computing subnet mask in binary based on prefix
    subnet = ''
    for i in range(32):
        if i%8 == 0 and i != 0: subnet+='.'
        if prefix > 0: subnet+='1'
        else: subnet+='0'
        prefix-=1
    return subnet

class NetworkAddressing:
    def __init__(self,addressPrefix): #constructors
        self.addressBinary = '.'.join(list(map(toBinary,(addressPrefix.split("/")[0]).split(".")))) #ip address in binary
        self.prefixDecimal = int(addressPrefix.split("/")[1]) #prefix length
        self.prefixBinary = subnetBinary(self.prefixDecimal) #subnet mask in binary
    def networkAddress(self): #logical ANDing for finding network address
        address = ''
        for i in range(35):
            if self.addressBinary[i] == '.' and self.prefixBinary[i] == '.':
                address+='.'
                continue
            if self.addressBinary[i] == '1' and self.prefixBinary[i] == '1':
                address+='1'
            else:
                address+='0'
        return '.'.join(list(map(toDecimal,address.split(".")))) + '/' + str(self.prefixDecimal)
    def subnetMask(self): #returns subnet mask in decimal
        return '.'.join(list(map(toDecimal,self.prefixBinary.split("."))))
    def firstHost(self): #returns first host address
        address = ''
        # network address with last bit equal to 1
        networkAddress = '.'.join(list(map(toBinary,(self.networkAddress().split("/")[0]).split("."))))[:-1] + '1'
        firsthost = '11111111.11111111.11111111.11111111'
        for i in range(35): #logical ANDing
            if networkAddress[i] == '.' and firsthost[i] == '.':
                address+='.'
                continue
            if networkAddress[i] == '1' and firsthost[i] == '1': address+='1'
            else: address+='0'
        return '.'.join(list(map(toDecimal,address.split(".")))) + '/' + str(self.prefixDecimal)
    def lastHost(self):
        address = ''
        #network address with host portion equal to 1 except last bit
        networkAddress = '.'.join(list(map(toBinary,(self.networkAddress().split("/")[0]).split("."))))[::-1].replace('0','1',32-self.prefixDecimal)[::-1][:-1] + '0'
        lasthost = '11111111.11111111.11111111.11111111'
        for i in range(35):
            if networkAddress[i] == '.' and lasthost[i] == '.':
                address+='.'
                continue
            if networkAddress[i] == '1' and lasthost[i] == '1': address+='1'
            else: address+='0'
        return '.'.join(list(map(toDecimal,address.split(".")))) + '/' + str(self.prefixDecimal)
    def broadcast(self):
        address = ''
        #host portion is equal to all 1s
        networkAddress = '.'.join(list(map(toBinary,(self.networkAddress().split("/")[0]).split("."))))[::-1].replace('0','1',32-self.prefixDecimal)[::-1]
        broadcast = '11111111.11111111.11111111.11111111'
        for i in range(35):
            if networkAddress[i] == '.' and broadcast[i] == '.':
                address+='.'
                continue
            if networkAddress[i] == '1' and broadcast[i] == '1': address+='1'
            else: address+='0'
        return '.'.join(list(map(toDecimal,address.split(".")))) + '/' + str(self.prefixDecimal)
    def numberHosts(self):
        return '{:,.2f}'.format(2**(self.prefixBinary.count('0'))-2)[:-3]

self = tk.Tk() #creating window

#background image (cisco)
image = ImageTk.PhotoImage(file="background.png")
background = tk.Label(self,image=image)
background.place(x=-2,y=-2)

#window icon
windowIcon = ImageTk.PhotoImage(file='ciscoLogo.png')
self.iconphoto(False,windowIcon)

#-----------------Labels------------------#
input = tk.Label(self,text='Enter IP Address with Prefix Length: ',font=("Calibri",20,'bold'),fg='#09383d',bg='#ffffff')
input.place(x=20,y=95)

network = tk.Label(self,text='Network Address: ',font=("Calibri",20,'bold'),fg='#09383d',bg='#ffffff')
network.place(x=20,y=145)

subnet = tk.Label(self,text='Subnet Mask: ',font=("Calibri",20,'bold'),fg='#09383d',bg='#ffffff')
subnet.place(x=20,y=195)

firstHost = tk.Label(self,text='First Host Address: ',font=("Calibri",20,'bold'),fg='#09383d',bg='#ffffff')
firstHost.place(x=20,y=245)

lastHost = tk.Label(self,text='Last Host Address: ',font=("Calibri",20,'bold'),fg='#09383d',bg='#ffffff')
lastHost.place(x=20,y=295)

broadcast = tk.Label(self,text='Broadcast Address: ',font=("Calibri",20,'bold'),fg='#09383d',bg='#ffffff')
broadcast.place(x=20,y=345)

hosts = tk.Label(self,text='Number of Hosts: ',font=("Calibri",20,'bold'),fg='#09383d',bg='#ffffff')
hosts.place(x=20,y=395)

#------------Output Labels-----------------#
networkOutput = tk.Label(self,text='',font=("Calibri",20,'bold'),fg='#ca0f19',bg='#ffffff')
networkOutput.place(x=240,y=145)

subnetOutput = tk.Label(self,text='',font=("Calibri",20,'bold'),fg='#ca0f19',bg='#ffffff')
subnetOutput.place(x=195,y=195)

firstHostOutput = tk.Label(self,text='',font=("Calibri",20,'bold'),fg='#ca0f19',bg='#ffffff')
firstHostOutput.place(x=250,y=245)

lastHostOutput = tk.Label(self,text='',font=("Calibri",20,'bold'),fg='#ca0f19',bg='#ffffff')
lastHostOutput.place(x=245,y=295)

broadcastOutput = tk.Label(self,text='',font=("Calibri",20,'bold'),fg='#ca0f19',bg='#ffffff')
broadcastOutput.place(x=255,y=345)

hostsOutput = tk.Label(self,text='',font=("Calibri",20,'bold'),fg='#ca0f19',bg='#ffffff')
hostsOutput.place(x=240,y=395)

#Text Area
txt = tk.Entry(self,width=18,font=("Calibri",20,'bold'),fg='#09383d')
txt.config(highlightbackground="#09383d", highlightthickness=2)
txt.focus()
txt.place(x=440,y=95)

def validate(addressValidate): #function for validating the range for octets and prefix
    address = (addressValidate.split("/")[0]).split(".")
    prefix = (addressValidate.split("/")[1])
    if addressValidate.count('/') > 1:
        return True
    if len(address) != 4: return True
    for i in address:
        if int(i) < 0 or int(i) > 255:
            return True
    if prefix.find('.') != -1: return True
    if int(prefix) < 0 or int(prefix) > 30:
        return True

def clear(): #clear inputs and outputs
    txt.delete(0, 'end')
    networkOutput.config(text='')
    subnetOutput.config(text='')
    firstHostOutput.config(text='')
    lastHostOutput.config(text='')
    broadcastOutput.config(text='')
    hostsOutput.config(text='')

def getInfo(): #triggers output
    try:
        input = txt.get()
        if validate(input):
            messagebox.showinfo('Error!', 'Error Occured!')
        else:
            output = NetworkAddressing(input)
            networkOutput.config(text=output.networkAddress())
            subnetOutput.config(text=output.subnetMask())
            firstHostOutput.config(text=output.firstHost())
            lastHostOutput.config(text=output.lastHost())
            broadcastOutput.config(text=output.broadcast())
            hostsOutput.config(text=output.numberHosts())
    except:
        messagebox.showinfo('Error!', 'Error Occured!')

#--------------Buttons-------------#
getInfoButton = tk.Button(self,text='Get Info',font=("Calibri",18),fg='#09383d',command=getInfo)
getInfoButton.place(x=550,y=420)

clearButton = tk.Button(self,text='Clear',font=("Calibri",18),fg='#ca0f19',command=clear)
clearButton.place(x=650,y=420)

self.title("Simple Networking Program") #window title
self.geometry('800x500') #window size
self.resizable(False,False) #window cannot be resized
self.mainloop() #window infinite loop







