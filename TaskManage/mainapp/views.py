from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.views import View
from django.core.paginator import Paginator
from mainapp.models import *
from datetime import datetime,timezone
from django.contrib.auth.models import User
import xlsxwriter
import xlwt
import pandas as pd


# Create your views here.


def download_excel_data(request,task_obj):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    # font_style = xlwt.XFStyle()
    # font_style.font.bold = True

    style = xlwt.XFStyle()

    # font
    font = xlwt.Font()
    font.bold = True
    style.font = font
    # borders
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THICK
    style.borders = borders





    columns = ['Serial Number', 'Task Title', 'Sub Task', 'Actual Work Done (Task)','Issue Faced','possible solution','Time','Status','other notable work','time','Date and Day','Milestone','Sprint Number','Sprint Duration','Person Of Work' ]

    for col_num in range(len(columns)):
        col_width = 256 * 90
        style1 = xlwt.easyxf('pattern: pattern solid, fore_colour blue')
        ws.col(col_num).width = col_width
        ws.write(row_num, col_num, columns[col_num], style1)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # rows = User.objects.all().values_list('username', 'username', 'username', 'username','username','username','username','username','username','username','username','username')
    all_vals = list()
    count = 0
    for tsk in task_obj:
        count+=1
        sep_data = list()
        # sep_data.extend([count,count,count,count,count,count,count,count,count,count,count,count])

        sep_data.extend([count,tsk.name])

        subtask_ls = SubTask.objects.filter(task = tsk)
        sub_task_content = ''
        ct = 0
        for subtsk in subtask_ls:
            ct+=1
            if ct == 1:
                sub_task_content = '1) '
            else:
                sub_task_content ='\n' + sub_task_content + str(ct) + ' ) '
            
            sub_task_content =  sub_task_content +  str(subtsk.name) + '\n'
        sep_data.append(sub_task_content)

        actual_wrk_ls = SubTaskWork.objects.filter(subtask__task = tsk)
        act_wrk_content = ''
        issue_faced_cont = ' 1 ) '
        ct2 = 0
        for act_wrk in actual_wrk_ls:
            ct2+=1
            if ct2 == 1:
                act_wrk_content = '1) '
            else:
                act_wrk_content ='\n' + act_wrk_content + str(ct2) + ' ) '

            act_wrk_content = act_wrk_content +  str(act_wrk.name) + '\n'
            issue_faced_cont = issue_faced_cont + str(act_wrk.description) + '\n' + str(ct2) + ' ) '
        sep_data.extend([act_wrk_content,issue_faced_cont])
        sep_data.append('-')
        start_end_task = str(tsk.taskdetail.start_time) + ' to ' + str(tsk.taskdetail.end_time)
        sep_data.append(start_end_task)        
        sep_data.append(tsk.status.name)
        sep_data.extend(['-','-'])


        sep_data.append(str(tsk.created_date))
        try:
            sep_data.append(tsk.sprint.milestone.name)
        except:
            sep_data.append('-')
        try:
            sep_data.append(tsk.sprint.name)
        except:
            sep_data.append('-')
        sep_data.append('1 week')
        sep_data.append('Ashish')

        sep_data = tuple(sep_data)
        all_vals.append(sep_data)


    rows = all_vals
    for row in rows:
        row_num += 1
        ws.row(row_num).height = 2000
        for col_num in range(len(row)):
            #wrap text in one column
            wrap_style = xlwt.XFStyle()
            wrap_style.alignment.wrap = True
            # print("DATA : ",row[col_num])
            if row[col_num] == "Completed":
                style0 = xlwt.easyxf('font: name Times New Roman, colour_index green')
                style0 = xlwt.easyxf('pattern: pattern solid, fore_colour green')
            elif row[col_num] == "Progress":
                style0 = xlwt.easyxf('font: name Times New Roman, colour_index yellow')
                style0 = xlwt.easyxf('pattern: pattern solid, fore_colour yellow')
            else:
                style0 = xlwt.easyxf('font: name Times New Roman, colour_index black')
            if col_num == 0:
                ws.col(col_num).width = 256 * 10
            else:
                ws.col(col_num).width = 256 * 70

            ws.write(row_num, col_num, row[col_num], style0)

    wb.save(response)

    return response

   





def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def TaskTableData(request):
    not_mine_stat = Status.objects.get(name = "Not Mine Task")
    all_tasks = Task.objects.all().exclude(status =not_mine_stat).order_by('-id')
    all_status = Status.objects.all()
    all_milestones = MileStone.objects.all()
    all_sprints = Sprint.objects.all()
    total_task = Task.objects.exclude(status =not_mine_stat).count()
    pending_task = Task.objects.filter(status__name = "Pending").count()
    bucket_task = Task.objects.filter(status__name = "Bucket").count()
    completed_task = Task.objects.filter(status__name = "Completed").count()
    progress_task = Task.objects.filter(status__name = "Progress").count()
    not_mine_task = Task.objects.filter(status__name = "Not Mine Task").count()
    mine_task = total_task - not_mine_task
    not_mine_tsk = Task.objects.filter(status = not_mine_stat)
    context = { 
        'all_tasks':all_tasks,
        'all_status' : all_status,
        'total_task' : total_task,
        'pending_task' : pending_task,
        'bucket_task' : bucket_task,
        'completed_task' : completed_task,
        'progress_task' : progress_task,
        'mine_task' : mine_task,
        'not_mine' : not_mine_task,
        'all_milestones' : all_milestones,
        'all_sprints' : all_sprints,
        'not_mine_tsk' : not_mine_tsk,
        }
    return context

class IndexView(View):
    def get(self,request,task_id = None):
        context = TaskTableData(request)
        if task_id:
            task_obj = Task.objects.get(id = task_id)
            context['task_detail'] = task_obj
            last_task_code = TaskCodes.objects.filter(task = task_obj).last()
            context['last_task_code'] = last_task_code
        return render(request,'index.html',context)

    def post(self,request,task_id=None):
        if get_client_ip(request) == "172.16.15.34":    # your static ip
            task_name = request.POST.get('task_name')
            if task_id:
                comment = ""
                task_status = request.POST.get('task_status')
                task_description = request.POST.get('task_description')
                task_code = request.POST.get('task_code')
                status_obj = Status.objects.get(id = int(task_status))
                task_obj = Task.objects.get(id = task_id)
                task_detail_obj = TaskDetail.objects.get(task = task_obj)
                if task_name != task_obj.name:
                    comment = f"Task Name changed from {task_obj.name} to {task_name} "
                    TaskHistry.objects.create(task = task_obj,comment = comment)
                if int(task_status) != task_obj.status.id:
                    comment = f"Task Status chnaged from {task_obj.status.name} to {status_obj.name}  "
                    TaskHistry.objects.create(task = task_obj,comment = comment) 
                if (task_description.strip() != task_detail_obj.description):
                    comment = f"task Description Chnages from {task_detail_obj.description} to {task_description} , "
                    TaskHistry.objects.create(task = task_obj,comment = comment)
            
                task_detail_obj.description = task_description
                task_obj.name = task_name
                task_obj.status = status_obj
                try:
                    start_date = request.POST['start_time']
                    print("START DATE : ",start_date)
                    end_date = request.POST['end_time']
                    start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
                    start_date = start_date.replace(tzinfo=timezone.utc)
                    end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
                    end_date = end_date.replace(tzinfo=timezone.utc)
                    task_detail_obj.start_time = start_date
                    task_detail_obj.end_time = end_date

                    if start_date == task_detail_obj.start_time:
                        comment = f"task start date Chnages from {task_detail_obj.start_time} to {start_date}  "
                        TaskHistry.objects.create(task = task_obj,comment = comment)
                    if end_date == task_detail_obj.end_time:
                        comment = f"task end date Chnages from {task_detail_obj.end_time} to {end_date} "
                        TaskHistry.objects.create(task = task_obj,comment = comment)
                except:
                    pass
                task_obj.save()
                task_detail_obj.save()                
                try:
                    task_file_name = request.POST.get('task_file_name')
                    task_file = request.FILES['task_file']
                    TaskFiles.objects.create(name = task_file_name,task = task_obj,task_file = task_file)
                    comment += f"Task file addeed with name {task_file_name} , "
                except:
                    pass
                TaskHistry.objects.create(task = task_obj,comment = comment)
                TaskCodes.objects.create(task = task_obj,code = task_code)
                return redirect('update_task',task_id)
            else:
                task_status = Status.objects.get(name = "Bucket")
                sprint_sel = request.POST.get('sprint_sel')
                sprint_obj = Sprint.objects.get(id = int(sprint_sel))
                task_obj = Task.objects.create(sprint = sprint_obj, name = task_name,status = task_status)
                task_detail_obj = TaskDetail.objects.create(task = task_obj)
                TaskHistry.objects.create(task = task_obj,comment = f"{task_name} created successfully")
                return redirect('index')
        else:
            return HttpResponse("You dont have permission to change here")

def DeleteTask(request,task_id):
    try:
        if get_client_ip(request) == "172.16.15.34":
            task_obj = Task.objects.get(id=task_id)
            task_obj.delete()
            return redirect('/')
        else:
            return HttpResponse("You dont have permission of doing this")
    except Exception as e:
        return HttpResponse(e)

def TaskHistory(request,task_id):
    context = TaskTableData(request)
    task_obj = Task.objects.get(id = task_id)
    task_files = TaskFiles.objects.filter(task = task_obj).order_by("-id")
    task_codes = TaskCodes.objects.filter(task = task_obj).order_by("-id")
    task_hist = TaskHistry.objects.filter(task = task_obj).order_by("-id")
    context['task_history'] = task_hist
    context['task_obj'] = task_obj
    context['task_files'] = task_files
    context['task_codes'] = task_codes
    return render(request,'index.html',context)



class DownloadExcel(View):
    def post(self,request):
        try:
            status_name = request.POST['status_name']
            if status_name == 'All':
                task_obj = Task.objects.all()
            else:
                status_obj = Status.objects.get(name = status_name)
                task_obj = Task.objects.filter(status = status_obj)
            res = download_excel_data(request,task_obj)
            return res

        except Exception as e:
            return HttpResponse(e)


class SubTasks(View):
    def get(self,request,task_id):
        context = TaskTableData(request)
        task_obj = Task.objects.get(id = task_id)
        all_subtask_work =SubTaskWork.objects.filter(subtask__task__id = task_obj.id)
        context['all_subtask_work'] = all_subtask_work
        context['task_subtask'] = task_obj
        all_subtasks = SubTask.objects.filter(task = task_obj).order_by('-id')
        context['all_subtask'] = all_subtasks
        return render(request,'index.html',context)

    def post(self,request,task_id):
        if get_client_ip(request) == "172.16.15.34":
            task_obj = Task.objects.get(id = task_id)
            SubTask.objects.create(task = task_obj,
            name=request.POST['subtask_name'],
            description = request.POST['subtask_description']
            )
            return redirect('subtasks',task_obj.id)
        else:
            return HttpResponse("you dont have permission ... ")


class SubTaskUpdate(View):
    def get(self,request,subtask_id):
        context = TaskTableData(request)
        subtask_obj = SubTask.objects.get(id = subtask_id)
        task_obj = Task.objects.get(id=subtask_obj.task.id)
        all_subtasks = SubTask.objects.filter(task = task_obj).order_by('-id')
        all_subtask_work =SubTaskWork.objects.filter(subtask__task__id = subtask_obj.task.id)
        context['all_subtask_work'] = all_subtask_work
        context['all_subtask'] = all_subtasks
        context['subtask_obj'] = subtask_obj
        return render(request,'index.html',context)

    def post(self,request,subtask_id):
        if get_client_ip(request) == "172.16.15.34":
            try:
                subtask_obj = SubTask.objects.get(id = subtask_id)
                subtask_obj.name = request.POST['subtask_name']
                subtask_obj.description = request.POST['subtask_description']
                subtask_obj.save()
                return redirect('subtask_update',subtask_obj.id)
            except:
                return redirect('subtasks', subtask_id)
        else:
            return HttpResponse("you Dont have Permission")




def SaveSubtaskWork(request,subtask_id):
    if request.method == "POST":
        if get_client_ip(request) == "172.16.15.34":
            subtask_obj = SubTask.objects.get(id = subtask_id)
            SubTaskWork.objects.create(subtask = subtask_obj,name = request.POST['subtask_work_name'],
            description = request.POST.get('subtask_work_description'))
            return redirect('subtasks',subtask_obj.task.id)
    else:
        return HttpResponse("you dont have permission")


def delete_subtask_work(request,sub_work_id):
    if get_client_ip(request) == "172.16.15.34":
        work = SubTaskWork.objects.get(id=sub_work_id)
        task_id = work.subtask.task.id
        work.delete()
        return redirect('subtasks',task_id)
    else:
        return HttpResponse("you dont have permission")


def delete_subtask(request,subtask_id):
    if get_client_ip(request) == "172.16.15.34":
        subtask_obj = SubTask.objects.get(id = subtask_id)
        task_id = subtask_obj.task.id
        subtask_obj.delete()
        return redirect('subtasks',task_id)
    else:
        return HttpResponse("you dont have permission")



def save_milestone(request):
    if request.method == "POST":
        if get_client_ip(request) == "172.16.15.34":
            milestone_name = request.POST['milestone_name']
            MileStone.objects.create(name = milestone_name)
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            return HttpResponse("you dont have permission")


def save_sprint(request):
    if request.method=="POST":
        if get_client_ip(request) == "172.16.15.34":
            Sprint.objects.create(milestone = MileStone.objects.get(id = int(request.POST['milestone'])),
            name = request.POST['sprint']
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            return HttpResponse("You dont have permission")
