import os 
import pyrogram
import PyPDF2
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message, Document 
from gtts import gTTS
from Emli import pbot as bughunter0

from Emli import TMP_DOWNLOAD_DIRECTORY



Disclaimer = """ Disclaimer Notice , This Audio Is Generated automatically Through AudioBook  plugin in  emli Bot, Join Omg_Info on Telegram for More Bots .     You are Now Listening to your Audio  ."""
  
Thanks = """ Thats the End of Your Audio Book, Join Omg_Info on Telegram To find more Interesting bots , And Thanks for Using this Service"""


        
        
@bughunter0.on_message(filters.command(["audiobook"])) # PdfToText 
async def pdf_to_text(bot, message):
 try:
           if message.reply_to_message:
                pdf_path = TMP_DOWNLOAD_DIRECTORY + f"{message.chat.id}.pdf" #pdfFileObject
                txt = await message.reply("Downloading.....")
                await message.reply_to_message.download(pdf_path)  
                await txt.edit("Downloaded File")
                pdf = open(pdf_path,'rb')
                pdf_reader = PyPDF2.PdfFileReader(pdf) #pdfReaderObject
                await txt.edit("Getting Number of Pages....")
                num_of_pages = pdf_reader.getNumPages() # Number of Pages               
                await txt.edit(f"Found {num_of_pages} Page")
                page_no = pdf_reader.getPage(0) # pageObject
                await txt.edit("Finding Text from Pdf File... ")
                page_content = """ """ # EmptyString   
                chat_id = message.chat.id
                with open(f'{message.chat.id}.txt', 'a+') as text_path:   
                  for page in range (0,num_of_pages):              
                      page_no = pdf_reader.getPage(page) # Iteration of page number
                      page_content += page_no.extractText()
                await txt.edit(f"Creating Your Audio Book...\n Please Don't Do Anything \n**Join :** `@Omg_Info`")
                output_text = Disclaimer + page_content + Thanks
              # Change Voice by editing the Language
                language = 'en-in'  # 'en': ['en-us', 'en-ca', 'en-uk', 'en-gb', 'en-au', 'en-gh', 'en-in',
                                    # 'en-ie', 'en-nz', 'en-ng', 'en-ph', 'en-za', 'en-tz'],
                tts_file = gTTS(text=output_text, lang=language, slow=False) 
                tts_file.save(f"{message.chat.id}.mp3")      
                with open(f"{message.chat.id}.mp3", "rb") as speech:
                      await bot.send_voice(chat_id, speech, caption ="@Omg_Info",reply_markup=CHANNEL_BUTTON)   
                await txt.edit("Join @nexleech")    
                os.remove(pdf_path)  
                
                
           else :
                await message.reply("Please Reply to PDF file")
 except Exception as error :
           print(error)
           await txt.delete()
           os.remove(pdf_path)
         

 	
