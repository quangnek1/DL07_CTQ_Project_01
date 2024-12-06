import streamlit as st
import pandas as pd
import numpy as np
from underthesea import word_tokenize, pos_tag, sent_tokenize
import regex
import string

# function cần thiết
def get_recommendations(df, ma_san_pham, cosine_sim, nums=5):
    # Get the index of the product that matches the ma_san_pham
    matching_indices = df.index[df['ma_san_pham'] == ma_san_pham].tolist()
    if not matching_indices:
        print(f"No product found with ID: {ma_san_pham}")
        return pd.DataFrame()  # Return an empty DataFrame if no match
    idx = matching_indices[0]

    # Get the pairwise similarity scores of all products with that product
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the products based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the nums most similar products (Ignoring the product itself)
    sim_scores = sim_scores[1:nums+1]

    # Get the product indices
    product_indices = [i[0] for i in sim_scores]

    # Return the top n most similar products as a DataFrame
    return df.iloc[product_indices]
# Hiển thị đề xuất ra bảng
def display_recommended_products(recommended_products, cols=5):
    for i in range(0, len(recommended_products), cols):
        cols = st.columns(cols)
        for j, col in enumerate(cols):
            if i + j < len(recommended_products):
                product = recommended_products.iloc[i + j]
                with col:   
                    st.write(product['ten_san_pham'])                    
                    expander = st.expander(f"Mô tả")
                    product_description = product['mo_ta']
                    truncated_description = ' '.join(product_description.split()[:100]) + '...'
                    expander.write(truncated_description)
                    expander.markdown("Nhấn vào mũi tên để đóng hộp text này.")           

# LOAD EMOJICON
emoji_dict = {}
with open('files/emojicon.txt', 'r', encoding="utf8") as file:
    emoji_lst = file.read().split('\n')
    for line in emoji_lst:
        if '\t' in line:  # Kiểm tra nếu dòng chứa ký tự tab
            try:
                key, value = line.split('\t')
                emoji_dict[key.strip()] = value.strip()  # Loại bỏ khoảng trắng thừa
            except ValueError:
                print(f"Skipped invalid line: {line}")  # In ra nếu dòng không hợp lệ

#################
# LOAD TEENCODE
teen_dict = {}
with open('files/teencode.txt', 'r', encoding="utf8") as file:
    teen_lst = file.read().split('\n')
    for line in teen_lst:
        if '\t' in line:  # Kiểm tra nếu dòng chứa ký tự tab
            try:
                key, value = line.split('\t')
                teen_dict[key.strip()] = value.strip()  # Loại bỏ khoảng trắng thừa
            except ValueError:
                print(f"Skipped invalid line: {line}")

###############
# LOAD TRANSLATE ENGLISH -> VNMESE
english_dict = {}
with open('files/english-vnmese.txt', 'r', encoding="utf8") as file:
    english_lst = file.read().split('\n')
    for line in english_lst:
        if '\t' in line:  # Kiểm tra nếu dòng chứa ký tự tab
            try:
                key, value = line.split('\t')
                english_dict[key.strip()] = value.strip()
            except ValueError:
                print(f"Skipped invalid line: {line}")

################
# LOAD wrong words
with open('files/wrong-word.txt', 'r', encoding="utf8") as file:
    wrong_lst = [word.strip() for word in file.read().split('\n') if word.strip()]  # Loại bỏ dòng trống và khoảng trắng thừa

#################
# LOAD STOPWORDS
with open('files/vietnamese-stopwords.txt', 'r', encoding="utf8") as file:
    stopwords_lst = [word.strip() for word in file.read().split('\n') if word.strip()]  # Loại bỏ dòng trống và khoảng trắng thừa

def process_text(text, emoji_dict, teen_dict, wrong_lst):
    document = text.lower()
    document = document.replace("’", '')
    document = regex.sub(r'\.+', ".", document)

    # Xử lý Emoji
    document = ''.join(emoji_dict[word]+' ' if word in emoji_dict else word for word in list(document))

    # Xử lý Teen Code
    document = ' '.join(teen_dict[word] if word in teen_dict else word for word in document.split())

    # Loại bỏ từ sai
    document = ' '.join('' if word in wrong_lst else word for word in document.split())

    # Loại bỏ khoảng trắng thừa
    document = regex.sub(r'\s+', ' ', document).strip()

    return document

def process_special_word(text):
    new_text = ''
    text_lst = text.split()
    i = 0
    if 'không' in text_lst:
        while i <= len(text_lst) - 1:
            word = text_lst[i]
            if word == 'không':
                next_idx = i + 1
                if next_idx <= len(text_lst) - 1:
                    word = word + '_' + text_lst[next_idx]
                i = next_idx + 1
            else:
                i += 1
            new_text = new_text + word + ' '
    else:
        new_text = text
    return new_text.strip()

# Chuẩn hóa unicode tiếng việt
def loaddicchar():
    uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
    unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"

    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic

# Đưa toàn bộ dữ liệu qua hàm này để chuẩn hóa lại
def covert_unicode(txt):
    dicchar = loaddicchar()
    return regex.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)

def process_special_word(text):
    new_text = ''
    text_lst = text.split()
    i = 0
    while i <= len(text_lst) - 1:
        word = text_lst[i]
        # Nếu từ là "không", kiểm tra từ tiếp theo
        if word == 'không' and i + 1 < len(text_lst):
            next_word = text_lst[i + 1]
            word = f"{word}_{next_word}"  # Nối "không" với từ tiếp theo
            i += 1  # Bỏ qua từ tiếp theo đã được nối
        new_text += word + ' '
        i += 1
    return new_text.strip()

import re
# Hàm để chuẩn hóa các từ có ký tự lặp
def normalize_repeated_characters(text):
    # Thay thế mọi ký tự lặp liên tiếp bằng một ký tự đó
    # Ví dụ: "lònggggg" thành "lòng", "thiệtttt" thành "thiệt"
    return re.sub(r'(.)\1+', r'\1', text)

# Áp dụng hàm chuẩn hóa cho văn bản
# print(normalize_repeated_characters(example))

def process_postag_thesea(text):
    new_document = ''
    for sentence in sent_tokenize(text):
        sentence = sentence.replace('.', '')
        lst_word_type = ['N', 'Np', 'A', 'AB', 'V', 'VB', 'VY', 'R']
        sentence = ' '.join(word[0] if word[1].upper() in lst_word_type else '' for word in pos_tag(process_special_word(word_tokenize(sentence, format="text"))))
        new_document = new_document + sentence + ' '
    new_document = regex.sub(r'\s+', ' ', new_document).strip()
    return new_document

def remove_stopword(text, stopwords):
    document = ' '.join(word for word in text.split() if word not in stopwords)
    return regex.sub(r'\s+', ' ', document).strip()  # Xóa khoảng trắng thừa

def TongHopTienXuLy(text):
    document = process_text(text, emoji_dict, teen_dict, wrong_lst)
    document = normalize_repeated_characters(document)
    document = process_postag_thesea(document)
    document = remove_stopword(document, stopwords_lst)
    return document