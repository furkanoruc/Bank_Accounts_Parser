import os
import zipcodes
import re
import json
#import base_parser
import sys
import csv
import glob

sys.argv[1]

class Bank:

    def __init__(self):
        self.date = None
        self.bankname = []
        self.photo_id = None
        self.account_number = None
        self.amount = []
        self.account_type = []

    def get_date_and_id_from_title(self, title):
        re1 = title.split("@")
        photo_id=""
        date=""
        if('.DS_Store' not in re1):
            #print("@@@@@@@@@@@@@@@@@@",re1)
            photo_id = re1[0].split("_")[1]
            date = re1[1].split("_")[0]
        return photo_id, date

    def check_bankname(self, content):
        # return bank name if finds a match from the given names
        # print(Banks)
        bank_list = ["bank of america", "suntrust", "j.p.morgan", "bankozk", "hhsb", "first convenience bank", 
        "chase", "regions", "navy fed", "citibank", "usb financial services", "us bank", "pnc bank", "capital one", 
        "td bank", "wells fargo", "Citizen Bank", "fifth third bank", "first fidelity bank", "commerce bank", "us bank", 
        "first citizens bank", "capital one", "first republic bank", "u.s. century bank","active duty", "american express",
        "aspirations bank", "b&t Bank", "banco felabella", "bb&t", "barrera farms", "bmo harris bank", "burning bank",
        "chime", "choice financial group", "citi", "commerce", "cryptocurrency", "discover", "DUPACO community credit union",
        "fair financial", "Go2Bank", "green dot bank", "hancock whitney", "huntington", "IPC bank", "Indi",
        "Kabbage", "key bank", "M&T bank", "Marcus", "Navy Fedral credit union", "New York Community Bank",
        "RCB bank", "Reve", "RF bank finance", "Robin Financial", "T Mobile Money", "usaa", "varo bank", "WAFD",
        "woodforest", "5 star bank", "allegiance bank", "ally bank", "alpine bank", "amerant bank", "ann arbour",
        "ArrowPointe", "ArrowPointe federal credit union", "bancorp south", "atlantic union bank", "bank of madison",
        "bank of texas", "bank of the james", "bank of tokyo", "bank united", "bank york", "bbva", "bragg mutual",
        "c&F bank", "carotrans", "cashier's check", "cathay bank", "CBC bank", "centerstate", "charlotte metro",
        "cnb","comerica", "community bank","community credit union","county educators","county national bank",
        "crown bank", "customers bank", "Dexterous mold and tool","eagle bank", "east west bank",
        "edfed", "erie insurance group","evolution risk advisors","executive banking","federal","federal credit union",
        "federal incentive check","federal tax return","fidelity bank","financial credit union","first national bank",
        "first south bank","first state bank","floridian community bank","founders","freedom bank","frost",
        "gamebreaker","german american bank","grove bank and trust", "guilford savings bank","harford bank",
        "havensavings bank","hudson valley credit union","huntington","IBM southeast employees","ibmsecu",
        "invesco","investors bank","jeff bank","key bank","key bank national association","lncb national bank",
        "lgfcu","lindell bank","marine","merril","merrimac valley credit union","metabank","midflorida",
        "morgan stanley","motion federal credit union","NC dept of revenue","ncua","new brunswick credit union",
        "northeast family", "northern trust","northview bank","nycb","ocean bank","pacific premier bank",
        "pacific western bank","patriot bank","peoples bank","peoples bank and trust","people's united bank",
        "planters bank","popa federal credit union","popular bank","prosperity bank","professional bank",
        "roselle bank","ruth smith","santandar bank","seacoast bank","select bank and trust", "signature bank",
        "simmons bank","south atlantic bank","south state bank","sovereign bank","space coast credit union",
        "spencer savings bank","state employees credit union","state of florida","stifel bank","sun east",
        "sunshine bank","sunstate bank","td bank","texena bank","the bank of new york mellon","the family bank",
        "the merchants national bank","towne bank","treasury of illinois","tri counties bank","u.s capital advisors",
        "u.s central bank","u.s century bank","ubs","umb bank","union county savings bank","united southern bank",
        "united states treasury","valley bank","vanguard municipal money market fund","valley neational bank",
        "voya institutional trust", "walmart moneycard","webster bank", "chime" ]
        re = set()
        
        ##### check bank name in text #####
        content_lower = content.lower()
        # print()
        for i in bank_list:
            if i in content_lower:
                re.add(i)
        return re

    def check_type(self, content):
        acc_type = ["saving", "checking", "credit"]
        re = set()
        content_lower = content.lower()
        for i in acc_type:
            if i in content_lower:
                re.add(i)
        return re

    def check_amount(self, content):
        # return the amounts present in the content
        result = {"amount":0,"Credited_sum":0,"Debited_sum":0} 
        credited_amount=[]
        debited_amount=[]
        # find with digit and decimal
        for i in re.finditer(r"\d{1,4}(?:,\d{4})*(?:\.\d+)+", content):
            # print(i)
            index = int(i.span()[0])
            check_trans = content[index-3:index]
            if("+" in check_trans):
                s=i.group().replace("$","").replace(",","")
                if(s.count(".")>1): 
                    s = s.replace(".","",1)
                    print("#############################",s)

                    
                credited_amount.append(s)
            elif("-" in check_trans):
                s=i.group().replace("$","").replace(",","")
                if(s.count(".")>1): 
                    s = s.replace(".","",1)
                    print("#############################",s)

                debited_amount.append(s)
            else:
                result["amount"]=i.group()
        #find with S digit and deciaml
        # for i in re.finditer(r"(\b[S][0-9]*\.[0-9]*)|\b[S][0-9]+", content):
        #     print(i.group())
        #     result.add(i.group()[1:])
        for i in re.finditer(r"\b[S]\d{1,4}(?:,\d{4})*(?:\.\d+)+|\b[S]\d{1,4}(?:,\d{4})*", content):
            # print(i.group())
            index = int(i.span()[0])
            check_trans = content[index-3:index]
            if("+" in check_trans):
                s=i.group().replace("$","").replace(",","").replace("S","")
                if(s.count(".")>1): 
                    s = s.replace(".","",1)
                    print("#############################",s)
                    
                credited_amount.append(s)
            elif("-" in check_trans):
                s=i.group().replace("$","").replace(",","").replace("S","")
                if(s.count(".")>1): 
                    s = s.replace(".","",1)
                    print("#############################",s)

                debited_amount.append(s)
            else:
                result["amount"] = i.group()[1:]
        # find with $ digit and decimal
        # for i in re.finditer(r"\$\d+(?:\.\d+)?", content):
        #     print(i.group())
        #     result.add(i.group()[1:])
        for i in re.finditer(r"\$\d{1,3}(?:,\d{3})*(?:\.\d+)+|\$\d{1,3}(?:,\d{3})*", content):
            # print(i.group())
            index = int(i.span()[0])
            check_trans = content[index-3:index]
            if("+" in check_trans):
                s=i.group().replace("$","").replace(",","")
                if(s.count(".")>1): 
                    s = s.replace(".","",1)
                    print("#############################",s)
                    
                credited_amount.append(s)
            elif("-" in check_trans):
                s=i.group().replace("$","").replace(",","")
                if(s.count(".")>1): 
                    s = s.replace(".","",1)
                    print("#############################",s)

                debited_amount.append(s)
            else:
                result["amount"] = i.group()[1:]
        
        credited_amount = list(set(credited_amount))
        debited_amount = list(set(debited_amount))
        
        credited_sum = 0
        debited_sum = 0
        for i in credited_amount:
            credited_sum=credited_sum+float(i)
            
        for i in debited_amount:
            debited_sum=debited_sum+float(i)
        
        result["Credited_sum"]=credited_sum
        result["Debited_sum"]=debited_sum
        print(result)
        
        return result

    def get_count_available_balance(self, content):
        # return the count of available amount
        word = "available balance"
        cnt = 0
        # content_lower = content.lower()
        for line in content:
            line = line.lower()
            if word in line:
                cnt += 1
        return cnt

    def data_assign_byrow(self, photo_id, date, bank, account_type, amount, balance_cnt,writer):
        amount.sort(reverse=True)
        # amount = amount[:balance_cnt]
        num_banks = len(bank)
        num_acc_type = len(account_type)
        num_amount = len(amount)
        if num_banks == 1:
            for i in range(0, max(num_banks,num_acc_type,num_amount)):
                if num_acc_type > 0:
                    acc_type = account_type.pop(0)
                    num_acc_type -= 1
                else:
                    acc_type = ""

                if num_amount > 0:
                    amt = amount.pop(0)
                    avail_amount=amt["amount"]
                    debited_amount=amt["Debited_sum"]
                    credited_amount=amt["Credited_sum"]
                    num_amount -= 1
                else:
                    amt = ""
                    avail_amount=""
                    debited_amount=""
                    credited_amount=""
                writer.writerow([photo_id, date, bank[0], acc_type, "", avail_amount,debited_amount,credited_amount])
            return 
        else:
            for i in range(0, max(num_banks,num_acc_type,num_amount)):
                if num_acc_type > 0:
                    acc_type = account_type.pop(0)
                    num_acc_type -= 1
                else:
                    acc_type = ""
                if num_amount > 0:
                    amt = amount.pop(0)
                    avail_amount=amt["amount"]
                    debited_amount=amt["Debited_sum"]
                    credited_amount=amt["Credited_sum"]
                    num_amount -= 1
                else:
                    amt = ""
                    avail_amount=""
                    debited_amount=""
                    credited_amount=""
                if num_banks > 0:
                    bank_name = bank.pop(0)
                    num_banks -= 1
                else:
                    bank_name = ""
                writer.writerow([photo_id, date, bank_name, acc_type, "",avail_amount,debited_amount,credited_amount])

if __name__ == '__main__':
    folder_textdoc_path = sys.argv[1]
    #textdoc_paths = base_parser.get_textdoc_paths(folder_textdoc_path)
    textdoc_paths = glob.glob(r'/Users/furkanoruc/Desktop/Desktop-Furkan/MSc./SPRING2022/GRA/Bank-Accounts/BankAccounts-TextFiles/*.txt')
    print(len(textdoc_paths))
    #print("HelloHElllo")
    #print(textdoc_paths)
    headerList = ['Pic Id', 'Date', 'Bank Name', 'Account Type', 'Account Number', 'Amount', 'Credited Amount','Debited Amount']
    with open('bank_accounts_data'+'.csv','w', newline='', encoding='utf-8') as f1:
        dw = csv.DictWriter(f1, delimiter=',', fieldnames=headerList)
        dw.writeheader()
        writer=csv.writer(f1, delimiter=',')#lineterminator='\n',
    # for i in np.arange(0,9):
    #     row = data[i]
    #     writer.writerow(row)
  
        for text_doc in textdoc_paths:
            writer=csv.writer(f1, delimiter=',')
            check = Bank()
            file_name = os.path.basename(text_doc)

            #### parse photo id and date
            photo_id, date = check.get_date_and_id_from_title(file_name)
            if photo_id:
                check.photo_id = photo_id
            if date:
                check.date = date

            ### parse zipcode and state
            with open(text_doc, encoding = "utf-8") as f:
                content = f.readlines()
            if content:
                text_des = content[-1]
            else:
                writer.writerow([check.photo_id, check.date, "", "", "", "", ""])
                continue
            #print((text_des).encode('utf-8'))

            if content:
                info_bank_type = check.check_type(text_des)
                check.account_type.extend([i for i in info_bank_type])

            #### parse bankname
                info_bank = check.check_bankname(text_des)
                check.bankname.extend([i for i in info_bank])
                for i in check.bankname:
                    #print("bank:",i)
                    pass
                check.amount = [check.check_amount(text_des)]
                #check.amount.extend(i for i in info_amount)
                avail_amt = check.get_count_available_balance(content[:-1])

            # for i,code in enumerate(check.zipcode):
            #     writer.writerow()
            else:
                print("Empty file")

            #print(check.photo_id, check.date, check.bankname, check.account_type, check.account_number, check.amount)
            # writer.writerow([check.photo_id, check.date, check.bankname, check.account_type, check.account_number, check.amount, avail_amt])
            check.data_assign_byrow(check.photo_id, check.date, check.bankname, check.account_type, check.amount, avail_amt, writer)
