import cmd
from option import *
import os
import cmd
from colorama import *
from definitions import *

class Backdoor(object, cmd.Cmd):
    def __init__(self, core):
        self.options = {}
        self.core = core
        self.modules = {} 
    def check_valid(self):
        return False
    
    def do_add(self, line): 
        if line in self.core.enabled_modules.keys():
            mod = self.core.enabled_modules[line](self.target, self.command, self.core)
            self.modules[mod] = mod.options
            self.enabled_modules[line] = mod
            print(GOOD + mod.name + " module added")
        else:
            print(BAD + "No module by that name available")


    def set_target(target):
        self.options['target'] = target

    def set_option(option, value):
        if option in self.options.keys():
            self.options[option] = value
            return True
        else:
            return False

    def do_exploit():
        return False

    def do_show(self, args):
        if args == "options":
            self.do_help(args)
        else:
            print BAD + "Unknown option %s", args
    
    def do_set(self, args):
        args = args.split(" ")
        if len(args) == 2 and args[0] in self.options:
            self.options[args[0].lower()].value = args[1]
            print "%s => %s" % (args[0], args[1])
        elif len(args) != 2:
            print "Please supply a variable and an option"
            print "Usage: set LHOST 10.1.0.1"
        else:
            print BAD + "Unknown option %s", args[0]

    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None


    def do_EOF(self, line):
        print ""
        return True
    def emptyline(self):
        return
    def precmd(self, line):
        self._hist += [ line.strip() ]
        return line 
    def default(self, line):       
        try:
            print GOOD + "Executing \"" + line + "\""
            os.system(line)
        except Exception, e:
            print e.__class__, ":", e 
    def do_history(self, args):
        print self._hist
    def default(self, line): 
        self.core.onecmd(line)
    def do_quit(self, args):
        print "Exiting"
        exit()
    def do_help(self, args):
        print "Backdoor options: "
        print("")
        print "Option\t\tValue\t\tDescription\t\tRequired"
        print "------\t\t-----\t\t-----------\t\t--------"
        for name, opt in self.options.iteritems():
            print("%s\t\t%s\t\t%s\t\t%s" % (opt.name, opt.value, opt.description, opt.required))
        if self.modules != {}:
            for mod in self.modules:
                print("\n%s module options: \n" % mod.name)
                print "Option\t\tValue\t\tDescription\t\tRequired"
                print "------\t\t-----\t\t-----------\t\t--------"

                for name, opt in mod.options.iteritems():
                    print("%s\t\t%s\t\t%s\t\t%s" % (opt.name, opt.value, opt.description, opt.required))

    def do_remove(self, args):
        print self.modules.keys()
        if args in self.enabled_modules.keys():
            
            mod = self.enabled_modules[args]
            self.modules.pop(mod, None)
            self.enabled_modules.pop(args, None)
            print(GOOD + "Removed %s module." % args)
        else:
            print(BAD + "No module by that name enabled")

    def preloop(self):
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}


