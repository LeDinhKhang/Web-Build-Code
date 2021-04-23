from django.shortcuts import render
from django.http import HttpResponse
import subprocess, shlex, os
 # Create your views here.
def home(request):
   return render(request, "home.html",{})


# xu li bai tap
def linkex1(request):
   ex = request.GET['ex']
   return render(request, "exercise.html",{"ex":ex})

# li thuyet
def theory(request):
   thry = request.GET['id_theory']
   print(thry)
   return render(request, "theory.html",{})

# build code 
def buildcode(request):
   inputcode = request.POST["inputcode"]
   language = request.POST["language"]
   inputvalue = request.POST["input_value"]
   if language =="java":
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
   elif language == "python":
      class_name="python.py"
      f1=open(class_name,"a")
      f1.truncate(0)
      f1.write(inputcode)
      f1.close()
      param=shlex.split("docker run --rm -it -v "+os.getcwd()+":/data --name 'pythoncompile' ubuntu:20.04 python3 /data/python.py" )
         
      test_compile = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      output_compile,err = test_compile.communicate()
      outputcode = str(output_compile,'utf-8')
      print(output_compile)
      return render(request, 'home.html',{"outputcode":outputcode , "inputcode":inputcode,"language":language}) 
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
      return render(request, 'home.html',{"outputcode": outputcode_csharp[28:-7], "inputcode":inputcode,"language":language})  

# build code bai tap
def buildcode_ex(request):
   inputcode = request.POST["inputcode"]
   language = request.POST["language"]
   if language == "python":
      return render(request, 'home.html',{"outputcode": language, "inputcode":inputcode})   
   else:
      return render(request, 'home.html', {"outputcode": "không biết"})
# quay lai
def back(request):
   location = request.GET['ex']
   print(location)
   return render(request, 'home.html', {})