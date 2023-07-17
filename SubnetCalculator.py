import math
from tkinter import *

def ipToHex(ip):
    hexadecimal = ""

    for i in ip.split("."):
        if len(hex(int(i))[2:]) == 2:
            hexadecimal += hex(int(i))[2:] + "."
        elif len(hex(int(i))[2:]) == 1:
            hexadecimal += "0" + hex(int(i))[2:] + "."
        else:
            return TypeError

    return hexadecimal[:-1]

def ipToNetwork(ip):
    return binaryToIp(ipToBinary(ip)[:-8] + "00000000")

def ipToBinary(ip):
    binary = ""
    
    for i in ip.split("."):
        binary += str(bin(int(i)))[2:].zfill(8)
    
    return binary

def binaryToIp(binary):
    decimal = ""
    
    for i in [binary[i:i+8] for i in range(0, len(binary), 8)]:
        decimal += str(int(i,2)) + "."
    
    return decimal[:-1]

def ipRange(maskBits, ip):
    lower = ""
    upper = ""

    for i in range(32 - int(maskBits)):
        lower += "0"
        upper += "1"
    
    broadcast = binaryToIp(ipToBinary(ip)[:-int(32 - int(maskBits))] + upper)
    lower = lower[:-1] + "1"
    upper = upper[:-1] + "0"

    return (
        binaryToIp(ipToBinary(ip)[:-int(32 - int(maskBits))] + lower),
        binaryToIp(ipToBinary(ip)[:-int(32 - int(maskBits))] + upper),
        broadcast
        )

def isValidIP(ip):
    
    if len(ip.split(".")) != 4:
        return False
    
    for i in ip.split("."):
        if not i.isdigit():
            return False
        if int(i) < 0 or int(i) > 255:
            return False
    
    return True

def maskBitsFunction(maskBits):
    hosts = 2**(32 - int(maskBits)) - 2
    binary = ""
    subnetMask = ""

    for i in range(int(maskBits)):
        binary += "1"

    for i in range(32 - int(maskBits)):
        binary += "0"
    
    for i in [binary[i:i+8] for i in range(0, len(binary), 8)]:
        subnetMask += str(int(i,2)) + "."

    subnetMask = subnetMask[:-1]

    return (maskBits, subnetMask, hosts)

def subnetMaskFunction(subnetMask):
    binary = ""
    maskBits = 0

    for i in subnetMask.split("."):
        binary += str(bin(int(i)))[2:].zfill(8)

    for i in binary:
        if i == "1":
            maskBits += 1

    return (maskBits, subnetMask, 2**(32-maskBits) - 2)

def hostsFunction(hosts):
    maskBits = math.floor(32 - math.log2(int(hosts) + 2))
    binary = ""
    subnetMask = ""
    
    for i in range(maskBits):
        binary += "1"
    
    for i in range(32-maskBits):
        binary += "0"

    for i in [binary[i:i+8] for i in range(0, len(binary), 8)]:
        subnetMask += str(int(i,2)) + "."

    subnetMask = subnetMask[:-1]
    
    return (maskBits, subnetMask, hosts)


def resultsDataTable():
    (lowerRange, upperRange, broadcast) = ipRange(maskBitsSelection.get(), ipInput.get())
    resultsText.delete(1.0, END)
    if notationSelection.get() == "Dec":
        resultsText.insert(END, "  Network: " + ipToNetwork(ipInput.get()) + "/" + maskBitsSelection.get() + "\n"
                            + "  Netmask: " + subnetMaskSelection.get() + "\n"
                            + " IP Range: " + lowerRange + "\n"
                            + "           " + upperRange + "\n"
                            + "    Hosts: " + hostsSelection.get() + "\n"
                            + "Broadcast: " + broadcast)
    elif notationSelection.get() == "Hex":
        resultsText.insert(END, "  Network: " + ipToHex(ipToNetwork(ipInput.get())) + "/" + hex(int(maskBitsSelection.get()))[2:] + "\n"
                            + "  Netmask: " + ipToHex(subnetMaskSelection.get()) + "\n"
                            + " IP Range: " + ipToHex(lowerRange) + "\n"
                            + "           " + ipToHex(upperRange) + "\n"
                            + "    Hosts: " + hex(int(hostsSelection.get()))[2:] + "\n"
                            + "Broadcast: " + ipToHex(broadcast))
    elif notationSelection.get() == "Bin":
        resultsText.insert(END, "  Network: " + ipToBinary(ipToNetwork(ipInput.get())) + "\n"
                            + "  Netmask: " + ipToBinary(subnetMaskSelection.get()) + "\n"
                            + " IP Range: " + ipToBinary(lowerRange) + "\n"
                            + "           " + ipToBinary(upperRange) + "\n"
                            + "Broadcast: " + ipToBinary(broadcast))

window = Tk()

window.title("Subnet Calculator")

maskBitsOptions = [
    "30",
    "29",
    "28",
    "27",
    "26",
    "25",
    "24",
    "23",
    "22",
    "21",
    "20",
    "19",
    "18",
    "17",
    "16",
    "15",
    "14",
    "13",
    "12",
    "11",
    "10",
    "9",
    "8",
    "7",
    "6",
    "5",
    "4",
    "3",
    "2",
    "1"
]

subnetMaskOptions = [
    "255.255.255.252",
    "255.255.255.248",
    "255.255.255.240",
    "255.255.255.224",
    "255.255.255.192",
    "255.255.255.128",
    "255.255.255.0",
    "255.255.254.0",
    "255.255.252.0",
    "255.255.248.0",
    "255.255.240.0",
    "255.255.224.0",
    "255.255.192.0",
    "255.255.128.0",
    "255.255.0.0",
    "255.254.0.0",
    "255.252.0.0",
    "255.248.0.0",
    "255.240.0.0",
    "255.224.0.0",
    "255.192.0.0",
    "255.128.0.0",
    "255.0.0.0",
    "254.0.0.0",
    "252.0.0.0",
    "248.0.0.0",
    "240.0.0.0",
    "224.0.0.0",
    "192.0.0.0",
    "128.0.0.0"
]

hostsOptions = [
    "2",
    "6",
    "14",
    "30",
    "62",
    "126",
    "254",
    "510",
    "1022",
    "2046",
    "4094",
    "8190",
    "16382",
    "32766",
    "65534",
    "131070",
    "262142",
    "524286",
    "1048574",
    "2097150",
    "4194302",
    "8388606",
    "16777214",
    "33554430",
    "67108862",
    "134217726",
    "268435454",
    "536870910",
    "1073741822",
    "2147483646"
]


maskBitsSelection = StringVar(window, maskBitsOptions[0])
subnetMaskSelection = StringVar(window, subnetMaskOptions[0])
hostsSelection = StringVar(window, hostsOptions[0])
ipInput = StringVar(window)


ipInputText = Label(window, text="IP Address: ")
ipInputEntry = Entry(window, textvariable=ipInput)


def editIpAddress(*args):
    if isValidIP(ipInput.get()):
        ipInputEntry.config(fg="white")
        resultsDataTable()
    else:
        ipInputEntry.config(fg="red")
        resultsText.delete(1.0, END)
        resultsText.insert(END, "Invalid IP Address")

def maskBitsSelectionFunction(*args):
    (maskBits, subnetMask, hosts) = maskBitsFunction(maskBitsSelection.get())
    subnetMaskSelection.set(subnetMask)
    hostsSelection.set(hosts)
    resultsDataTable()

def subnetMaskSelectionFunction(*args):
    (maskBits, subnetMask, hosts) = subnetMaskFunction(subnetMaskSelection.get())
    maskBitsSelection.set(maskBits)
    hostsSelection.set(hosts)
    resultsDataTable()

def hostsSelectionFunction(*args):
    (maskBits, subnetMask, hosts) = hostsFunction(hostsSelection.get())
    maskBitsSelection.set(maskBits)
    subnetMaskSelection.set(subnetMask)
    resultsDataTable()

ipInput.trace_add("write", editIpAddress)
maskBitsSelection.trace_add("write", maskBitsSelectionFunction)
subnetMaskSelection.trace_add("write", subnetMaskSelectionFunction)
hostsSelection.trace_add("write", hostsSelectionFunction)



ipInputText.grid(row=0, column=0, sticky=E)
ipInputEntry.grid(row=0, column=1, sticky=W)

maskBitsText = Label(window, text="Mask Bits: ")
maskBitsDropDown = OptionMenu(window, maskBitsSelection, *maskBitsOptions)
maskBitsText.grid(row=1, column=0, sticky=E)
maskBitsDropDown.grid(row=1, column=1, sticky=W)

subnetMaskText = Label(window, text="Subnet Mask: ")
subnetMaskDropDown = OptionMenu(window, subnetMaskSelection, *subnetMaskOptions)
subnetMaskText.grid(row=2, column=0, sticky=E)
subnetMaskDropDown.grid(row=2, column=1, sticky=W)

hostsText = Label(window, text="Hosts: ")
hostsDropDown = OptionMenu(window, hostsSelection, *hostsOptions)
hostsText.grid(row=3, column=0, sticky=E)
hostsDropDown.grid(row=3, column=1, sticky=W)

notationSelection = StringVar(window, "Dec")

R1 = Radiobutton(window, text="Dec", variable=notationSelection, value="Dec", command=resultsDataTable)
R2 = Radiobutton(window, text="Hex", variable=notationSelection, value="Hex", command=resultsDataTable)
R3 = Radiobutton(window, text="Bin", variable=notationSelection, value="Bin", command=resultsDataTable)

R1.grid(row=4, column=0)
R2.grid(row=4, column=1)
R3.grid(row=4, column=2)

resultsText = Text(window, height=6, width=50)
resultsText.grid(row=5, column=0, columnspan=3)

window.mainloop()