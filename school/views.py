from django.views import View
from django.db.models import Sum, Count
from rest_framework.permissions import IsAuthenticated
from .models import Student, Teacher
from django.shortcuts import render
from school.models import SchoolClass, Subject, Mark
from django.db.models import Q, F
from rest_framework import generics, viewsets
from rest_framework.response import Response
from .permissions import IsTeacher
from .serializers import MarkSerializer, SubjectSerializer, SchoolClassSerializer, StudentSerializer, TeacherSerializer


class DashboardNoSqlView(View):
    """
        - This view only used for NoSQL database like Mongodb, Cassandra etc
    """

    def get(self, request, *args, **kwargs):
        context = dict()

        # for drop down data
        context["subjects"] = Subject.objects.all()
        context["class_list"] = SchoolClass.objects.all()

        # get class and subject id from client request
        class_id = request.GET.get('class_id', 1)
        subject_id = request.GET.get('subject_id', None)

        # used to store chart data
        context["result"] = []
        if not subject_id:
            # for first bar chart
            sub_list = Subject.objects.filter(class_name_id=class_id)
            context['total_student'] = Student.objects.filter(class_name_id=class_id).count()
            # collect each subject pass percent, number of students, subject name. subject like Bangla, English etc
            for sub in sub_list:
                # get total pass mark of a subject. like s1=50, s2=50 then total_pass_mark = 50 + 50 = 100
                total_pass_mark = sub.marks.aggregate(
                    total_mark=Sum("mark", distinct=True))["total_mark"]
                # get total mark of a subject. if 2 student of subject then total_mark = 2*100 = 200
                total_mark = sub.marks.filter(mark__gt=33).aggregate(
                    total_mark=Count("mark", distinct=True))["total_mark"] * 100
                # make pass percentage of a subject.
                # if 2 student of subject then pass_percentage = total_pass_mark * 100 / total_mark
                pass_percentage = int((total_pass_mark * 100) / total_mark) if total_pass_mark else 0
                # create each subject bar chart data
                context["result"].append({
                    "name": sub.name,  # subject name
                    "pass_percentage": pass_percentage,
                    "total_student": sub.class_name.students.filter(
                        marks__subject__name=sub.name, marks__mark__gt=33).count(),
                })
            # print(context["result"])
            # print('total_student: ', context["total_student"])
            return render(request, 'chartapp/bar.html', context)
        else:
            # for second bar chart
            # get mark base on class & subject
            mark_objs = Mark.objects.filter(class_name_id=class_id, subject_id=subject_id)
            # get total student because each student have at least one grade like A+, F etc
            context['total_student'] = mark_objs.count()
            # collect each grade percent, number of students. grade like A+, B, C, D, F etc
            for d in Mark.GRADE_CHOICES:
                # get total student of a grade like A+,B
                grade_total_student = mark_objs.filter(grade=d[1]).aggregate(total_sum=Count('grade'))["total_sum"]
                # calculate percentage of a grade
                percentage = int((grade_total_student * 100) / context['total_student']) if grade_total_student else 0
                # create each grade pie chart data
                context["result"].append({
                    "grade": d[1],  # grade name
                    "percentage": percentage,  # percent against student number
                    "grade_total_student": grade_total_student,  # total student of a grade
                })
            # print(context["result"])
            # print('total_student: ', context["total_student"])
            return render(request, 'chartapp/pie.html', context)


class DashboardSqlView(View):
    """
        - This view only used for SQL database like sqlite3, PostgreSQL, MYSQL etc
    """

    def get(self, request, *args, **kwargs):
        context = dict()

        # for drop down data
        context["subjects"] = Subject.objects.all()
        context["class_list"] = SchoolClass.objects.all()

        # get class and subject id from client request
        class_id = request.GET.get('class_id', 1)
        subject_id = request.GET.get('subject_id', None)

        # used to store chart data
        context["result"] = []
        if not subject_id:
            # for first bar chart
            # collect each subject pass percent, number of students, subject name. subject like Bangla, English etc
            context['result'] = Subject.objects.filter(class_name_id=class_id) \
                .annotate(
                total_student=Count('class_name__students',
                                    filter=Q(class_name__students__marks__mark__gt=33) \
                                           & Q(class_name__students__marks__subject__name=F('name')), distinct=True),
                pass_percentage=(Sum("marks__mark", \
                                     filter=Q(marks__mark__gt=33), \
                                     distinct=True) * 100) / (Count("marks__mark", distinct=True) * 100),
            ).values('name', 'pass_percentage', 'total_student')
            # get total student of this class
            context['total_student'] = Student.objects.filter(class_name_id=class_id).count()
            # print(context["result"])
            # print('total_student: ', context["total_student"])
            return render(request, 'chartapp/bar.html', context)
        else:
            # for second bar chart
            mark_objs = Mark.objects.filter(class_name_id=class_id, subject_id=subject_id)
            # get total student of this class
            context['total_student'] = mark_objs.count()
            # collect each grade percent, number of students, grade name. grade like A+, B, C, D, F etc
            context['result'] = mark_objs.values('grade').annotate(
                total_student=Count('grade'), percentage=(Count('grade') * 100) / context['total_student']).order_by()
            # print(context["result"])
            # print('total_student: ', context["total_student"])
            return render(request, 'chartapp/pie.html', context)


class MarkViewSet(viewsets.ModelViewSet):
    serializer_class = MarkSerializer
    permission_classes = [IsTeacher]
    queryset = Mark.objects.all()


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all()


class ClassViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated]
    queryset = SchoolClass.objects.all()


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    queryset = Teacher.objects.all()
