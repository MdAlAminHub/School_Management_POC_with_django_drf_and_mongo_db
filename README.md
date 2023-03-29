
## School_Management_POC with Django, Django Rest Feamework and MongoDB

""" The project is dockerized so there is two pre prerequisite requirments """

1.Docker
2.Docker Compose 

## To Run this Project with docker follow below:

"docker-compose up --build"

the project will run at 
http://localhost:7000/

## To Run this Project without docker follow below:
```
for windows:
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
```
for Linux:
python3 -m venv env
sudo apt source 
source env/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

#### There is a File link to "http://localhost:7000/api/docs/?fbclid=IwAR1M1rLXyxHO_nSYN4kneDO6Kdf41fn0L7elpTosnRQENfd3kwY0rFzsQZ4#/" which has the swagger Collection of API's which are mainly all the API's for the project 

look like below :
![](screenshot/api_docs.png)

for example to add mark for students

![](screenshot/add_mark.png)


## Let's discuss about some key feature visualization :


1.For CRUD operations of Class,Subjects,Students,Teachers,Mark the "school" app is designed.

2.For the automated GPA Grading system you can see the Mark Model

code snippet :

```
class Mark(models.Model):
    GRADE_CHOICES = (
        ('5.00', 'A+'),
        ('4.00', 'A'),
        ('3.50', 'A-'),
        ('3.25', 'B'),
        ('2.00', 'C'),
        ('1.00', 'D'),
        ('0.00', 'F'),
        )
    class_name = models.ForeignKey('school.SchoolClass', on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey('school.Subject', on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey('school.Student', on_delete=models.CASCADE, related_name='marks')
    teacher = models.ForeignKey('school.Teacher', on_delete=models.CASCADE, related_name='marks')
    mark = models.IntegerField()
    grade = models.CharField(max_length=5, null=True, blank=True)
    grade_point = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.mark >= 80:
            self.grade = 'A+'
            self.grade_point = 5.0
        elif self.mark >= 70:
            self.grade = 'A'
            self.grade_point = 4.0
        elif self.mark >= 60:
            self.grade = 'A-'
            self.grade_point = 3.5
        elif self.mark >= 50:
            self.grade = 'B'
            self.grade_point = 3.25
        elif self.mark >= 40:
            self.grade = 'C'
            self.grade_point = 2.0
        elif self.mark >= 33:
            self.grade = 'D'
            self.grade_point = 1.0
        else:
            self.grade = 'F'
            self.grade_point = 0.0
        super().save(*args, **kwargs)

    @property
    def gpa(self):
        return self.student.marks.aggregate(avg_grade_point=Avg('grade_point'))['avg_grade_point']

    class Meta:
        ordering = ('-id',)
        verbose_name = "Mark"
        verbose_name_plural = "Marks"
```

3.The first dashboard summarizing results looks like :
![](screenshot/bar.png)  

4.The second dashboard summarizing results looks like :
![](screenshot/pie.png)  
 
## code behind the bar and pie chart visualization: 

```
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
```