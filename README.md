# CSR-Generation
Certificate Generation using Streamlit
	 CERTIFICATE  GENERATION

The certificate generation tool is used to create the CSR generation and crt generation. In this tool, user has two tabs:
    • Csr generation.
    • Crt generation.

CSR generation tab:
 
In this page, the blocks are provided for DNS entry.  The DNS name should be in DNS.1=das.example.digivalet.in format. The tool make sthe folder with the same name which will be entered in the DNS.1 block so user has to remember the FQDN name of the DNS entered on the block DNS.1 for further procedure.

![image](https://user-images.githubusercontent.com/67871362/192806698-7d753dc4-a452-4211-99f7-d1b1e0d82c80.png)
                                                                                                                             
When user enters on the Submit button, the certificate request is provided to user on the interface with the Download CSR button. 

![image](https://user-images.githubusercontent.com/67871362/192807026-ae7b66a1-f891-4701-af84-0193fa439bb7.png)
                                                                                                                                                                                                                                                                                                                                                         
On clicking on the Download CSR button, the required csr is downloaded on the system with the name of das.example.digivalet.in.csr. 

CRT generation tab:

In this, the user has to provides the FQDN name of the DNS.1 in the first field  in the form of  das.tond.digivalet.in whose crt user wants and in the second field the user provides the zip file provided by Nitin sir. 

When user clicks on the Click buton,  it provides  the required zip to the user having CA.crt, server.crt, server.pem. server.key  in the zip.

![image](https://user-images.githubusercontent.com/67871362/192807112-495a62ae-8c36-496c-bf57-b91a12718184.png)


Required Libraries in Python:
 
1. streamlit==1.12.2
2. os.( latest )
3. shutil.( latest )
4. regex.( latest )
5. datetime.( latest )
6. subprocess.( latest )
7. zipfile.( latest )
