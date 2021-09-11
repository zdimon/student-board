# from course.models import NewsLetter, Lesson
# from pl.settings import DOMAIN 

# def create_news_letter():
    #tmp = []
    # for lesson in Lesson.objects.filter(is_new=True):
        # html = '''
        #     <p>
        #         <a href="%s%s"> %s </a>
        #     </p>
        # ''' % (DOMAIN,lesson.get_absolute_url(),lesson.title)
        # tmp.append(html)
    #out = '<br />'.join(tmp)

def get_credits(ammount):

    if ammount == 50:
        return 2
    if ammount == 100:
        return 5
    if ammount == 200:
        return 10
    if ammount == 400:
        return 20
    if ammount == 700:
        return 40
    return 0
