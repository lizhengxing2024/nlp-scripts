import pysrt
import re
import json

def has_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

subs = pysrt.open("data/TBBT/S01E01.srt", encoding='utf-8')

result = []

for subtitle in subs:
    text = subtitle.text
    start = subtitle.start
    end = subtitle.end
    duration = subtitle.duration
    
    text = re.sub('{[^}]+}', '', text)
    
    item = {}
    item['start'] = '%02d:%02d:%02d,%03d' % (start.hours, start.minutes, start.seconds, start.milliseconds)
    item['end'] = '%02d:%02d:%02d,%03d' % (end.hours, end.minutes, end.seconds, end.milliseconds)
    item['duration'] = '%02d:%02d:%02d,%03d' % (duration.hours, duration.minutes, duration.seconds, duration.milliseconds)
    item['text'] = text
    
    chs_eng = text.split('\n')
    if len(chs_eng) == 1:
       if has_chinese(chs_eng[0]):
        item['text-zh'] = chs_eng[0].strip()
       else:
        item['text-en'] = chs_eng[0].strip()
    elif len(chs_eng) == 2:
        item['text-zh'] = chs_eng[0].strip()
        item['text-en'] = chs_eng[1].strip()
    else:
        if '《生活大爆炸》' in text:
            print('INGORED:',text)
            continue
        else:
            raise Exception('len(chs_eng) != 2')
    result.append(item)

result_string = json.dumps(result, ensure_ascii=False)

with open('s01e01.json', 'w', encoding='utf-8') as f:
    f.write(result_string)
