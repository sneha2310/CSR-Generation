# CSR-Generation
Certificate Generation using Streamlit

The certificate generation tool is used to create the CSR generation and crt generation. In this tool, user has two tabs:
    • Csr generation.
    • Crt generation.

CSR generation tab:
 
In this page, the blocks are provided for DNS entry.  The DNS name should be in DNS.1=das.example.digivalet.in format. The tool make sthe folder with the same name which will be entered in the DNS.1 block so user has to remember the FQDN name of the DNS entered on the block DNS.1 for further procedure.

![image](https://user-images.githubusercontent.com/67871362/190660428-3d4b66ce-f47f-47f4-af78-df7de835a5e5.png)

When user enters on the Submit button, the certificate request is provided to user on the interface with the Download CSR button. 

![image](https://user-images.githubusercontent.com/67871362/190660490-9582f997-c56b-425b-89e3-554960ca17f5.png)

On clicking on the Download CSR button, the required csr is downloaded on the system with the 
name of das.example.digivalet.in.csr. 


CRT generation tab:

In this, the user has to provides the FQDN name of the DNS.1 in the first field whose crt user wants and in the second field the user provides the zip file provided by Nitin sir. 

When user clicks on the Click buton,  it provides  the required zip to the user having CA.crt, server.crt, server.pem. server.key  in the zip.

![image](https://user-images.githubusercontent.com/67871362/190660625-cea7b595-e014-42f5-886e-ff1f46a3e075.png)
