import streamlit as st
st.set_page_config(layout="wide")
import os
import shutil
import subprocess as sp
import numpy as np
import regex as re
import subprocess
from zipfile import ZipFile
from datetime import datetime
das_fqdn_val =[]
col1, col2 = st.columns([2.5,6])
with col2:
    original_title = '<p style="font-family:Courier; color:white; font-size: 50px; height: 70px;">CERTIFICATE GENERATION</p>'
    st.markdown(original_title, unsafe_allow_html=True)


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
    replace_values_x=['<<DAS FQDN>>',
                        """DNS.1 = das.address-palace.digivalet.in
\nDNS.2 = dvs.address-palace.digivalet.in
\nDNS.3 = his.address-palace.digivalet.in"""
                    ]
    replace_values_y=[das_fqdn_val, txt]
    print(txt)
    for i in range(2):
        with open( os.path.join(os.getcwd(),das_fqdn_val,files[i]), 'r') as file:
            x = replace_values_x[i]
            y = replace_values_y[i]
            data = file.read()
            data = data.replace(x, y)
        with open(os.path.join(os.getcwd(),das_fqdn_val,files[i]), 'w') as file:
            file.write(data)


# generate csr
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
        print(csrname)
        copy_files(csrname)
        replace_files(csrname,txt)
        text_of_csr = generatefile(csrname)
        return text_of_csr,True


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
    
    
def unzipfile(name_of_file,uploaded_file):
    if uploaded_file is not None:
        subprocess.call(['chmod', '-R','755', os.path.join(os.getcwd(),name_of_file)])
        print(os.path.join(os.getcwd(),name_of_file,uploaded_file.name))
        with ZipFile(os.path.join(os.getcwd(),name_of_file,uploaded_file.name), 'r') as f:
            f.extractall(os.path.join(os.getcwd(),name_of_file))
        crt = uploaded_file.name.split('.')[-2]
        os.rename(os.path.join(os.getcwd(),name_of_file,crt)+'.ca-bundle',os.path.join(os.getcwd(),name_of_file)+'/CA.crt')
        os.rename(os.path.join(os.getcwd(),name_of_file,crt)+'.crt',os.path.join(os.getcwd(),name_of_file)+'/server.crt')
        mod1,mod2,condition = checkfile(name_of_file)
        if condition and mod1==0 and mod2==0:
            os.mkdir(os.path.join(os.getcwd(),name_of_file)+'/DV')
            os.system('mv '+os.path.join(os.getcwd(),name_of_file,'CA.crt')+' '+os.path.join(os.getcwd(),name_of_file,'server.crt')+' '+os.path.join(os.getcwd(),name_of_file,'DV'))
            os.system('cp '+os.path.join(os.getcwd(),name_of_file,'server.key')+' '+os.path.join(os.getcwd(),name_of_file,'DV'))
            os.system('cat '+os.path.join(os.getcwd(),name_of_file,'DV','server.crt') +' > ' +os.path.join(os.getcwd(),name_of_file,'DV','server.pem'))
            os.system('cat '+os.path.join(os.getcwd(),name_of_file,'DV','CA.crt') +' >> ' +os.path.join(os.getcwd(),name_of_file,'DV','server.pem'))
            print(os.path.join(os.getcwd(),name_of_file)+'/'+name_of_file+'.zip ')
            os.system('zip -r '+os.path.join(os.getcwd(),name_of_file)+'/'+name_of_file+'.zip '+os.path.join(os.getcwd(),name_of_file,'DV'))
            subprocess.call(['chmod', '-R','755', os.path.join(os.getcwd(),name_of_file)])
            return mod1,mod2,True
        else:
            return mod1,mod2,False
        
        
if  __name__ == '__main__':
    tab1, tab2 = st.tabs(["csr generation","crt generation"])
    with tab1:
            col1,col2 = st.columns(2)
            with col1:
                dns1 = (st.text_input('DNS.1', '')).strip()
                dns2 = (st.text_input('DNS.2', '')).strip()
                dns3 = (st.text_input('DNS.3', '')).strip()
                dns4 = (st.text_input('DNS.4', '')).strip()
            with col2:
                dns5 = (st.text_input('DNS.5', '')).strip()
                dns6 = (st.text_input('DNS.6', '')).strip()
                dns7 = (st.text_input('DNS.7', '')).strip()
                dns8 = (st.text_input('DNS.8', '')).strip()
            if st.button('Submit'):
                combo = [dns1,dns2,dns3,dns4,dns5,dns6,dns7,dns8]
                list_of_dns=[]
                for i in range(len(combo)-1):
                    if len(combo[i])!=0:
                        list_of_dns.append(combo[i])
                flag,flag_list = False, list()
                for i in list_of_dns:
                        if  re.match('^(DNS.)([0-9])([=])[a-zA-Z.]*$',i):
                            continue
                        else:
                            flag = True
                            print(flag_list)
                            flag_list.append(i)
                if flag:
                    original_title = '<p style="font-family:Courier; color:red; font-size:14px;">*The following DNS are not in correct format, should be in DNS.1=das.example.digivalet.in format.*</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    print(flag_list)
                    for i in flag_list:
                        print("hey")
                        if not i.startswith('DNS'):
                            st.write(i)
                        else:
                            st.write(i)
                else:
                    print(list_of_dns)
                    count = 0
                    if count == 0:
                        das_name = [i for i in list_of_dns if 'das' in i ]
                        if len(das_name) ==0:
                            count =1
                    if count == 1:
                        das_name = list_of_dns
                    print(das_name)
                    txt = '\n'.join(list_of_dns)
                    # print((das_name[0]).split('=')[-1])
                    # print(os.path.isdir(((os.path.join(os.getcwd(),das_name[0])).split('=')[-1])))
                    if not os.path.isdir(((os.path.join(os.getcwd(),das_name[0])).split('=')[-1])):
                        text,check = csrgenerate(das_name[0],txt)
                        if 'Certificate Request' in text:
                                st.text(text)
                        print(((os.path.join(os.getcwd(),das_name[0])).split('=')[-1])+'.csr')
                        with open(os.path.join(os.getcwd(),((os.path.join(os.getcwd(),das_name[0])).split('=')[-1]),((os.path.join(os.getcwd(),das_name[0])).split('=')[-1])+'.csr'), 'rb') as f:
                            st.download_button('Download CSR', f, file_name=((os.path.join(os.getcwd(),das_name[0])).split('=')[-1])+'.csr')
                    else:
                        st.write("The folder with "+das_name[0]+" already exists.")  
            
                    
                     
                
    with tab2: 
           
            name_of_file=st.text_input("Enter the name of the folder")
            original_title = '<p style="font-family:Courier; color:red; font-size:14px;">*Format of file name should be in das.tond.digivalet.in*</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Choose a zip file")
            if st.button('Click'):
                if uploaded_file is not None and (uploaded_file.name).endswith('.zip'):
                    st.markdown("**The file is sucessfully Uploaded.**")
                    print(os.getcwd())
                    
                    if os.path.exists(os.path.join(os.getcwd(),name_of_file,'CA.crt')):
                        st.write("The folder already contain CA.crt and server.crt")
                    if os.path.exists(os.path.join(os.getcwd(),name_of_file,uploaded_file.name)):
                        st.write("The folder already contain ",uploaded_file.name)
                    else:
                        with open(os.path.join(os.getcwd(),name_of_file,uploaded_file.name),"wb") as f:
                                        f.write((uploaded_file).getbuffer())
                        mod1,mod2,condition=unzipfile(name_of_file,uploaded_file)
                        print(mod1, mod2, condition)
                        if condition and mod1==0 and mod2==0:
                                print(os.path.join(os.getcwd(),name_of_file,name_of_file+'.zip'))
                                with open(os.path.join(os.getcwd(),name_of_file,name_of_file+'.zip'), 'rb') as f:
                                    st.download_button('Download Zip', f, file_name=name_of_file+'.zip') 
                                os.system('zip -r '+ os.path.join(os.getcwd())+'/'+name_of_file+'_'+(str(datetime.now())).split()[0]+'.zip '+os.path.join(os.getcwd(),name_of_file))
                                subprocess.call(['chmod', '-R','755', os.path.join(os.getcwd())+'/'+name_of_file+'_'+(str(datetime.now())).split()[0]+'.zip'])
                                print(os.path.join(os.getcwd())+'/'+name_of_file+'_'+(str(datetime.now())).split()[0]+'.zip')
                                name = os.path.join(os.getcwd())+'/'+name_of_file+'_'+(str(datetime.now())).split()[0]+'.zip'
                                shutil.move( name, '/tmp/')
                                shutil.rmtree(os.path.join(os.getcwd())+'/'+name_of_file)
                        else:
                            st.write("The modulus of server.crt ("+mod1+") and server.key ("+mod2+") are different.")
                else:
                    original_title = '<p style="font-family:Courier; color:red; font-size:14px;">"The uploaded file is either None or not in zip format."</p>'
                    st.markdown(original_title, unsafe_allow_html=True)           
                    # else:
                    #         st.write("The folder already contain CA.crt and server.crt")
                    

            # c1, c2, c3 = st.columns((2,3,2))
            # with c2:          
            #     st.info(""" DNS(Domain name server) are written in the following format:
            #                 \n**DNS.1=das.tond.digivalet.in**,
            #                 \n**DNS.2=analytics.tond.digivalet.in**,
            #                 \n**DNS.3=butler.tond.digivalet.in**,
            #                 \n**DNS.4=dvs.tond.digivalet.in**,
            #                 \n**DNS.5=his.tond.digivalet.in**,
            #                 \n**DNS.6=vod.tond.digivalet.in**""",icon="ℹ️")
            
            
        
        