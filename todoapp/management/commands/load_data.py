from django.core.management import BaseCommand
from todoapp.models import *
import openpyxl
from django.contrib.auth.models import User

# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    #Show this when the user types help
    def add_arguments(self, parser):
        parser.add_argument('datafile', type=str)

    # A command must define handle()
    def handle(self, *args, **options):
        excelfile = options['datafile']
        if not excelfile.lower().endswith('.xlsx'):
            print 'Excel file should end with .xlsx : found : ' + excelfile
            return

        wb = openpyxl.load_workbook(excelfile)

        Data = []
        ws = wb.get_sheet_by_name('dummydata')
        for row in ws.rows:
            Data.append([x.value for x in row])

        wb.close()
        #print Data
        for i in range(1,len(Data)):
            if(Data[i][0] == None):
                break
            if Todolist.objects.filter(name=Data[i][0], creation_date=Data[i][1],user=User.objects.get(username=Data[i][2])).count() > 0:
                titem = Todoitem(todolist=Todolist.objects.get(name=Data[i][0],user=User.objects.get(username=Data[i][2])),
                                 description=Data[i][3],completed=Data[i][4], due_by=Data[i][5])

                #print "hi",titem
                titem.save()
            else:
                tlist = Todolist(name=Data[i][0], creation_date=Data[i][1],user=User.objects.get(username=Data[i][2]))
                tlist.save()
                titem = Todoitem(todolist=tlist, description=Data[i][3],
                                 completed=Data[i][4], due_by=Data[i][5])

                #print "bye",tlist,titem

                titem.save()

        pass

