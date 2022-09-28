import streamlit as st
st.set_page_config(layout="wide")
import os
import shutil
import subprocess as sp
import regex as re
import subprocess
from zipfile import ZipFile
from datetime import datetime
import pandas as pd
import sys
import subprocess
month_number ={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
das_fqdn_val =[]

# ------------------------------------------------------------- Title ------------------------------------------------------------
col1, col2 = st.columns([2,6])
with col2:
    original_title = '<p style="font-family:Courier; color:white; font-size: 50px; height: 70px;">DIGIVALET-CERTIFICATE-MANAGER</p>'
    st.markdown(original_title, unsafe_allow_html=True)

hide_menu_style = """
                <style>
                MainMenu {visibility: hidden; }
                footer {visibility: hidden; }
                </style>
    """    
st.markdown(hide_menu_style, unsafe_allow_html=True)   

# ---------------------------------------------------------------------------------------------------------------------------------

# calling file for scheduling
def new_schedulers(name_of_file):
    l=(((sp.getoutput("openssl x509 -in "+os.path.join(os.getcwd()+'/'+name_of_file)+"/dv/server.crt -noout -enddate")).split("=")[-1]).split(" "))
    l.insert(0,name_of_file)
    # name = ",".join(l)
    df=pd.DataFrame({'nameoffile':[l[0]],'month':[l[1]],'date':[l[2]],'time':[l[3]],'year':[l[4]],'timezone':[l[5]]})
    now = datetime.now()
    subprocess.run([f"{sys.executable}", 'slack_webhook.py', l[0], l[1], l[2] , l[4], l[3], l[5],'1'])  
    

# copy the required files
def copy_files(das_fqdn_val):
    l=['csrgenerate','openssl.cnf','verify']
    for i in range(3):
        src_path = os.path.join(os.getcwd(),'files',l[i])
        dst_path = os.path.join(os.getcwd(),das_fqdn_val,l[i])
        shutil.copy(src_path, dst_path)
        os.system('chmod +x '+os.path.join(os.getcwd(),das_fqdn_val,l[i]))
     
        
# replace context from the csrgenerate, openssl.cnf, verify.
def replace_files(das_fqdn_val,txt):
    files=['csrgenerate','openssl.cnf']
    replace_values_x=['<<DAS FQDN>>',"""DNS.1 = das.address-palace.digivalet.in\n\nDNS.2 = dvs.address-palace.digivalet.in\n\nDNS.3 = his.address-palace.digivalet.in"""]
    replace_values_y=[das_fqdn_val, txt]
    print(txt)
    for i in range(2):
        with open( os.path.join(os.getcwd(),das_fqdn_val,files[i]), 'r') as file:
            x = replace_values_x[i]
            y = replace_values_y[i]
            data = file.read()
            data = data.replace(x, y)
            print('data: ',x," ",y)
        with open(os.path.join(os.getcwd(),das_fqdn_val,files[i]), 'w') as file:
            file.write(data)


# generating the required csr.
def generatefile(das_fqdn_val):
    print(das_fqdn_val)
    os.chdir('./'+das_fqdn_val)
    bash_csr_value = os.system('bash csrgenerate')
    if bash_csr_value is not None:
        out = sp.getoutput('bash verify '+ das_fqdn_val+'.csr')
        if out is not None:
            with open('csrfile','w') as file:
                file.write(out)
            os.chdir('../')
            return out
        else:
            return False
    else:
        return False


def csrgenerate(csrname,txt):
        csrname = csrname[6:]
        os.mkdir(csrname)
        copy_files(csrname)
        replace_files(csrname,txt)
        text_of_csr = generatefile(csrname)
        return text_of_csr,True

# compare the server.crt and the server.key.
def checkfile(name_of_file):
    subprocess.call(['chmod', '-R','755', os.path.join(os.getcwd(),name_of_file)])
    out1 = sp.getoutput("openssl x509 -noout -modulus -in "+os.path.join(os.getcwd(),name_of_file,'server.crt')+ "| openssl md5")
    value1 = out1.split('=')[-1]
    out2 = sp.getoutput("openssl rsa -noout -modulus -in "+os.path.join(os.getcwd(),name_of_file,'server.key')+ "| openssl md5")
    value2 = out2.split('=')[-1]
    if value1 == value2:
        return 0,0,True
    else:
        return value1,value2,False
    
# unzip the inserted file in crt generation.  
def unzipfile(name_of_file,uploaded_file):
    try:
        if uploaded_file is not None:
            subprocess.call(['chmod', '-R','755', os.path.join(os.getcwd(),name_of_file)])
            with ZipFile(os.path.join(os.getcwd(),name_of_file,uploaded_file.name), 'r') as f:
                f.extractall(os.path.join(os.getcwd(),name_of_file))
            crt = uploaded_file.name.split('.')[-2]
            os.rename(os.path.join(os.getcwd(),name_of_file,crt)+'.ca-bundle',os.path.join(os.getcwd(),name_of_file)+'/CA.crt')
            os.rename(os.path.join(os.getcwd(),name_of_file,crt)+'.crt',os.path.join(os.getcwd(),name_of_file)+'/server.crt')
            mod1,mod2,condition = checkfile(name_of_file)
            if condition and mod1==0 and mod2==0:
                os.mkdir(os.path.join(os.getcwd(),name_of_file)+'/dv')
                os.system('mv '+os.path.join(os.getcwd(),name_of_file,'CA.crt')+' '+os.path.join(os.getcwd(),name_of_file,'server.crt')+' '+os.path.join(os.getcwd(),name_of_file,'dv'))
                os.system('cp '+os.path.join(os.getcwd(),name_of_file,'server.key')+' '+os.path.join(os.getcwd(),name_of_file,'dv'))
                os.system('cat '+os.path.join(os.getcwd(),name_of_file,'dv','server.crt') +' > ' +os.path.join(os.getcwd(),name_of_file,'dv','server.pem'))
                os.system('cat '+os.path.join(os.getcwd(),name_of_file,'dv','CA.crt') +' >> ' +os.path.join(os.getcwd(),name_of_file,'dv','server.pem'))
                os.system('zip -r '+name_of_file+'.zip '+os.path.join(name_of_file,'dv'))
                os.system('mv '+name_of_file+'.zip '+os.path.join(name_of_file))
                subprocess.call(['chmod', '-R','755', os.path.join(os.getcwd(),name_of_file)])
                return mod1,mod2,True
            else:
                    return mod1,mod2,False
    except FileNotFoundError as e:
        st.write("The folder doesn't contain the required files.")
        return False,False,False
        
        
if  __name__ == '__main__':
        tab1, tab2 = st.tabs(["csr generation","crt generation"])
        with tab1:
                col1,col2 = st.columns(2)
                with col1:
                    dns1 = (st.text_input('DNS.1', '',key=11)).strip()
                    dns2 = (st.text_input('DNS.2', '',key=21)).strip()
                    dns3 = (st.text_input('DNS.3', '',key=31)).strip()
                    dns4 = (st.text_input('DNS.4', '',key=41)).strip()
                with col2:
                    dns5 = (st.text_input('DNS.5', '',key=51)).strip()
                    dns6 = (st.text_input('DNS.6', '',key=61)).strip()
                    dns7 = (st.text_input('DNS.7', '',key=71)).strip()
                    dns8 = (st.text_input('DNS.8', '',key=81)).strip()
                if st.button('Submit'):
                    combo = [dns1,dns2,dns3,dns4,dns5,dns6,dns7,dns8]
                    list_of_dns=[]
                    # print(combo)
                    for i in range(len(combo)-1):
                        if len(combo[i])!=0:
                            list_of_dns.append(combo[i])
                    flag,flag_list = False, list()
                    for i in list_of_dns:
                            if  re.match('^(DNS.)([0-9])([=])[a-zA-Z.-]*$',i):
                                continue
                            else:
                                flag = True
                                print(flag_list)
                                flag_list.append(i)
                    if flag:
                        original_title = '<p style="font-family:Courier; color:red; font-size:14px;">*The following DNS are not in correct format, should be in DNS.1=das.example.digivalet.in format.*</p>'
                        st.markdown(original_title, unsafe_allow_html=True)
                        for i in flag_list:
                            if not i.startswith('DNS'):
                                st.write(i)
                            else:
                                st.write(i)
                    else:
                        count = 0
                        if count == 0:
                            das_name = [i for i in list_of_dns if 'das' in i ]
                            if len(das_name)==0:
                                count =1
                        if count == 1:
                            das_name = list_of_dns
                        txt = '\n'.join(list_of_dns)
                        try:
                            if not os.path.isdir(((os.path.join(os.getcwd(),das_name[0])).split('=')[-1])):
                                text,check = csrgenerate(das_name[0],txt)
                                try:
                                    if 'Certificate Request' in text:
                                            st.text(text)
                                    with open(os.path.join(os.getcwd(),((os.path.join(os.getcwd(),das_name[0])).split('=')[-1]),((os.path.join(os.getcwd(),das_name[0])).split('=')[-1])+'.csr'), 'rb') as f:
                                        st.download_button('Download CSR', f, file_name=((os.path.join(os.getcwd(),das_name[0])).split('=')[-1])+'.csr')
                                except Exception as e:
                                    st.write("The text doesn't contain CERTIFICATE REQUEST.")
                        except Exception as e:
                            st.write("The folder with "+das_name[0]+" already exists.")  
        with tab2: 
                name_of_file=st.text_input("Enter the name of the folder").strip()
                original_title = '<p style="font-family:Courier; color:red; font-size:14px;">*Format of file name should be in das.tond.digivalet.in*</p>'
                st.markdown(original_title, unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Choose a zip file")
                if st.button('Click'):
                    if uploaded_file is not None and (uploaded_file.name).endswith('.zip'):
                        st.markdown("**The file is sucessfully Uploaded.**")
                        if not os.path.exists(os.path.join(os.getcwd(),name_of_file)):
                            st.write("The folder with "+name_of_file+" is not present.")
                        else:
                            if os.path.exists(os.path.join(os.getcwd(),name_of_file,uploaded_file.name)):
                                st.write("The file ("+uploaded_file.name+") already present in the mentioned folder.")
                            else:
                                with open(os.path.join(os.getcwd(),name_of_file,uploaded_file.name),"wb") as f:
                                                f.write((uploaded_file).getbuffer())
                                mod1,mod2,condition=unzipfile(name_of_file,uploaded_file)
                                print(mod1, mod2, condition)
                                if condition  and mod1==0 and mod2==0:
                                        import pandas as pd
                                        df_header_index_col = pd.read_csv('schedule.csv', sep=',' ,names=('nameoffile','schedulers'))
                                        if (df_header_index_col['nameoffile'].isin([name_of_file])).any():
                                            print(df_header_index_col[['nameoffile']])
                                            for index, row in df_header_index_col.iterrows():
                                                if row['nameoffile'] == name_of_file:
                                                    print(row['schedulers'], type(row['schedulers']))
                                                    subprocess.run([f"{sys.executable}", 'slack_webhook.py', '0', row['schedulers'], row['nameoffile']])  
                                            new_schedulers(name_of_file)
                                        else:
                                            new_schedulers(name_of_file)
                                        with open(os.path.join(os.getcwd(),name_of_file,name_of_file+'.zip'), 'rb') as f:
                                            st.download_button('Download Zip', f, file_name=name_of_file+'.zip')
                                        os.system('zip -r '+ os.path.join(os.getcwd())+'/'+name_of_file+'_'+(":".join([str((str(str('_'.join(str(datetime.now()).split())).split('.')[0]).split(':'))[0]), str((str(str('_'.join(str(datetime.now()).split())).split('.')[0]).split(':'))[1])]))+'.zip '+os.path.join(os.getcwd(),name_of_file))
                                        subprocess.call(['chmod', '-R','755', os.path.join(os.getcwd())+'/'+name_of_file+'_'+(":".join([str((str(str('_'.join(str(datetime.now()).split())).split('.')[0]).split(':'))[0]), str((str(str('_'.join(str(datetime.now()).split())).split('.')[0]).split(':'))[1])]))+'.zip'])
                                        name = os.path.join(os.getcwd())+'/'+name_of_file+'_'+(":".join([str((str(str('_'.join(str(datetime.now()).split())).split('.')[0]).split(':'))[0]), str((str(str('_'.join(str(datetime.now()).split())).split('.')[0]).split(':'))[1])]))+'.zip'
                                        try:
                                            shutil.move( name, '/tmp/')
                                            shutil.rmtree(os.path.join(os.getcwd())+'/'+name_of_file)
                                        except:
                                            st.write("The zip file with "+name+" already present.")
                                else:
                                    try:
                                        dir_path = name_of_file
                                        req = ["csrfile","csrgenerate","server.key","openssl.cnf","verify",name_of_file+'.csr']
                                        res = [path for path in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, path))]
                                        for i in res:
                                            if i not in req:
                                                os.remove(os.path.join(dir_path,i))
                                        print(os.listdir(dir_path))
                                        if mod1 is not None and mod2 is not None:
                                            st.write("The modulus of server.crt ("+mod1+") and server.key ("+mod2+") are different.")   
                                    except:
                                        pass            
                    else:
                        original_title = '<p style="font-family:Courier; color:red; font-size:14px;">"The uploaded file is either None or not in zip format."</p>'
                        st.markdown(original_title, unsafe_allow_html=True)   
        
        
             
    
                    
        