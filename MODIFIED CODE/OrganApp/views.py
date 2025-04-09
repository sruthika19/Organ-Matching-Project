from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import json
from web3 import Web3, HTTPProvider
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import random
from datetime import date
import smtplib
from email.message import EmailMessage




one={
    'from':'0x1cB8fda14C61b640c44c9416EB0947A99F188374' # Default Ethereum account used for transactions
}
global user, hospital

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================2222")
    blockchain_address = 'http://127.0.0.1:7545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'blocks/build/contracts/Organ.json' #Organ contract code
    deployed_contract_address = '0x68030a2371Ef3Ce2d52d52126FB350868BDd8A4F' #hash address to access Organ contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'signup':
        details = contract.functions.getUser().call(one)
    if contract_type == 'donor':
        details = contract.functions.getDonor().call(one)
    if contract_type == 'patient':
        details = contract.functions.getPatient().call(one)
    print("Details Loader",details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'blocks/build/contracts/Organ.json' #Organ contract file
    deployed_contract_address = '0x68030a2371Ef3Ce2d52d52126FB350868BDd8A4F' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.addUser(details).transact(one)
    if contract_type == 'donor':
        details+=currentData
        msg = contract.functions.setDonor(details).transact(one)
    if contract_type == 'patient':
        details+=currentData
        msg = contract.functions.setPatient(details).transact(one)
   

def updateConsent(currentData, contract_type):
    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'blocks/build/contracts/Organ.json' #organ contract file
    deployed_contract_address = '0x68030a2371Ef3Ce2d52d52126FB350868BDd8A4F' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    if contract_type == "donor":
        msg = contract.functions.setDonor(currentData).transact(one)
    else:
        msg = contract.functions.setPatient(currentData).transact(one)

def Alert(request):
    if request.method == 'GET':
        global user
        pid = request.GET.get('pid', False)
        did = request.GET.get('did', False)
        record = ''
        mailOf=""
        
        readDetails("patient")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            
            if arr[0] != pid:
                record += rows[i]+"\n"
            else:
                
                record += arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+arr[4]+"#"+arr[5]+"#"+arr[6]+"#"+arr[7]+"#"+arr[8]+"#Donor "+did+" Matched\n"
                mailOf=arr[10]

        updateConsent(record, "patient")

        record = ''
        readDetails("donor")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] != did:
                record += rows[i]+"\n"
            else:
                print(record)
                record += arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+arr[4]+"#"+arr[5]+"#"+arr[6]+"#"+arr[7]+"#"+arr[8]+"#Patients "+pid+" Matched\n"
        updateConsent(record, "donor")

        context= {'data':"Alert Sent to both Patinet : "+pid+" & Donor : "+did+" About Matched"}
        print(mailOf)
        receiver_email=mailOf
        subject=f"Alert From Hospital"
        body=f"We Have Find Your Matched Donor and You Can Contact to Hospital for Further Process"
        msg=EmailMessage()
        msg['Subject']=subject
        msg['From']=sender_email
        msg['To']=receiver_email
        msg.set_content(body)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com',465)as smtp:
                smtp.login(sender_email,app_passwordd)
                smtp.send_message(msg)
            print("✅ Email Sent")
        except Exception as e:
            print(f"❎ Sorry Email is Not {e}")
        return render(request, 'HospitalScreen.html', context)
                

def MatchOrganAction(request):
    if request.method == 'GET':
        global user
        pid = request.GET.get('pid', False)
        organs = request.GET.get('organs', False)
        columns = ['Donor ID', 'Donor Name', 'Address', 'Contact No', 'Health Condition & Donating Organs', 'Aadhar No', 'Hospital', 'Entry Date', 'Alert User & Donor About Matching']
        output = "<table border=1 align=center>"
        font = '<font size="" color="black">'
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"
        readDetails("donor")
        rows = details.split("\n")

        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            print(arr,"dhfjdhfjdf")
            if arr[4] in organs:
                if arr[9] == 'Pending':
                    output+='<tr><td>'+font+str(arr[0])+'</td>'
                    output+='<td>'+font+str(arr[1])+'</td>'
                    output+='<td>'+font+str(arr[2])+'</td>'
                    output+='<td>'+font+str(arr[3])+'</td>'
                    output+='<td>'+font+str(arr[4])+'</td>'
                    # output+='<td>'+font+str(arr[5])+'</td>'
                    output+='<td>'+font+str(arr[6])+'</td>'
                    output+='<td>'+font+str(arr[7])+'</td>'
                    output+='<td>'+font+str(arr[8])+'</td>'
                    output+='<td><a href=\'Alert?pid='+str(pid)+'&did='+str(arr[0])+'\'><font size=3 color=black>Send Alert</font></a></td></tr>'                
        output += "<tr></tr><tr></tr><tr></tr><tr></tr><tr></tr>"
        context= {'data':output}
        return render(request, 'HospitalScreen.html', context)                 
        

def MatchOrgans(request):
    if request.method == 'GET':
    
        columns = ['Patient ID', 'Patient Name', 'Address', 'Contact No', 'Disease History', 'Required Organs', 'Aadhar No', 'Hospital', 'Entry Date', 'Match Organs']
        output = "<table border=1 align=center>"
        font = '<font size="" color="black">'
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"
        readDetails("patient")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[7] == hospital:
                 if arr[9] == 'Pending':

                     output+='<tr><td>'+font+str(arr[0])+'</td>'
                     output+='<td>'+font+str(arr[1])+'</td>'
                     output+='<td>'+font+str(arr[2])+'</td>'
                     output+='<td>'+font+str(arr[3])+'</td>'
                     output+='<td>'+font+str(arr[4])+'</td>'
                     output+='<td>'+font+str(arr[5])+'</td>'
                     output+='<td>'+font+str(arr[6])+'</td>'
                     output+='<td>'+font+str(arr[7])+'</td>'
                     output+='<td>'+font+str(arr[8])+'</td>'
                     output+='<td><a href=\'MatchOrganAction?pid='+str(arr[0])+'&organs='+str(arr[5])+'\'><font size=3 color=black>Click Here to Match Organs</font></a></td></tr>'                
        output += "<tr></tr><tr></tr><tr></tr><tr></tr><tr></tr>"
        context= {'data':output}
        return render(request, 'HospitalScreen.html', context)

def ViewTransplant(request):
    if request.method == 'GET':
        print(hospital,"ksdfdsf")
        columns = ['Patient ID', 'Patient Name', 'Address', 'Contact No', 'Disease History', 'Required Organs', 'Aadhar No', 'Hospital', 'Entry Date', 'Transplant Status']
        output = "<table border=1 align=center>"
        font = '<font size="" color="black">'
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"
        readDetails("patient")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[9] != 'Pending':
                if arr[7] == hospital:
                    output+='<tr><td>'+font+str(arr[0])+'</td>'
                    output+='<td>'+font+str(arr[1])+'</td>'
                    output+='<td>'+font+str(arr[2])+'</td>'
                    output+='<td>'+font+str(arr[3])+'</td>'
                    output+='<td>'+font+str(arr[4])+'</td>'
                    output+='<td>'+font+str(arr[5])+'</td>'
                    output+='<td>'+font+str(arr[6])+'</td>'
                    output+='<td>'+font+str(arr[7])+'</td>'
                    output+='<td>'+font+str(arr[8])+'</td>'
                    output+='<td>'+font+str(arr[9])+'</td></tr>'                
        output += "<tr></tr><tr></tr><tr></tr><tr></tr><tr></tr>"
        context= {'data':output}
        print(output)   
        return render(request, 'HospitalScreen.html', context)

def ViewRequestStatus(request):
    if request.method == 'GET':
        global user
        columns = ['Patient ID', 'Patient Name', 'Address', 'Contact No', 'Disease History', 'Required Organs', 'Aadhar No', 'Hospital', 'Entry Date', 'Transplant Status']
        output = "<table border=1 align=center>"
        font = '<font size="" color="black">'
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"
        readDetails("patient")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if user == arr[0]:
                output+='<tr><td>'+font+str(arr[0])+'</td>'
                output+='<td>'+font+str(arr[1])+'</td>'
                output+='<td>'+font+str(arr[2])+'</td>'
                output+='<td>'+font+str(arr[3])+'</td>'
                output+='<td>'+font+str(arr[4])+'</td>'
                output+='<td>'+font+str(arr[5])+'</td>'
                output+='<td>'+font+str(arr[6])+'</td>'
                output+='<td>'+font+str(arr[7])+'</td>'
                output+='<td>'+font+str(arr[8])+'</td>'
                if arr[9] != 'Pending':
                    output+='<td>'+font+"Matched"+'</td>'
                else:
                    output+='<td>'+font+str(arr[9])+'</td></tr>'                
        output += "<tr></tr><tr></tr><tr></tr><tr></tr><tr></tr>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def DonationStatus(request):
    if request.method == 'GET':
        global user
        pid = request.GET.get('pid', False)
        organs = request.GET.get('organs', False)
        columns = ['Donor ID', 'Donor Name', 'Address', 'Contact No', 'Health Condition & Donating Organs', 'Aadhar No', 'Hospital', 'Entry Date', 'Match Status']
        output = "<table border=1 align=center>"
        font = '<font size="" color="black">'
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"
        readDetails("donor")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if user == arr[0]:
                output+='<tr><td>'+font+str(arr[0])+'</td>'
                output+='<td>'+font+str(arr[1])+'</td>'
                output+='<td>'+font+str(arr[2])+'</td>'
                output+='<td>'+font+str(arr[3])+'</td>'
                output+='<td>'+font+str(arr[4])+'</td>'
                # output+='<td>'+font+str(arr[5])+'</td>'
                output+='<td>'+font+str(arr[6])+'</td>'
                output+='<td>'+font+str(arr[7])+'</td>'
                output+='<td>'+font+str(arr[8])+'</td>'
                if arr[9] != 'Pending':
                    output+='<td>'+font+"Matched"+'</td>'
                else:
                    output+='<td>'+"Matched"+'</td></tr>'                
        output += "<tr></tr><tr></tr><tr></tr><tr></tr><tr></tr>"
        context= {'data':output}
        return render(request, 'DonorScreen.html', context)       
sender_email="reenasultanapattan@gmail.com"
app_passwordd="tjajjyzhsauqebsi"
        
def AddDonorHistoryAction(request):
    if request.method == 'POST':
        global hospital
        donor = request.POST.get('t1', '')
        address = request.POST.get('t2', '')
        contact = request.POST.get('t3', '')
        condition = request.POST.get('t4', '')
        organs = request.POST.get('t5', '')
        aadhar = request.POST.get('t6', '')
        mail=request.POST.get('mail','')
        today = date.today()
        readDetails("donor")
        rows = details.split("\n")
        did = len(rows)
        if did == 0:
            did = 1
        donor_id = donor+"-"+str(did)
        data = donor_id+"#"+donor+"#"+address+"#"+contact+"#"+condition+"#"+organs+"#"+aadhar+"#"+hospital+"#"+str(today)+"#Pending\n"
        
        saveDataBlockChain(data,"donor")
        
        receiver_email=mail
        subject=f"A Unique Id From {hospital}"
        body=f"Your Credentails from hospital \n and your Credentails are {donor_id}"
        msg=EmailMessage()
        msg['Subject']=subject
        msg['From']=sender_email
        msg['To']=receiver_email
        msg.set_content(body)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com',465)as smtp:
                smtp.login(sender_email,app_passwordd)
                smtp.send_message(msg)
            print("✅ Email Sent")
        except Exception as e:
            print(f"❎ Sorry Email is Not {e}")
        
        context= {'data':'Donor Details Added with ID : '+donor_id+"<br/>Use above Donor Id for login"}
        
        return render(request, 'AddDonorHistory.html', context)

def AddDonorHistory(request):
    if request.method == 'GET':
       return render(request, 'AddDonorHistory.html', {})    
    
def AddPatientHistoryAction(request):
    if request.method == 'POST':
        global hospital
        patient = request.POST.get('t1', False)
        address = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        disease = request.POST.get('t4', False)
        organs = request.POST.get('t5', False)
        aadhar = request.POST.get('t6', False)
        mail = request.POST.get('mail', False)
        today = date.today()
        readDetails("patient")
        rows = details.split("\n")
        pid = len(rows)
        if pid == 0:
            pid = 1
        patient_id = patient+"-"+str(pid)
        
        data = patient_id+"#"+patient+"#"+address+"#"+contact+"#"+disease+"#"+organs+"#"+aadhar+"#"+hospital+"#"+str(today)+"#Pending"+f"#{mail}\n"
        saveDataBlockChain(data,"patient")
        receiver_email=mail
        subject=f"A Unique Id From {hospital}"
        body=f"Your Credentails from hospital {hospital} \n and your Credentails are {patient_id}"
        msg=EmailMessage()
        msg['Subject']=subject
        msg['From']=sender_email
        msg['To']=receiver_email
        msg.set_content(body)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com',465)as smtp:
                smtp.login(sender_email,app_passwordd)
                smtp.send_message(msg)
            print("✅ Email Sent")
        except Exception as e:
            print(f"❎ Sorry Email is Not {e}")
        
        
        
        context= {'data':'Patient Details Added with ID : '+patient_id+"<br/>Use above Patient Id for login"}
        return render(request, 'AddPatientHistory.html', context)

def AddPatientHistory(request):
    if request.method == 'GET':
       return render(request, 'AddPatientHistory.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def HospitalLogin(request):
    if request.method == 'GET':
       return render(request, 'HospitalLogin.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def DonorLogin(request):
    if request.method == 'GET':
       return render(request, 'DonorLogin.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})    

def checkUser(username):
    flag = False
    readDetails("signup")
    rows = details.split("\n")
    for i in range(len(rows)-1):
        arr = rows[i].split("#")
        if arr[5] == username:
            flag = True
            break
    return flag

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        hospital = request.POST.get('hospital', False)
        if checkUser(hospital) == False:
            data = username+"#"+password+"#"+contact+"#"+email+"#"+address+"#"+hospital+"\n"
            saveDataBlockChain(data,"signup")    
            context= {'data':'Signup Process Completed'}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Given Hospital already exists'}
            return render(request, 'Register.html', context)

def HospitalLoginAction(request):
    if request.method == 'POST':
        global user, hospital
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = 'none'
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == username and arr[1] == password:                
                status = 'success'
                hospital = arr[5]
                user = username
        if status == 'success':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "HospitalScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'HospitalLogin.html', context)
        

def DonorLoginAction(request):
    if request.method == 'POST':
        global user
        username = request.POST.get('username', False)
        readDetails("donor")
        rows = details.split("\n")
        status = "none"
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == username:                
                status = 'success'
                user = username
        if status == 'success':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "DonorScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'DonorLogin.html', context)
        
def UserLoginAction(request):
    if request.method == 'POST':
        global user
        username = request.POST.get('username', False)
        readDetails("patient")
        rows = details.split("\n")
        status = "none"
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == username:                
                status = 'success'
                user = username
        if status == 'success':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "UserScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)


        
            
