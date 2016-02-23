# -*- coding: utf-8 -*-
"""

PythonUtils.py  -  utilies for python runner

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================
"""

import sys
import StringIO
from qgis.core import *
from qgis.gui import *

from gabbs.MapUtils import iface, debug_trace

class PythonRunnerImpl(QgsPythonRunner):
    def __init__(self):
        QgsPythonRunner.__init__(self)
        self.pythonUtils = PythonUtilsImpl()

    def runCommand(self, command, messageOnError = ""):
        return self.pythonUtils.runString(command, messageOnError)

    def evalCommand(self, command, result):
        return self.pythonUtils.evalString(command, result)

class PythonUtilsImpl(object):
    def __init__(self):
        object.__init__(self)
        self.mPythonEnabled = True
        self.codeOut = None
        self.codeErr = None

    def isEnabled(self):
        return self.mPythonEnabled

    def installErrorHook(self):
        self.runString("qgis.utils.installErrorHook()")

    def uninstallErrorHook(self):
        self.runString("qgis.utils.uninstallErrorHook()")

    def runStringUnsafe(self, command):
       # capture output and errors
        codeOut = StringIO.StringIO()
        codeErr = StringIO.StringIO()
        sys.stdout = codeOut
        sys.stderr = codeErr
        try:
            exec command.toUtf8().data()
        except:
            pass
        # restore stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        #out = codeOut.getvalue()
        res = (codeErr.getvalue() == "")
        return res

    def runString(self, command, msgOnError):
        res = self.runStringUnsafe(command)
        if (res):
            return True

        if (msgOnError.isEmpty()):
            # use some default message if custom hasn't been specified
            print "error"
        else:
            print msgOnError.toString()
        return False

"""
QgsPythonUtilsImpl::~QgsPythonUtilsImpl()
{
#if SIP_VERSION >= 0x40e06
  exitPython();
#endif
}

bool QgsPythonUtilsImpl::checkSystemImports()
{
  runString( "import sys" ); // import sys module (for display / exception hooks)
  runString( "import os" ); // import os module (for user paths)

  // support for PYTHONSTARTUP-like environment variable: PYQGIS_STARTUP
  // (unlike PYTHONHOME and PYTHONPATH, PYTHONSTARTUP is not supported for embedded interpreter by default)
  // this is different than user's 'startup.py' (below), since it is loaded just after Py_Initialize
  // it is very useful for cleaning sys.path, which may have undesireable paths, or for
  // isolating/loading the initial environ without requiring a virt env, e.g. homebrew or MacPorts installs on Mac
  runString( "pyqgstart = os.getenv('PYQGIS_STARTUP')\n" );
  runString( "if pyqgstart is not None and os.path.exists(pyqgstart): execfile(pyqgstart)\n" );

#ifdef Q_OS_WIN
  runString( "oldhome=None" );
  runString( "if os.environ.has_key('HOME'): oldhome=os.environ['HOME']\n" );
  runString( "os.environ['HOME']=os.environ['USERPROFILE']\n" );
#endif

  // construct a list of plugin paths
  // plugin dirs passed in QGIS_PLUGINPATH env. variable have highest priority (usually empty)
  // locally installed plugins have priority over the system plugins
  // use os.path.expanduser to support usernames with special characters (see #2512)
  QStringList pluginpaths;
  Q_FOREACH ( QString p, extraPluginsPaths() )
  {
    if ( !QDir( p ).exists() )
    {
      QgsMessageOutput* msg = QgsMessageOutput::createMessageOutput();
      msg->setTitle( QObject::tr( "Python error" ) );
      msg->setMessage( QString( QObject::tr( "The extra plugin path '%1' does not exist !" ) ).arg( p ), QgsMessageOutput::MessageText );
      msg->showMessage();
    }
#ifdef Q_OS_WIN
    p.replace( '\\', "\\\\" );
#endif
    // we store here paths in unicode strings
    // the str constant will contain utf8 code (through runString)
    // so we call '...'.decode('utf-8') to make a unicode string
    pluginpaths << '"' + p + "\".decode('utf-8')";
  }
  pluginpaths << homePluginsPath();
  pluginpaths << '"' + pluginsPath() + '"';

  // expect that bindings are installed locally, so add the path to modules
  // also add path to plugins
  QStringList newpaths;
  newpaths << '"' + pythonPath() + '"';
  newpaths << homePythonPath();
  newpaths << pluginpaths;
  runString( "sys.path = [" + newpaths.join( "," ) + "] + sys.path" );

  // import SIP
  if ( !runString( "import sip",
                   QObject::tr( "Couldn't load SIP module." ) + "\n" + QObject::tr( "Python support will be disabled." ) ) )
  {
    return false;
  }

  // set PyQt4 api versions
  QStringList apiV2classes;
  apiV2classes << "QDate" << "QDateTime" << "QString" << "QTextStream" << "QTime" << "QUrl" << "QVariant";
  Q_FOREACH ( const QString& clsName, apiV2classes )
  {
    if ( !runString( QString( "sip.setapi('%1', 2)" ).arg( clsName ),
                     QObject::tr( "Couldn't set SIP API versions." ) + "\n" + QObject::tr( "Python support will be disabled." ) ) )
    {
      return false;
    }
  }

  // import Qt bindings
  if ( !runString( "from PyQt4 import QtCore, QtGui",
                   QObject::tr( "Couldn't load PyQt4." ) + "\n" + QObject::tr( "Python support will be disabled." ) ) )
  {
    return false;
  }

  // import QGIS bindings
  QString error_msg = QObject::tr( "Couldn't load PyQGIS." ) + "\n" + QObject::tr( "Python support will be disabled." );
  if ( !runString( "from qgis.core import *", error_msg ) || !runString( "from qgis.gui import *", error_msg ) )
  {
    return false;
  }

  // import QGIS utils
  error_msg = QObject::tr( "Couldn't load QGIS utils." ) + "\n" + QObject::tr( "Python support will be disabled." );
  if ( !runString( "import qgis.utils", error_msg ) )
  {
    return false;
  }

  // tell the utils script where to look for the plugins
  runString( "qgis.utils.plugin_paths = [" + pluginpaths.join( "," ) + "]" );
  runString( "qgis.utils.sys_plugin_path = \"" + pluginsPath() + "\"" );
  runString( "qgis.utils.home_plugin_path = " + homePluginsPath() );

#ifdef Q_OS_WIN
  runString( "if oldhome: os.environ['HOME']=oldhome\n" );
#endif

  return true;
}


void QgsPythonUtilsImpl::finish()
{
  // release GIL!
  // Later on, we acquire GIL just before doing some Python calls and
  // release GIL again when the work with Python API is done.
  // (i.e. there must be PyGILState_Ensure + PyGILState_Release pair
  // around any calls to Python API, otherwise we may segfault!)
  _mainState = PyEval_SaveThread();
}

bool QgsPythonUtilsImpl::checkQgisUser()
{
  // import QGIS user
  QString error_msg = QObject::tr( "Couldn't load qgis.user." ) + "\n" + QObject::tr( "Python support will be disabled." );
  if ( !runString( "import qgis.user", error_msg ) )
  {
    // Should we really bail because of this?!
    return false;
  }
  return true;
}

void QgsPythonUtilsImpl::doUserImports()
{

  QString startuppath = homePythonPath() + " + \"/startup.py\"";
  runString( "if os.path.exists(" + startuppath + "): from startup import *\n" );
}

void QgsPythonUtilsImpl::initPython( QgisInterface* interface )
{
  init();
  if ( !checkSystemImports() )
  {
    exitPython();
    return;
  }
  // initialize 'iface' object
  runString( "qgis.utils.initInterface(" + QString::number(( unsigned long ) interface ) + ")" );
  if ( !checkQgisUser() )
  {
    exitPython();
    return;
  }
  doUserImports();
  finish();
}


#ifdef HAVE_SERVER_PYTHON_PLUGINS
void QgsPythonUtilsImpl::initServerPython( QgsServerInterface* interface )
{
  init();
  if ( !checkSystemImports() )
  {
    exitPython();
    return;
  }

  // This is the main difference with initInterface() for desktop plugins
  // import QGIS Server bindings
  QString error_msg = QObject::tr( "Couldn't load PyQGIS Server." ) + "\n" + QObject::tr( "Python support will be disabled." );
  if ( !runString( "from qgis.server import *", error_msg ) )
  {
    return;
  }

  // This is the other main difference with initInterface() for desktop plugins
  runString( "qgis.utils.initServerInterface(" + QString::number(( unsigned long ) interface ) + ")" );

  doUserImports();
  finish();
}

bool QgsPythonUtilsImpl::startServerPlugin( QString packageName )
{
  QString output;
  evalString( "qgis.utils.startServerPlugin('" + packageName + "')", output );
  return ( output == "True" );
}

#endif // End HAVE_SERVER_PYTHON_PLUGINS



QString QgsPythonUtilsImpl::getTraceback()
{
#define TRACEBACK_FETCH_ERROR(what) {errMsg = what; goto done;}

  // acquire global interpreter lock to ensure we are in a consistent state
  PyGILState_STATE gstate;
  gstate = PyGILState_Ensure();

  QString errMsg;
  QString result;

  PyObject *modStringIO = NULL;
  PyObject *modTB = NULL;
  PyObject *obStringIO = NULL;
  PyObject *obResult = NULL;

  PyObject *type, *value, *traceback;

  PyErr_Fetch( &type, &value, &traceback );
  PyErr_NormalizeException( &type, &value, &traceback );

  modStringIO = PyImport_ImportModule( "cStringIO" );
  if ( modStringIO == NULL )
    TRACEBACK_FETCH_ERROR( "can't import cStringIO" );

  obStringIO = PyObject_CallMethod( modStringIO, ( char* ) "StringIO", NULL );

  /* Construct a cStringIO object */
  if ( obStringIO == NULL )
    TRACEBACK_FETCH_ERROR( "cStringIO.StringIO() failed" );

  modTB = PyImport_ImportModule( "traceback" );
  if ( modTB == NULL )
    TRACEBACK_FETCH_ERROR( "can't import traceback" );

  obResult = PyObject_CallMethod( modTB, ( char* ) "print_exception",
                                  ( char* ) "OOOOO",
                                  type, value ? value : Py_None,
                                  traceback ? traceback : Py_None,
                                  Py_None,
                                  obStringIO );

  if ( obResult == NULL )
    TRACEBACK_FETCH_ERROR( "traceback.print_exception() failed" );
  Py_DECREF( obResult );

  obResult = PyObject_CallMethod( obStringIO, ( char* ) "getvalue", NULL );
  if ( obResult == NULL )
    TRACEBACK_FETCH_ERROR( "getvalue() failed." );

  /* And it should be a string all ready to go - duplicate it. */
  if ( !PyString_Check( obResult ) )
    TRACEBACK_FETCH_ERROR( "getvalue() did not return a string" );

  result = PyString_AsString( obResult );

done:

  // All finished - first see if we encountered an error
  if ( result.isEmpty() && !errMsg.isEmpty() )
  {
    result = errMsg;
  }

  Py_XDECREF( modStringIO );
  Py_XDECREF( modTB );
  Py_XDECREF( obStringIO );
  Py_XDECREF( obResult );
  Py_XDECREF( value );
  Py_XDECREF( traceback );
  Py_XDECREF( type );

  // we are done calling python API, release global interpreter lock
  PyGILState_Release( gstate );

  return result;
}

QString QgsPythonUtilsImpl::getTypeAsString( PyObject* obj )
{
  if ( obj == NULL )
    return NULL;

  if ( PyClass_Check( obj ) )
  {
    QgsDebugMsg( "got class" );
    return QString( PyString_AsString((( PyClassObject* )obj )->cl_name ) );
  }
  else if ( PyType_Check( obj ) )
  {
    QgsDebugMsg( "got type" );
    return QString((( PyTypeObject* )obj )->tp_name );
  }
  else
  {
    QgsDebugMsg( "got object" );
    return PyObjectToQString( obj );
  }
}

bool QgsPythonUtilsImpl::getError( QString& errorClassName, QString& errorText )
{
  // acquire global interpreter lock to ensure we are in a consistent state
  PyGILState_STATE gstate;
  gstate = PyGILState_Ensure();

  if ( !PyErr_Occurred() )
  {
    PyGILState_Release( gstate );
    return false;
  }

  PyObject* err_type;
  PyObject* err_value;
  PyObject* err_tb;

  // get the exception information and clear error
  PyErr_Fetch( &err_type, &err_value, &err_tb );

  // get exception's class name
  errorClassName = getTypeAsString( err_type );

  // get exception's text
  if ( err_value != NULL && err_value != Py_None )
  {
    errorText = PyObjectToQString( err_value );
  }
  else
    errorText.clear();

  // cleanup
  Py_XDECREF( err_type );
  Py_XDECREF( err_value );
  Py_XDECREF( err_tb );

  // we are done calling python API, release global interpreter lock
  PyGILState_Release( gstate );

  return true;
}


QString QgsPythonUtilsImpl::PyObjectToQString( PyObject* obj )
{
  QString result;

  // is it None?
  if ( obj == Py_None )
  {
    return QString();
  }

  // check whether the object is already a unicode string
  if ( PyUnicode_Check( obj ) )
  {
    PyObject* utf8 = PyUnicode_AsUTF8String( obj );
    if ( utf8 )
      result = QString::fromUtf8( PyString_AS_STRING( utf8 ) );
    else
      result = "(qgis error)";
    Py_XDECREF( utf8 );
    return result;
  }

  // check whether the object is a classical (8-bit) string
  if ( PyString_Check( obj ) )
  {
    return QString::fromUtf8( PyString_AS_STRING( obj ) );
  }

  // it's some other type of object:
  // convert object to unicode string (equivalent to calling unicode(obj) )

  PyObject* obj_uni = PyObject_Unicode( obj ); // obj_uni is new reference
  if ( obj_uni )
  {
    // get utf-8 representation of unicode string (new reference)
    PyObject* obj_utf8 = PyUnicode_AsUTF8String( obj_uni );
    // convert from utf-8 to QString
    if ( obj_utf8 )
      result = QString::fromUtf8( PyString_AsString( obj_utf8 ) );
    else
      result = "(qgis error)";
    Py_XDECREF( obj_utf8 );
    Py_XDECREF( obj_uni );
    return result;
  }

  // if conversion to unicode failed, try to convert it to classic string, i.e. str(obj)
  PyObject* obj_str = PyObject_Str( obj ); // new reference
  if ( obj_str )
  {
    result = QString::fromUtf8( PyString_AS_STRING( obj_str ) );
    Py_XDECREF( obj_str );
    return result;
  }

  // some problem with conversion to unicode string
  QgsDebugMsg( "unable to convert PyObject to a QString!" );
  return "(qgis error)";
}


bool QgsPythonUtilsImpl::evalString( const QString& command, QString& result )
{
  // acquire global interpreter lock to ensure we are in a consistent state
  PyGILState_STATE gstate;
  gstate = PyGILState_Ensure();

  PyObject* res = PyRun_String( command.toUtf8().data(), Py_eval_input, mMainDict, mMainDict );
  bool success = ( res != NULL );

  // TODO: error handling

  if ( success )
    result = PyObjectToQString( res );

  // we are done calling python API, release global interpreter lock
  PyGILState_Release( gstate );

  return success;
}

QString QgsPythonUtilsImpl::pythonPath()
{
  if ( QgsApplication::isRunningFromBuildDir() )
    return QgsApplication::buildOutputPath() + "/python";
  else
    return QgsApplication::pkgDataPath() + "/python";
}

QString QgsPythonUtilsImpl::pluginsPath()
{
  return pythonPath() + "/plugins";
}

QString QgsPythonUtilsImpl::homePythonPath()
{
  QString settingsDir = QgsApplication::qgisSettingsDirPath();
  if ( QDir::cleanPath( settingsDir ) == QDir::homePath() + QString( "/.qgis%1" ).arg( QGis::QGIS_VERSION_INT / 10000 ) )
  {
    return QString( "\"%1/.qgis%2/python\".decode('utf-8')" ).arg( QDir::homePath() ).arg( QGis::QGIS_VERSION_INT / 10000 );
  }
  else
  {
    return '"' + settingsDir.replace( '\\', "\\\\" ) + "python\".decode('utf-8')";
  }
}

QString QgsPythonUtilsImpl::homePluginsPath()
{
  return homePythonPath() + " + \"/plugins\"";
}

QStringList QgsPythonUtilsImpl::extraPluginsPaths()
{
  const char* cpaths = getenv( "QGIS_PLUGINPATH" );
  if ( cpaths == NULL )
    return QStringList();

  QString paths = QString::fromLocal8Bit( cpaths );
#ifndef Q_OS_WIN
  if ( paths.contains( ':' ) )
    return paths.split( ':', QString::SkipEmptyParts );
#endif
  if ( paths.contains( ';' ) )
    return paths.split( ';', QString::SkipEmptyParts );
  else
    return QStringList( paths );
}


QStringList QgsPythonUtilsImpl::pluginList()
{
  runString( "qgis.utils.updateAvailablePlugins()" );

  QString output;
  evalString( "'\\n'.join(qgis.utils.available_plugins)", output );
  return output.split( QChar( '\n' ), QString::SkipEmptyParts );
}

QString QgsPythonUtilsImpl::getPluginMetadata( QString pluginName, QString function )
{
  QString res;
  QString str = "qgis.utils.pluginMetadata('" + pluginName + "', '" + function + "')";
  evalString( str, res );
  //QgsDebugMsg("metadata "+pluginName+" - '"+function+"' = "+res);
  return res;
}

bool QgsPythonUtilsImpl::loadPlugin( QString packageName )
{
  QString output;
  evalString( "qgis.utils.loadPlugin('" + packageName + "')", output );
  return ( output == "True" );
}

bool QgsPythonUtilsImpl::startPlugin( QString packageName )
{
  QString output;
  evalString( "qgis.utils.startPlugin('" + packageName + "')", output );
  return ( output == "True" );
}

bool QgsPythonUtilsImpl::canUninstallPlugin( QString packageName )
{
  QString output;
  evalString( "qgis.utils.canUninstallPlugin('" + packageName + "')", output );
  return ( output == "True" );
}

bool QgsPythonUtilsImpl::unloadPlugin( QString packageName )
{
  QString output;
  evalString( "qgis.utils.unloadPlugin('" + packageName + "')", output );
  return ( output == "True" );
}

bool QgsPythonUtilsImpl::isPluginLoaded( QString packageName )
{
  QString output;
  evalString( "qgis.utils.isPluginLoaded('" + packageName + "')", output );
  return ( output == "True" );
}

QStringList QgsPythonUtilsImpl::listActivePlugins()
{
  QString output;
  evalString( "'\\n'.join(qgis.utils.active_plugins)", output );
  return output.split( QChar( '\n' ), QString::SkipEmptyParts );
}

"""