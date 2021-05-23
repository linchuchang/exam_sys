import win32timezone
from django.db import models

SEX = (('male', '男'), ('female', '女'))
# Create your models here.
class Student(models.Model):

    GRADE = (('one', '大一'), ('two', '大二'), ('three', '大三'), ('four', '大四'))

    student_number = models.CharField("学号", max_length=8, default='123')
    name = models.CharField("姓名", max_length=256, unique=False)
    password = models.CharField("密码", max_length=128, default='123')
    grade = models.CharField("年级", max_length=5, choices=GRADE)
    sex = models.CharField("性别", max_length=6, choices=SEX, default='男')
    email = models.EmailField("邮箱", max_length=50, unique=True)
    major = models.CharField("专业名称", max_length=10)
    # institution = models.CharField("机构名称", choices=);

    def __str__(self):
        return self.name

class Teacher(models.Model):
    Teacher_number = models.CharField("学号", max_length=8, default='123')
    name = models.CharField("姓名", max_length=256, unique=False)
    password = models.CharField("密码", max_length=128, default='123')
    sex = models.CharField("性别", max_length=6, choices=SEX, default='男')
    email = models.EmailField("邮箱", max_length=50, unique=True)

    def __str__(self):
        return self.name

class Test_Questions(models.Model):
    ANSWER = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    LEVEL = {
        ('easy', 'easy'),
        ('general', 'general'),
        ('difficult', 'difficult'),
    }
    Question_number = models.AutoField(primary_key=True)
    subject = models.CharField('科目', max_length=512)
    title = models.TextField('题目')
    optionA = models.CharField('A选项', max_length=512)
    optionB = models.CharField('B选项', max_length=512)
    optionC = models.CharField('C选项', max_length=512)
    optionD = models.CharField('D选项', max_length=512)
    answer = models.CharField('答案', max_length=512, choices=ANSWER)
    level = models.CharField('等级', max_length=10, choices=LEVEL)
    score = models.IntegerField('分数', default=1)

    class Meta:
        db_table = 'question'
        verbose_name = '单项选择题库'
        verbose_name_plural = verbose_name
        ordering = ('Question_number',)

    def __str__(self):
        return '<%s:%s>' % (self.subject, self.title);

class Paper(models.Model):
    #题号pid 和题库为多对多的关系
    pid = models.ManyToManyField(Test_Questions)#多对多
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE)#添加外键
    subject = models.CharField('科目', max_length=20, default='')
    major = models.CharField('考卷适用专业', max_length=20)
    examtime = models.DateTimeField()


    class Meta:
        db_table = 'paper'
        verbose_name = '试卷'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.major;


