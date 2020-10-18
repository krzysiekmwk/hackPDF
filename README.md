# PDF Password breaker

Windows

Start server:
`python.exe .\main_controller.py`
- server will start listening for new connection
- if there will be one connection it will start sending PDF file to it
- then there will be command to start decoding that file
- start listening for received message (password or no password)
- if client will go (ctrl+c to kill) then server starts to listen again for clients

Start client:
`python.exe -m core.client`
- client will start listening for new commands
- if there will be **CMD:SEND_PDF_FILE** command then start to receiving pdf file
- file will be saved in main directory with timestamp and some random id
- if there will be **CMD:START_DECRYPT** command then start algorithm for decrypt pdf
- after finish algorithm, client will send to server password - or no password
- then will start for waiting for next commands (kill it by ctrl+c)