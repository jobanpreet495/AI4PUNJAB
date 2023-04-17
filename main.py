from flask import Flask,render_template,request,session,jsonify
import re
from IPA import ipa_creation
from transliteration import pun_to_eng,eng_to_pun,eng_to_pun2
from sound import play_phoneme_list
import pytesseract
from PIL import Image

app=Flask(__name__)
app.secret_key = 'your_secret_key'

#-----------------------------------------------Render templates------------------------------------------------
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/phonetic')
def phonetic():
    return render_template('phonetic.html')



@app.route('/transliteration')
def transliteration():
    return render_template('transliterate.html')


@app.route('/typepad')
def typepad():
    return render_template('typepad.html')


#--------------------------------------------------------OCR code----------------------------------------------
@app.route('/ocr')
def ocr():
    return render_template('OCR.html')


@app.route('/convert', methods=['POST','GET'])
def convert():
    if request.method == 'POST':
        image_file = request.files['image-upload']
        img = Image.open(image_file)

 
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        text = pytesseract.image_to_string(img,lang="pan")
        return render_template('OCR.html',text=text)
    

#---------------------------------------------------Transliteration---------------------------------------------------------------------


@app.route("/translit" , methods=['POST'])
def translit():
    text=request.form['tt']
    text=text.strip()
    
    # text = re.sub('[a-zA-Z]', '', text)
    option1=request.form['dropdown1']
    option2=request.form['dropdown2']
  
    if option1=='Punjabi' and option2=='Punjabi':
       return render_template('transliterate.html',error="Please select another target language")
    elif option1=='English' and option2=='English':
        return render_template('transliterate.html',error="Please select another target language")

            
    elif option1=='Punjabi' and option2=='English':
        text=expand_numerics(text)
        text = re.sub('[a-zA-Z]', '', text)   
        trans=pun_to_eng(text)
        rt=extract_word(trans)
        
        return render_template('transliterate.html',rt=" ".join(rt))
    


    elif option1=='English' and option2=='Punjabi':
        text = re.sub('[^A-Za-z ]+', '', text)
        text=text.lower()
        trans=eng_to_pun(text)
        rt=extract_word(trans)
      
        return render_template('transliterate.html',rt=" ".join(rt))

def extract_word(s):
        name = ""
        l=[]
        for char in s:
            if char == "@":
                name = ""
            elif char == "#":
                l.append(name)
            else:
                name += char
        #return l
                
        prev = None
        result = []
        for item in l:
            if item != prev:
                result.append(item)
            prev = item
        return result


@app.route('/predict', methods=['POST'])
def predict():
    input_text = request.form['text']
    output_text = eng_to_pun2(input_text)
    output_text=extract_word(output_text)
    s=[]
    for i in output_text:
        if i=='ਏ':
            s.append(i[1:])
        else:
            s.append(i)

    return {'output': "".join(s)}

#-------------------------------------Preprocessing-------------------------------------------------

def clean_text(text):
    text = re.sub(r'[^\u0A00-\u0A7F\s]', '', text)
    return text


def expand_numerics(text):
    numerics = {
        '0': 'ਸਿਫਰ',
        '1': 'ਇੱਕ',
        '2': 'ਦੋ',
        '3': 'ਤਿੰਨ',
        '4':'ਚਾਰ',
        '5': 'ਪੰਜ',
        '6':'ਛੇ',
        '7':'ਸੱਤ',
        '8':'ਅੱਠ',
        '9':'ਨੌ'

    }
    for numeric, expansion in numerics.items():
        text = text.replace(numeric, " " +expansion)
    return text

#------------------------------------------------------------------------------------------------------------
con=['ਕ','ਖ','ਗ','ਘ','ਙ','ਚ','ਛ','ਜ','ਝ','ਞ','ਟ','ਠ','ਡ','ਢ','ਣ','ਤ','ਥ','ਦ','ਧ','ਨ','ਪ','ਫ','ਬ','ਭ','ਮ','ਯ','ਰ','ਲ','ਲ਼','ਵ','ਸ਼','ਸ','ਹ','ਖ਼','ਗ਼','ਜ਼','ੜ','ਫ਼']
NonV=['ਇ','ਈ','ਏ','ਐ','ਅ','ਆ','ਔ','ਉ','ਊ','ਓ','ੰ','ਂ']
NV=['ਇੰ','ਈਂ','ਅੰ','ਆਂ','ਔਂ','ਉਂ','ਊਂ','ਓਂਂ','ਏਂ','ਐਂ']
m={'ਾ': 'ਆ',
        'ਿ': 'ਇ', 'ੀ': 'ਈ',
        'ੁ': 'ਉ', 'ੂ': 'ਊ',
        'ੇ': 'ਏ', 'ੈ': 'ਐ',
        'ੋ': 'ਓ', 'ੌ': 'ਔ'}
NUQTA = '਼'
HALANT = '੍'
ADDAK = 'ੱ'
CV_NonV=[]
CV_NV=[]
for i in con:
        for j in NonV:
            CV_NonV.append(i+j)

    # list of combination of consonants with nasalized vowels

for i in con:
    for j in NV:
        CV_NV.append(i+j)


@app.route('/phoneme',methods=['POST','GET'])
def phoneme():
    word=request.form['any_text']
    word=word.strip()
    word=expand_numerics(word)
    word = re.sub('[a-zA-Z]', '', word)
    trans_word=word
    ph=[]
    words=word.split()
    for word in words:
        if word.strip() in CV_NonV or word in CV_NV :
            ph.append(word)
            ph.append('s')
        else:
            for char in word:
                if char == HALANT:
                    pass
                elif char in con:
                    ph.append(char)
                    ph.append('ਅ')
                elif char in NonV:
                    ph.append(char)
                elif char in m:
                    ph.pop()
                    ph.append(m[char])
                elif char == NUQTA:
                    pass
            ph.append("s")
                
        i = 0
        while i < len(ph) - 1:
            if ph[i] == 'ਓ' and ph[i+1] == 'ਂ':
                ph[i:i+2] =['ਓਂਂ']  # replace 'ਓ' and 'ਂ' with 'ਓਂਂ'

            elif ph[i] == 'ਆ' and ph[i+1] == 'ਂ':
                # Replace both elements with 'ਆਂ'
                ph[i:i+2] = ['ਆਂ']

            elif ph[i] == 'ਇ' and ph[i+1] == 'ੰ':
                ph[i:i+2] = ['ਇੰ']

            elif ph[i] == 'ਈ' and ph[i+1] == 'ਂ':
                ph[i:i+2] = ['ਈਂ']

            elif ph[i] == 'ਔ' and ph[i+1] == 'ਂ':
                ph[i:i+2] = ['ਔਂ']

            elif ph[i] == 'ਐ' and ph[i+1] == 'ਂ':
                ph[i:i+2] = ['ਐਂ']

            elif ph[i] == 'ਉ' and (ph[i+1] == 'ਂ' or ph[i+1] == 'ੰ'):
                ph[i:i+2] = ['ਉ']

            elif ph[i] == 'ਊ' and (ph[i+1] == 'ਂ' or ph[i+1] == 'ੰ'):
                ph[i:i+2] = ['ਊਂ']

            elif ph[i] == 'ਏ' and ph[i+1] == 'ਂ':
                ph[i:i+2] = ['ਏਂ']

            elif ph[i] == 'ਅ' and ph[i+1] == 'ੰ':
                ph[i:i+2] = ['ਅੰ']



            i += 1  
    
    result = []
    for i, elem in enumerate(ph):
        if ph[i] in con and (ph[i+1] in NonV or ph[i+1] in NV):
            a=ph[i]+ph[i+1]
            result.append(a)
            ph.pop(i)
        else:
            result.append(elem)
    new_list = result
    
#--------------------------------------------------------------------------------------------------------
 
    res = []
    for word in words:
        temp = ''
        for i in result:
            if i == 's':
                break
            temp += i + " "
        res.append((word,temp))
        result = result[result.index('s') + 1:]

  
#-------------------------------------------IPA---------------------------------------------------------

    new = []
    temp_str = ''

    for element in new_list:
        if element == 's':
            new.append(temp_str)
            new.append(element)
            temp_str = ''
        else:
            temp_str += element
    if temp_str:
        new.append(temp_str)
    
    
  

    for i in range(len(new)):
       if len(new[i]) >= 2 and new[i][-2] in con and new[i][-1] == 'ਅ':
        new[i] = new[i][:-1]
    
    ipa=[]
    for i in new:
        ipa.append(ipa_creation(i))
    
    

    ipa_new = []
   
    for word in words:
        temp = ''
        for i in ipa:
            if i == 's':
                break
            temp += i + " "
        ipa_new.append((word,temp))
        ipa = ipa[ipa.index('s') + 1:]
   

    

#----------------------------------------English----------------------------------------------------------------------
    s=pun_to_eng(trans_word)
    def extract_word(s):
        name = ""
        l=[]
        for char in s:
            if char == "@":
                name = ""
            elif char == "#":
                l.append(name)
            else:
                name += char
        #return l
                
        prev = None
        global result
        result = []
        for item in l:
            if item != prev:
                result.append(item)
            prev = item
        return result
        

    l=extract_word(s)
    
#----------------------------------------------Sound------------------------------------------------------------------------    
    global phoneme_lists
    phoneme_lists = [[]]
    for element in new_list:  # new_list is my actual phonemes which is used futher to produc sound of sentences
        phoneme_lists.append([]) if element == 's' else phoneme_lists[-1].append(element)
    if not phoneme_lists[-1]:
        phoneme_lists.pop()
   

    session['phoneme_lists'] = phoneme_lists

   
    return render_template('phonetic.html',res=res,l=l,ipa_new=ipa_new,phoneme_lists=phoneme_lists)



@app.route('/play', methods=['POST'])
def play():
    if 'submit_button' in request.form:
        # Extract the index of the clicked button from the form data
        button_index = int(request.form['submit_button']) - 1
        
        # Get the corresponding phoneme list from the session context
        phoneme_lists = session['phoneme_lists']
        phoneme_list = phoneme_lists[button_index]
        
        # Play the phoneme list using the sound function
        play_phoneme_list(phoneme_list)
    return '', 204  # Return an empty response with status code 204 (No Content)

 #------------------------------------------------------------------------------------------------------------------------------



    
        












    


if __name__=="__main__":
    app.run(port=8002)