"""
   This script can be used to define using dumpbin.exe
   whether the library is compiled using /MT or /MD flag 
   
   Author: Victor Yastrebov
   Initial work: https://github.com/victor-yastrebov/MtMdChecker
"""

from subprocess import Popen, PIPE
import ntpath

# execute cmd command
def SystemExecute( cmd_line, verbose_output = False ) :
    print( 'Executing: ' + cmd_line )
    process = Popen(cmd_line, stdout=PIPE, shell=True)

    while True :
       line = process.stdout.readline().rstrip()
       if not line :
          break
       if( verbose_output ) : 
          print( line.decode( "utf-8" ) )

    process.communicate()   # wait till process has ended
    print( 'Executing DONE\n')

# get rid of leading and trailing ' ' and \n characters 
def preprocessString(fileName) :
   return fileName.strip();

# create cmd line command for DumpBin.exe
def createDumpBinCmd(fileName, pathToDumpBin) :
   dumpBinFlag = "/directives"

   outputFilename = "dirs_" + ntpath.basename(fileName) + ".txt"
   redirectOutputCmd = "> " + outputFilename
   
   stringList = [pathToDumpBin, dumpBinFlag, fileName, redirectOutputCmd]
   # concatenate strings via ' '
   return [' '.join(string for string in stringList), outputFilename]

# check whether library is build using MD or MT
def checkMdOrMt(fileName) :
   
   isMT = False
   isMD = False

   with open(fileName) as fp:  
      for line in fp:
         if(line.find('libcmt') != -1) :
            isMT = True
         if(line.find('msvcrt') != -1) :
            isMD = True

   if(isMT and isMD ):
      return "MT_MD"
   elif(isMT):
      return "MT"
   elif(isMD):
      return "MD"
   else :
      return "UNKNOWN"
   
# entry point for application
if __name__ == "__main__" :
   
   # specify all pathes here
   inputFileName = "input_example.txt";
   outputFileName = "results.txt";
   pathToDumpBin = "C:\\\"Program Files (x86)\"\\\"Microsoft Visual Studio 14.0\"\\VC\\bin\\dumpbin.exe"
   
   with open(inputFileName) as fp:  
      for srcFileName in fp:
         
         # do not process comments and empty lines
         if(srcFileName[0] == '#' or srcFileName[0] == '\n') :
            continue
         
         preprocFileName = preprocessString(srcFileName)

         [cmdLine, outputFile] = createDumpBinCmd(preprocFileName, pathToDumpBin);
         SystemExecute(cmdLine, False)
         statusMdMt = checkMdOrMt(outputFile)
         
         with open(outputFileName, "a") as outfile:
            outfile.write(preprocFileName + ": " + statusMdMt + "\n")
         
   print("Done!")
         