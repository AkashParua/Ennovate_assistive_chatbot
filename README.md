# Ennovate_assistive_chatbot

Steps to set up the server -

1. virtualenv env
2. activate the env  ./Scripts/activate
3. install -r requirements.txt
4. cd server
# The persist_dir contains the embeddings 
# To add your own manual ,change the contents of server/sample_manual.txt and run  python3 extract.py  to create new embeddings 

#Remember to add your own headers int the main.py from rapidapi
https://rapidapi.com/FutureWave/api/chatgpt-gpt-3-5 - user Python(Requests)
