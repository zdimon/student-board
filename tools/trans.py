
import googletrans
file = '/Users/dima/develop/it-course/frontend-js-ru/1-vars-math/var-math.md'
f = open(file,'r')
txt = f.read()
f.close()
import string
tmp = txt.split('\n')
file_translate = googletrans.Translator()
result = file_translate.translate(txt, dest='fr')
f = open('rezult.md','w')
f.write(result)
f.close()