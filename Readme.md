# Ticket Generator and Scanner

Ticket generator and scanner , made for use for the NIE CS Freshers Party 2021. Make use it for some other party where tickets are required .

### Dependencies
- `Python 3.x` 
- `MongoDB 4.x.x`
- `Gotenberg (tag : latest)`
    - do a  `docker pull gotenberg/gotenberg`

## How To 
#### Generating Tickets :
- The first step is to get all the dependencies installed. As well as installing the python packages required. You can use the below command to install the packages
    ```bash
     pip install -r requirements.txt
    ```
- The list of names and amounts in `ticket_generate::main.py` was just randomly generated. Replace it with actual data later. Good way of doing so would be to read from a properly formatted csv or a json instead of harcoding it. 
- Run the gotenberg container and forward port `3000:3000` . This is where we make the requests to generate the pdfs. If you dont want to generate pdfs, you can skip this step  but you will need to edit some code here and there. Running the container can be done with the below command
    ```bash
     docker run --rm -p 3000:3000 gotenberg/gotenberg
    ```
- Finally now running the code should give you some pdfs in the folder which are the tickets for the event. Tickets are rendered using jinja and based of `ticker_generate::ticket.html` . So if you want a different ticket design change the html template and change the jinja variables too if required.

#### Scanning and validating tickets
- This is done using a flask app with the help of a nice library called [jsQR](https://github.com/cozmo/jsQR) to scan and decode the QR Codes.
- Run the flask app (`ticket_backend::app.py`) with the command below.
    ```bash
    python app.py
    ```
- This will start a flask app , running on port `5000` . Visiting `localhost:5000\qr` on your browser of choice will show you something similar to this
 ![The main screen](/images/Main_Screen.png)
- Only difference is that instead of a cat you'll see your beautiful face from your laptops webcam. (If you're on a desktop PC or dont have a webcam you'll just see a beautiful error.)
- Everything is now setup to scan and let people in. 
- When guests start showing up. Ask them to show a copy of the pdf ticket you've (hopefully) sent over. Put the QR code near your webcam and the app should recognize and mark it as shown below. This will also freeze the video stream so dont worry.
![A QR code was found!!](/images/qr_code_found.png)
- The contents of the QR code is displayed underneath after decoding. Your Primary check is to make sure that the name and other details you've added in your copy of this code match that which is found on the ticket. If they dont, the ticket is invalid straight off the bat , no need to query the database at all.
- If those match you can click on the `Check If Valid` button below the data , which sends a request to the same flask server to check if the ticket is valid or not (which is indicated by the isValid field in the response ). Depending on this one of two things will happen
- - (A) The ticket is valid , then the ticket holders details present in the database show up and a  nice satisfying check mark is show as well. It might look like something similar to the image down below ![A valid ticket](/images/valid_ticket.png)
- - (B) Or the ticket is invalid for some reason ( eg already used before, or forged etc ). In which case a cross mark shows up along with the reason why the ticket is invalid. ![A invalid ticket](/images/invalid_ticket.png)
- If the ticket is valid , then the app also marks it as used in the database preventing it from being used any further.
- To continue scanning more tickets, just click the `Reset Scanner` button below and it should start the video stream again. This lets you scan as many tickets as required. Use the same button in case of rare false positives too caused by bad lighting or a bad t-shirt.

##### Important Note
The app might give some false positives for the qr detection if you're in really bad lighting. So make so you have enough light for things to work properly.

#### TO DO
- I was unable to make this work with android browsers for some reason. If this was done , the code could be slightly modified so that it can be hosted and the scanning can be done anywhere , through ones phone . This would be much easier to handle on site and plus would look waay cooler.
- Maybe add ways for accounts to be created and the events managed. With each user having a list of events, and each event having a list of guests and tickets. This could also be hosted and provide a way for people who arent so tech inclined to use this app as well. Might also be able to give out good stats about the event and such.


And as always PRs and improvements are always appreciated and welcome. If you can improve this or knock some stuff off the TO DO list ,please feel free to do so.
