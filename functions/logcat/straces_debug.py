#!/usr/bin/env python
# -*- coding:utf-8 -*-
import getopt
import os
import re
import string
import sys
import getpass
import urllib
import subprocess


def PrintUsage():
  print
  print "  usage: " + sys.argv[0] + " [options] [FILE]"
  print
  print "  --symbols-dir=path"
  print "       the path to a symbols dir, such as =/tmp/out/target/product/dream/symbols"
  print
  print "  --symbols-zip=path"
  print "       the path to a symbols zip file, such as =dream-symbols-12345.zip"
  print
  print "  --auto"
  print "       attempt to:"
  print "         1) automatically find the build number in the crash"
  print "         2) if it's an official build, download the symbols "
  print "            from the build server, and use them"
  print
  print "  FILE should contain a stack trace in it somewhere"
  print "       the tool will find that and re-print it with"
  print "       source files and line numbers.  If you don't"
  print "       pass FILE, or if file is -, it reads from"
  print "       stdin."
  print
  sys.exit(1)

def FindSymbolsDir():
  cmd = "CALLED_FROM_SETUP=true make -f build/core/envsetup.mk " \
      + "dumpvar-abs-TARGET_OUT_UNSTRIPPED"
  stream = os.popen(cmd)
  str = stream.read()
  stream.close()
  return str.strip()

# returns a list containing the function name and the file/lineno
def CallAddr2Line(lib, addr):
  uname = os.uname()[0]
  if uname == "Darwin":
    proc = os.uname()[-1]
    if proc == "i386":
      uname = "darwin-x86"
    else:
      uname = "darwin-ppc"
  if lib != "":
    #cmd = "./prebuilt/" + uname + "/toolchain-eabi-4.2.1/bin/arm-eabi-addr2line" \
    cmd = "arm-eabi-addr2line" \
        + " -f -e " + SYMBOLS_DIR + lib \
        + " 0x" + addr
    stream = os.popen(cmd)
    lines = stream.readlines()
    list = map(string.strip, lines)
  else:
    list = []
  if list != []:
    # Name like "move_forward_type<JavaVMOption>" causes troubles
    mangled_name = re.sub('<', '\<', list[0]);
    mangled_name = re.sub('>', '\>', mangled_name);
    #cmd = "./prebuilt/" + uname + "/toolchain-eabi-4.2.1/bin/arm-eabi-c++filt "\
    cmd = "arm-eabi-c++filt "\
          + mangled_name
    stream = os.popen(cmd)
    list[0] = stream.readline()
    stream.close()
    list = map(string.strip, list)
  else:
    list = [ "(unknown)", "(unknown)" ]
  return list

class SSOCookie(object):
  """
  creates a cookie file so we can download files from the build server
  """
  def __init__(self, cookiename=".sso.cookie", keep=False):
    self.sso_server = "login.corp.google.com"
    self.name = cookiename
    self.keeper = keep
    self.tmp_opts = ".curl.options"
    if not os.path.exists(self.name):
      user = os.environ['USER']
      print "\n%s, to access the symbols, please enter your LDAP " % user,
      password = getpass.getpass()
      params = urllib.urlencode({"u": user, "pw": password})
      fd = os.open(self.tmp_opts, os.O_RDWR | os.O_CREAT, 0600)
      os.write(fd, '-b "%s"\n' % self.name)
      os.write(fd, '-c "%s"\n' % self.name)
      os.write(fd, '-s"\n-L\n-d "%s"\n' % params)
      os.write(fd, 'url = "https://%s/login?ssoformat=CORP_SSO"\n' %
               self.sso_server)
      # login to SSO
      response = os.popen("/usr/bin/curl -K %s" % self.tmp_opts)
      response.close()
      if os.path.exists(self.tmp_opts):
        os.remove(self.tmp_opts)
      if os.path.exists(self.name):
        os.chmod(self.name, 0600)
      else:
        print "Could not log in to SSO"
        sys.exit(1)
  def __del__(self):
      """clean up"""
      if not self.keeper:
        os.remove(self.name)


class NoBuildIDException(Exception):
  pass

def FindBuildFingerprint(lines):
  """
  Searches the given file (array of lines) for the build fingerprint information
  """
  fingerprint_regex = re.compile("^.*Build fingerprint:\s'(?P<fingerprint>.*)'")
  for line in lines:
    fingerprint_search = fingerprint_regex.match(line.strip())
    if fingerprint_search:
      return fingerprint_search.group('fingerprint')

  return None  # didn't find the fingerprint string, so return none



class SymbolDownloadException(Exception):
  pass

DEFAULT_SYMROOT = "/tmp/symbols"
def DownloadSymbols(fingerprint, cookie):
  """
  Attempts to download the symbols from the build server, extracts them,
  and returns the path.  Takes the fingerprint from the pasted stack trace
  and the SSOCookie
  """
  if fingerprint is None:
    return (None, None)
  symdir = "%s/%s" % (DEFAULT_SYMROOT, hash(fingerprint))
  if not os.path.exists(symdir):
    os.makedirs(symdir)
  # build server figures out the branch based on the CL
  params = {
              'op': "GET-SYMBOLS-LINK",
              'fingerprint': fingerprint,
           }
  url = urllib.urlopen("http://android-build/buildbot-update?",
                            urllib.urlencode(params)).readlines()[0]
  if url == "":
    raise SymbolDownloadException, "Build server down? Failed to find syms..."

  regex_str = (r'(?P<baseURL>http\:\/\/android-build\/builds\/.*\/[0-9]+' +
           r'\/)(?P<img>.*)')
  url_regex = re.compile(regex_str)
  url_match = url_regex.match(url)
  if url_match is None:
    raise SymbolDownloadException, "Unexpected results from build server URL..."

  baseURL = url_match.group('baseURL')
  img =  url_match.group('img')
  symbolfile = img.replace("-img-", "-symbols-")
  symurl = baseURL + symbolfile
  localsyms = symdir + symbolfile

  if not os.path.exists(localsyms):
    print "downloading %s ..." % symurl
    curlcmd = ("""/usr/bin/curl -b %s -sL -w %%{http_code} -o %s %s""" %
                          (cookie.name, localsyms, symurl))
    (fi,fo,fe) = os.popen3(curlcmd)
    fi.close()
    code = fo.read()
    err = fe.read()
    if err != "":
      raise SymbolDownloadException, "stderr from curl download: %s" % err
    if code != "200":
      raise SymbolDownloadException, "Faied to download %s" % symurl
  else:
    print "using existing cache for symbols"

  print "extracting %s..." % symbolfile
  saveddir = os.getcwd()
  os.chdir(symdir)
  unzipcode = subprocess.call(["unzip", "-qq", "-o", localsyms])
  if unzipcode > 0:
    raise SymbolDownloadException, ("failed to extract symbol files (%s)."
                             % localsyms)
  os.chdir(saveddir)

  return (symdir, "%s/out/target/product/dream/symbols" % symdir)


def UnzipSymbols(symbolfile):
  """Unzips a file to DEFAULT_SYMROOT and returns the unzipped location.

  Args:
    symbolfile: The .zip file to unzip

  Returns:
    A tuple containing (the directory into which the zip file was unzipped,
    the path to the "symbols" directory in the unzipped file).  To clean
    up, the caller can delete the first element of the tuple.

  Raises:
    SymbolDownloadException: When the unzip fails.
  """
  symdir = "%s/%s" % (DEFAULT_SYMROOT, hash(symbolfile))
  if not os.path.exists(symdir):
    os.makedirs(symdir)

  print "extracting %s..." % symbolfile
  saveddir = os.getcwd()
  os.chdir(symdir)
  unzipcode = subprocess.call(["unzip", "-qq", "-o", symbolfile])
  if unzipcode > 0:
    raise SymbolDownloadException, ("failed to extract symbol files (%s)."
                             % symbolfile)
  os.chdir(saveddir)

  return (symdir, "%s/out/target/product/dream/symbols" % symdir)


def PrintTraceLines(traceLines):
    maxlen = max(map(lambda tl: len(tl[1]), traceLines))
    print
    print "Stack Trace:"
    print "  ADDR      " + "FUNCTION".ljust(maxlen) + "  FILE:LINE"
    for tl in traceLines:
      print "  " + tl[0] + "  " + tl[1].ljust(maxlen) + "  " + tl[2]
    return


def PrintValueLines(valueLines):
    print
    print "Stack Data:"
    print "  ADDR      VALUE     " + "FILE:LINE/FUNCTION"
    for vl in valueLines:
      print "  " + vl[1] + "  " + vl[2] + "  " + vl[4]
      if vl[4] != "":
        print "                      " + vl[3]
    return


def ConvertTrace(lines):
  PROCESS_INFO_LINE = re.compile("(pid: [0-9]+, tid: [0-9]+.*)")
  SIGNAL_LINE = re.compile("(signal [0-9]+ \(.*\).*)")
  REGISTER_LINE = re.compile("(([ ]*[0-9a-z]{2} [0-9a-f]{8}){4})")
  TRACE_LINE = re.compile("(.*)\#([0-9]+)  (..) ([0-9a-f]{3})([0-9a-f]{5})  ([^\r\n \t]*)")
  VALUE_LINE = re.compile("(.*)([0-9a-f]{2})([0-9a-f]{6})  ([0-9a-f]{3})([0-9a-f]{5})  ([^\r\n \t]*)")
  THREAD_LINE = re.compile("(.*)(\-\-\- ){15}\-\-\-")

  traceLines = []
  valueLines = []

  for line in lines:
    header = PROCESS_INFO_LINE.search(line)
    if header:
      print header.group(1)
      continue
    header = SIGNAL_LINE.search(line)
    if header:
      print header.group(1)
      continue
    header = REGISTER_LINE.search(line)
    if header:
      print header.group(1)
      continue
    if TRACE_LINE.match(line):
      match = TRACE_LINE.match(line)
      groups = match.groups()
      if groups[5] == "<unknown>" or groups[5] == "[heap]" or groups[5] == "[stack]":
        traceLines.append((groups[3]+groups[4], groups[5], groups[5]))
      else:
        info = CallAddr2Line(groups[5], groups[4])
        traceLines.append((groups[3]+groups[4], info[0], info[1]))
    if VALUE_LINE.match(line):
      match = VALUE_LINE.match(line)
      groups = match.groups()
      if groups[5] == "<unknown>" or groups[5] == "[heap]" or groups[5] == "[stack]" or groups[5] == "":
        valueLines.append((groups[0], groups[1]+groups[2], groups[3]+groups[4], groups[5], ""))
      else:
        info = CallAddr2Line(groups[5], groups[4])
        valueLines.append((groups[0], groups[1]+groups[2], groups[3]+groups[4], info[0], info[1]))
    header = THREAD_LINE.search(line)
    if header:
      if len(traceLines) > 0:
        PrintTraceLines(traceLines)

      if len(valueLines) > 0:
        PrintValueLines(valueLines)
      traceLines = []
      valueLines = []
      print
      print "-----------------------------------------------------\n"


  if len(traceLines) > 0:
    PrintTraceLines(traceLines)

  if len(valueLines) > 0:
    PrintValueLines(valueLines)


SYMBOLS_DIR = FindSymbolsDir()

if __name__ == '__main__':
  try:
    options, arguments = getopt.getopt(sys.argv[1:], "",
                             ["auto", "symbols-dir=", "symbols-zip=", "help"])
  except getopt.GetoptError, error:
    PrintUsage()

  AUTO = False
  zipArg = None
  for option, value in options:
    if option == "--help":
      PrintUsage()
    elif option == "--symbols-dir":
      SYMBOLS_DIR = value
    elif option == "--symbols-zip":
      zipArg = value
    elif option == "--auto":
      AUTO = True

  if len(arguments) > 1:
    PrintUsage()

  if AUTO:
    cookie = SSOCookie(".symbols.cookie")

  if len(arguments) == 0 or arguments[0] == "-":
    print "Reading native crash info from stdin"
    f = sys.stdin
  else:
    print "Searching for native crashes in %s" % arguments[0]
    f = open(arguments[0], "r")

  lines = f.readlines()
  rootdir = None
  if AUTO:
    fingerprint = FindBuildFingerprint(lines)
    print "fingerprint:", fingerprint
    rootdir, SYMBOLS_DIR = DownloadSymbols(fingerprint, cookie)
  elif zipArg is not None:
    rootdir, SYMBOLS_DIR = UnzipSymbols(zipArg)

  print "Reading symbols from", SYMBOLS_DIR
  lines = ConvertTrace(lines)

  if rootdir is not None:
    # be a good citizen and clean up...os.rmdir and os.removedirs() don't work
    cmd = "rm -rf \"%s\"" % rootdir
    print "\ncleaning up (%s)" % cmd
    os.system(cmd)

  # vi: ts=2 sw=2
