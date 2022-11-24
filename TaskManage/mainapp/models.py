from django.db import models
from django.utils import timezone
# Create your models here.



class MileStone(models.Model):
    name = models.CharField(max_length=100,verbose_name="milestone name",unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Sprint(models.Model):
    milestone = models.ForeignKey(to=MileStone,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name="status name",unique=True)
    duration = models.CharField(max_length=100,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name



class Status(models.Model):
    name = models.CharField(max_length=100,verbose_name="status name",unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    sprint = models.ForeignKey(to=Sprint,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=100,verbose_name="task name")
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(to=Status,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TaskDetail(models.Model):
    task = models.OneToOneField(to=Task,on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    start_time = models.DateTimeField(blank=True,null=True,default=timezone.now)
    end_time = models.DateTimeField(blank=True,null=True,default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.task.name



class SubTask(models.Model):
    task = models.ForeignKey(to=Task,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True,null=True)    
    description = models.TextField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class SubTaskWork(models.Model):
    subtask = models.ForeignKey(to=SubTask,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True,null=True)    
    description = models.TextField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class TaskCodes(models.Model):
    task = models.ForeignKey(to=Task,on_delete=models.CASCADE)
    code = models.TextField(default="-")
    created_date = models.DateTimeField(auto_now_add=True)


class TaskFiles(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    task = models.ForeignKey(to=Task,on_delete=models.CASCADE)
    task_file = models.FileField(upload_to = "task_files",blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)



class TaskHistry(models.Model):
    task = models.ForeignKey(to=Task,on_delete=models.CASCADE)
    comment = models.TextField(default='-')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task.name