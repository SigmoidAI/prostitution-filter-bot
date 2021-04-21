# prostitution-filter-bot
This repository stores the EDA Process and the project structure of a telegram bot that filters the person that share prostitution offers in telegram chat/group.
If setted as an admin to a telegram chat it can find prostitution offers in textes of messages and kick out users from the chat.

Origin of the data used - backpacge (http://backpage.com/) now it's blocked by FBI. Vasile found the data in github repository, the link si listed below.
Repository with the original data - https://github.com/usc-isi-i2/dig-alignment

Backpage was a classified advertising website founded in 2004. By the time that federal law enforcement agencies seized it in April 2018, it had become the largest marketplace for buying and selling sex.
More on wikipedia - https://en.wikipedia.org/wiki/Backpage

It was developed during a the Anti-Trafficking Hackathon (https://www.facebook.com/events/341855330476545) by one of sigmaritans - Vasile Păpăluță.

The repository have the following structure:
* DATA - the folder with all data files.
  - dirty_json - 6 json files with the original data found in a folder.
  - cleaned_json - 6 json files wiht cleaned data.
* EDA - the folder stores 2 files:
  - Untitled.ipynb - it shows the process of cleaning the data.
  - Untitled1.ipynb - it shows the procces of normalizing data and building the Machine Learning Model.
* MODEL - stores the files and modules needed for the Machine Learning Pipe line.
  - normalizer.obj - the binary file with the normalizer of the text.
  - vectorizer.obj - the binary file with the TF-IDF vectorizer trained on the data.
  - vocabulary.json - the json file with the list of the tokens of interest.
* PROD - stores the production files.
  - bot.py - the main file with the logic.
  - telebot.py - contains the chatbot class definision.
  - norm.py - contains the TextNormalizer class.
  - normaizer.obj - the binary file with the normalizer (ignored).
  - vectorizer.obj - the binary file with the TF-IDF vectorizer trained on the data.
  - vocabulary.json - the json file with the list of the tokens of interest.
  - database.bak, database.dat, database.dir - the shelve files for storing the user data. (create your own).

To run the project you must run the bot.py file by typing - ```python bot.py```.

Made with love by Sigmoid.
