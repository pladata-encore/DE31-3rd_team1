from django.shortcuts import render
from django.db import connection,connections
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import io
import base64
from gtts import gTTS
import os

# 한글 폰트 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 경로를 자신의 시스템에 맞게 수정
font_prop = fm.FontProperties(fname=font_path)
plt.rc('font', family=font_prop.get_name())


def word(request):
    date = request.GET.get('input-date')
    
    if date:
        table_name = f"`{date}`"
    else:
        table_name = '`2024-07-01`'  # 기본값 설정

    # 동적으로 테이블 이름을 설정하여 데이터 가져오기
    with connections['default'].cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        rows = cursor.fetchall()
    


    # 데이터를 쉽게 사용할 수 있도록 리스트로 변환
    word_data = [{'Keyword': row[0], 'count': row[1]} for row in rows]

      
    word_freq = {item['Keyword']: item['count'] for item in word_data}
    wordcloud = WordCloud(width=800, height=600, background_color='white', font_path=font_path).generate_from_frequencies(word_freq)
    
    img = io.BytesIO()
    plt.rcParams["font.family"] = 'NanumGothic'
    #font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(img, format='png')
    img.seek(0)
    
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return render(request, 'word/word.html', {'word_data': word_data, 'wordcloud': img_base64})



    
    