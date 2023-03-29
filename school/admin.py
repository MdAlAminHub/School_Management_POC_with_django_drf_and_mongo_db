from django.contrib import admin
from .models import Subject, SchoolClass, Student, Teacher, Mark


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name')
    list_filter = ('class_name',)


admin.site.register(Teacher)


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'student', 'subject', 'teacher', 'mark', 'grade', 'grade_point')
    list_filter = ('student__class_name', 'subject', 'teacher')

    # add_form_template = 'index.html'
    # change_form_template = 'index.html'
    # delete_confirmation_template = 'index.html'

    def get_mark(self, obj):
        return obj.mark

    get_mark.short_description = 'Mark'

    def grade(self, obj):
        return obj.get_grade_display()

    # gpa.short_description = 'GPA'
