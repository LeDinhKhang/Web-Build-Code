from django.shortcuts import render
from django.http import HttpResponse
import subprocess, shlex, os
from .models import *
 # Create your views here.
def home(request):
   return render(request, "home.html",{})


# xu li bai tap
def linkex(request):
   ex = request.GET['ex']
   ex1 = BaiTap.objects.get(id_bai__exact = ex)
   return render(request, "exercise.html",{"ex":ex1.debai,"maso":ex})

# build code 
def buildcode(request):
   inputcode = request.POST["inputcode"]
   language = request.POST["language"]
   inputvalue = request.POST["input_value"]
   if language =="java":
      if ("readln" in inputcode) | ("read" in inputcode):
         return render(request, 'home.html',{"outputcode": "EOFError: EOF when reading a line", "inputcode":inputcode,"language":language})
      else:
         if inputvalue =="":
            java_class=inputcode.split()[inputcode.split().index('class')+1]
            class_name=java_class+".java"
            f1=open(class_name,"a")
            f1.truncate(0)
            f1.write(inputcode)
            f1.close()
            f2=open("compile.sh","a")
            f2.truncate(0)
            f2.write("cd /data"+"\n"+"javac "+class_name+"\n"+"java "+java_class)
            f2.close()
            
            param=shlex.split("docker run --rm -it -v "+os.getcwd()+":/data --name 'javacompile' ubuntu:20.04 bash /data/compile.sh" )
               
            test_compile = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_compile,err = test_compile.communicate()
            outputcode = str(output_compile,'utf-8')
            return render(request, 'home.html',{"outputcode": outputcode, "inputcode":inputcode,"language":language}) 
         else:
            java_class=inputcode.split()[inputcode.split().index('class')+1]
            class_name=java_class+".java"
            f1=open(class_name,"a")
            f1.truncate(0)
            f1.write(inputcode)
            f1.close()
            f2=open("compile.sh","a")
            f2.truncate(0)
            f2.write("cd /data"+"\n"+"javac "+class_name+"\n"+"java "+java_class+" \"$@\"")
            f2.close()
            
            param=shlex.split("docker run --rm -it -v "+os.getcwd()+":/data --name 'javacompile' ubuntu:20.04 bash /data/compile.sh " + inputvalue)
               
            test_compile = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_compile,err = test_compile.communicate()
            outputcode = str(output_compile,'utf-8')
            return render(request, 'home.html',{"outputcode": outputcode, "inputcode":inputcode,"language":language, "inputvalue":inputvalue})
         
   elif language == "python":
      if ('input' in inputcode):
         return render(request, 'home.html',{"outputcode": "EOFError: EOF when reading a line", "inputcode":inputcode,"language":language, "inputvalue":inputvalue})
      else:
         if inputvalue =="":
            class_name="python.py"
            f1=open(class_name,"a")
            f1.truncate(0)
            f1.write(inputcode)
            f1.close()
            param=shlex.split("docker run --rm -it -v "+os.getcwd()+":/data --name 'pythoncompile' ubuntu:20.04 python3 /data/python.py ")
               
            test_compile = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_compile,err = test_compile.communicate()
            outputcode = str(output_compile,'utf-8')
            print(output_compile)
            return render(request, 'home.html',{"outputcode":outputcode , "inputcode":inputcode,"language":language}) 
         else:
            class_name="python.py"
            f1=open(class_name,"a")
            f1.truncate(0)
            f1.write(inputcode)
            f1.close()
            param=shlex.split("docker run --rm -it -v "+os.getcwd()+":/data --name 'pythoncompile' ubuntu:20.04 python3 /data/python.py " + inputvalue)
               
            test_compile = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_compile,err = test_compile.communicate()
            outputcode = str(output_compile,'utf-8')
            print(output_compile)
            return render(request, 'home.html',{"outputcode":outputcode , "inputcode":inputcode,"language":language, "inputvalue":inputvalue}) 

   else:
      if('readln' in inputcode) | ('readline' in inputcode):
         return render(request, 'home.html',{"outputcode": "EOFError: EOF when reading a line", "inputcode":inputcode,"language":language, "inputvalue":inputvalue})
      else:
         if inputvalue =="":
            class_name="Program.cs"
            f1=open(class_name,"a")
            f1.truncate(0)
            f1.write(inputcode)
            f1.close()
            param=shlex.split("docker run --rm -it -v "+os.getcwd()+":/data --name 'csharpcompile' ubuntu:20.04 /bin/bash -c 'cp /data/Program.cs /data/App/Program.cs && cd /data/App && dotnet run --projectApp'" )
               
            test_compile = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_compile_Csharp,err = test_compile.communicate()
            outputcode_csharp = str(output_compile_Csharp,'utf-8')
            return render(request, 'home.html',{"outputcode": outputcode_csharp[28:-7], "inputcode":inputcode,"language":language}) 
         else:
            class_name="Program.cs"
            f1=open(class_name,"a")
            f1.truncate(0)
            f1.write(inputcode)
            f1.close()
            execute = "cp /data/Program.cs /data/App/Program.cs && cd /data/App && dotnet run " + inputvalue
            param=shlex.split("docker run --rm -it -v "+os.getcwd()+":/data --name 'csharpcompile' ubuntu:20.04 /bin/bash -c '"+ execute +"'")
               
            test_compile = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_compile_Csharp,err = test_compile.communicate()
            outputcode_csharp = str(output_compile_Csharp,'utf-8')
            return render(request, 'home.html',{"outputcode": outputcode_csharp[28:-7], "inputcode":inputcode,"language":language,"inputvalue":inputvalue})  
            
         

# build code bai tap
def buildcode_ex(request):
   inputcode = request.POST["inputcode"]
   language = request.POST["language"]
   id = request.GET["maso"]
   dapan = BaiTap.objects.get(id_bai__exact = id).dapan
   debai = BaiTap.objects.get(id_bai__exact = id).debai
   if language =="java":
      if ("readln" in inputcode) | ("read" in inputcode):
         return render(request, 'exercise.html',{"outputcode": "EOFError: EOF when reading a line", "inputcode":inputcode,"language":language,"result":"incorrect","ex":debai,"maso":id})
      else:
            java_class=inputcode.split()[inputcode.split().index('class')+1]
            class_name=java_class+".java"
            f1=open(class_name,"a")
            f1.truncate(0)
            f1.write(inputcode)
            f1.close()
            f2=open("compile.sh","a")
            f2.truncate(0)
            f2.write("cd /data"+"\n"+"javac "+class_name+"\n"+"java "+java_class)
            f2.close()
            
            param=shlex.split("docker run --rm -it -v "+os.getcwd()+":/data --name 'javacompile' ubuntu:20.04 bash /data/compile.sh" )
               
            test_compile = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_compile,err = test_compile.communicate()
            outputcode = str(output_compile,'utf-8')
            if bytes(outputcode[:-2],'utf-8') == bytes(dapan,'utf-8'):
               return render(request, 'exercise.html',{"outputcode": outputcode, "inputcode":inputcode,"language":language,"result":"correct","ex":debai,"maso":id})
            else:
               return render(request, 'exercise.html',{"outputcode": outputcode, "inputcode":inputcode,"language":language,"result":"incorrect","ex":debai,"maso":id}) 
               
         
   elif language == "python":
      if ('input' in inputcode):
         return render(request, 'exercise.html',{"outputcode": "EOFError: EOF when reading a line", "inputcode":inputcode,"language":language,"ex":debai,"maso":id})
      else:
            class_name="python.py"
            f1=open(class_name,"a")
            f1.truncate(0)
            f1.write(inputcode)
            f1.close()
            param=shlex.split("docker run --rm -it -v "+os.getcwd()+":/data --name 'pythoncompile' ubuntu:20.04 python3 /data/python.py ")
               
            test_compile = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_compile,err = test_compile.communicate()
            outputcode = str(output_compile,'utf-8')
            out = outputcode[:-2]
            if bytes(out,'utf-8') == bytes(dapan,'utf-8'):
               return render(request, 'exercise.html',{"outputcode": outputcode, "inputcode":inputcode,"language":language,"result":"correct","ex":debai,"maso":id})
            else:
               return render(request, 'exercise.html',{"outputcode": outputcode, "inputcode":inputcode,"language":language,"result":"incorrect","ex":debai,"maso":id}) 
         
   else:
      if('readln' in inputcode) | ('readline' in inputcode):
         return render(request, 'exercise.html',{"outputcode": "EOFError: EOF when reading a line", "inputcode":inputcode,"language":language,"ex":debai,"maso":id})
      else:
            class_name="Program.cs"
            f1=open(class_name,"a")
            f1.truncate(0)
            f1.write(inputcode)
            f1.close()
            param=shlex.split("docker run --rm -it -v "+os.getcwd()+":/data --name 'csharpcompile' ubuntu:20.04 /bin/bash -c 'cp /data/Program.cs /data/App/Program.cs && cd /data/App && dotnet run --projectApp'" )
               
            test_compile = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_compile_Csharp,err = test_compile.communicate()
            outputcode_csharp = str(output_compile_Csharp,'utf-8')
            if bytes(dapan,'utf-8') == bytes(outputcode_csharp[28:-9],'utf-8'):
               return render(request, 'exercise.html',{"outputcode": outputcode_csharp[28:-7], "inputcode":inputcode,"language":language,"result":"correct","ex":debai,"maso":id}) 
            else:
               return render(request, 'exercise.html',{"outputcode": outputcode_csharp[28:-7], "inputcode":inputcode,"language":language,"result":"incorrect","ex":debai,"maso":id}) 
               
# quay lai
def back(request):
   location = request.GET['maso']
   if location == '1':
      debai = BaiTap.objects.get(id_bai__exact = location).debai
      return render(request,'exercise.html',{"ex":debai,"maso":location})
   else:
      location = str(int(location) -1)
      debai = BaiTap.objects.get(id_bai__exact = location).debai
      return render(request, 'exercise.html', {"ex":debai,"maso":location})
      

def continue_ex(request):
   location = request.GET['maso']
   if location == '10':
      debai = BaiTap.objects.get(id_bai__exact = location).debai
      return render(request,'exercise.html',{"ex":debai,"maso":location})
   else:
      location = str(int(location) +1)
      debai = BaiTap.objects.get(id_bai__exact = location).debai
      return render(request, 'exercise.html', {"ex":debai,"maso":location})