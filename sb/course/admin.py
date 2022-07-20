from django.contrib import admin
from django.utils.safestring import mark_safe
from course.models import Course, Lesson, Topic, LessonPayments, Comments, Subscription, Lab, Kursak
from django.http import HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name_slug', 'name', 'meta_title', 'order', 'is_active', 'lang']
    list_editable = ['order', 'is_active']
from django.contrib import messages
from .models import NewsLetter
def create_letter(modeladmin, request, queryset):
    try:
        l = NewsLetter.objects.get(title='News')
    except:
        l = NewsLetter()
    l.title = 'News'
    l.save()
    for lesson in queryset:
        l.lesson.add(lesson)
    messages.add_message(request, messages.INFO, 'A letter has been created!')

create_letter.short_description = 'Create a news letter'

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 3

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'name_slug', 'course', 'number', 'desc', 'is_new', 'subscribe_link', 'has_video']
    list_filter = ['course']
    search_fields = ['name_slug', 'title']
    list_editable = ['is_new']
    actions = [create_letter, ]
    inlines = [TopicInline]
    search_fields = ['title']
    

    def subscribe_link(self, obj):
        url = reverse('admin:send_news',args=[obj.id])
        return mark_safe('<a href="%s">Разослать</a>' % url)

    def get_urls(self):
        from django.urls import path
        urls = super(LessonAdmin, self).get_urls()
        myurl = [
            path('send/news/<int:lesson_id>', self.admin_site.admin_view(self.send_news), name="send_news")
        ]
        return myurl+urls

    def send_news(self, request, lesson_id):
        lesson = Lesson.objects.get(pk=lesson_id)
        for s in Subscription.objects.all():
            print('Sent to %s' % s.email)
            title = 'Новый урок - %s' % lesson
            content= '<a href="#">test</a>'
            send_mail(
                title,
                content,
                'zdimon@pressa.ru',
                ['zdimon77@gmail.com'],
                html_message=content,
                fail_silently=False,
            )
        messages.success(request, 'Письма разослал')
        return redirect(reverse('admin:course_lesson_changelist'))


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'filename', 'course', 'lesson', 'video', 'has_video', 'is_youtube', 'order']
    list_filter = ['has_video']
    list_editable = ['order']
    search_fields = ['filename']





@admin.register(LessonPayments)
class LessonPaymentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'created', 'is_paid']
    



from mptt.admin import MPTTModelAdmin

@admin.register(Comments)
class CommentsAdmin(MPTTModelAdmin):
    list_display = ['user', 'content', 'parent']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_subscribed']
    list_editable = ['is_subscribed']

from .models import Catalog, Article

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'filename', 'catalog']
    list_filter = ['catalog']

from .models import NewsLetter

class LessonInline(admin.TabularInline):
    model = NewsLetter.lesson.through
    extra = 3

from course.tasks import send_letters_task
def send_letter(modeladmin, request, queryset):
    for lesson in queryset:
        messages.success(request, 'Письма разослал')
        send_letters_task.delay(lesson.id)
send_letter.short_description = 'Send a news letter'

@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ['title','send_letter_link', 'content']
    inlines = [LessonInline]
    change_list_template = 'admin/newsletter_list.html'
    actions = [send_letter, ]

    def send_news_letter(self, request, letter_id):
        letter = NewsLetter.objects.get(pk=letter_id)
        users = []
        for s in Subscription.objects.filter(is_subscribed=True):
            users.append(s.email)
            
        send_mail(
            letter.title,
            letter.txt_content,
            'zdimon@pressa.ru',
            users,
            html_message=letter.content,
            fail_silently=False,
        )
        messages.success(request, 'Письма разослал %s челикам' % len(users))
        return redirect(reverse('admin:course_newsletter_changelist'))

    def create_news_letter(self, request):
        n = NewsLetter()
        n.title = 'Новое на сайте webmonstr.com'
        n.save()
        for lesson in Lesson.objects.filter(is_new=True):
            n.lesson.add(lesson)
        messages.success(request, 'Письмо создал')
        return redirect(reverse('admin:course_newsletter_changelist'))

    def get_urls(self):
        from django.urls import path
        urls = super(NewsLetterAdmin, self).get_urls()
        myurl = [
            path('send/letter/<int:letter_id>', self.admin_site.admin_view(self.send_news_letter), name="send_news_letter"),
            path('create/letter', self.admin_site.admin_view(self.create_news_letter), name="create_news_letter")
        ]
        return myurl+urls

    def send_letter_link(self, obj):
        url = reverse('admin:send_news_letter',args=[obj.id])
        return mark_safe('<a href="%s">%s</a>' % (url, 'Send the letter'))




@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ['course','lesson']

@admin.register(Kursak)
class KursakAdmin(admin.ModelAdmin):
    list_display = ['course','title', 'file']