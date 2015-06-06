#!/usr/bin/python

import os
import commands
import argparse
import urllib
import re
import datetime

from distutils.util import strtobool

verbose = False
cs_debug = False    # only print cs commands w/o execution for debugging this tool
es_debug = False    # only print local commands w/o execution for debugging this tool

vt = "/opt/vde/services/instances/vde_latest/bin/vde_tool "
vtn = vt + "--Vno_sync "


# execute a shell command in dir, output to console, return True if exit code is 0
def shell(cmd, dir="."):
    if verbose or es_debug:
        print(">>> CMD: %s: %s" % (dir, cmd))
    if es_debug:
        return True

    if os.system("cd %s; %s" % (dir, cmd)) != 0:
        raise Exception("Failed to execute \"%s\" under dir \"%s\"." % (cmd, dir))


# execute a shell command in dir, return stdout string
def shell_out(cmd, dir="."):
    if verbose or es_debug:
        print(">>> CMD: %s: %s" % (dir, cmd))
    if es_debug:
        return "NULL"

    rtn = commands.getoutput("cd %s; %s" % (dir, cmd))
    if verbose:
        print(">>> GET: " + rtn)

    return rtn


cec_id = shell_out("logname")

# creg green label publishing page
creg_url = "http://creg-web.cisco.com/labels.php"

# code server alias map
cs_map = {
    "ads":  "sjc-ads-4492",
    "ucs":  "cabu-bld41",
    "ucs1": "cabu-bld38",
    "ucs2": "cabu-bld39",
}

# ios->binos branch map
branch_map = {
    "mcp_dev": {
        "ios":      "mcp_dev",
        "binos":    "main",
    },

    "issu": {
        "ios":      "mcp_cable_issu_test_ios",
        "binos":    "mcp_cable_issu_test_binos",
    },

    "XE316": {
        "ios":      "v155_3_s_xe316_throttle",
        "binos":    "xe316_throttle",
    },

    "ECE6A": {
        "ios":      "ece6a_throttle_ios",
        "binos":    "ece6a_throttle_binos",
    },
}

# product build commands map
product_map = {
    # CBR8 unsigned
    "cbr_unsigned": {
        "dir":           "ios/sys",
        "cmd":           "mcp_ios_precommit DIGI_SIGN=REVOCATION -- -j 16 cbr_super",
        "ext_ios_dir":   "ios/sys/obj-x86_64bi-ubr-iosd ios/sys/obj-mips64-ubr-clc",
        "ext_binos_dir": "linkfarm/iso-cbr",
    },

    # CBR8 signed
    "cbr": {
        "dir":           "ios/sys",
        "cmd":           "mcp_ios_precommit DIGI_SIGN=DEVELOPMENT -- -j 16 cbr_super",
        "ext_ios_dir":   "ios/sys/obj-x86_64bi-ubr-iosd ios/sys/obj-mips64-ubr-clc",
        "ext_binos_dir": "linkfarm/iso-cbr",
        "sign":          True,
    },

    # make dependencies only
    "mkdep": {
        "dir":           "ios/sys",
        "cmd":           "make -j 16 dependencies",
    },
}

# rsym symbol file map
symbol_map = {
    "cbr_super":    "obj-x86_64bi-ubr-iosd/x86_64bi_linux_iosd_ubr-universalk9-ms.symbols",
    "cbr_clc":      "linkfarm/mips64/usr/binos/bin/ubrclc-k9lc-ms.symbols",
}

# IOS sa file map
sa_image_map = {
    "cbr_super":    "x86_64bi_linux_iosd_ubr-universalk9-ms",
    "cbr_clc":      "ubrclc-k9lc-ms",
}

# setws role/res configuration
role_map = {
    "cable_ios": {
        "res":      "vob-src",
    },

    "cable_binos": {
        "res":      "cable-cpp",
        "ws_base":  "/nobackup/" + cec_id,
    },
}


# Yes/No query
def yes_no_query(question):
    print("%s [y/n]" % question)
    while True:
        try:
            return strtobool(raw_input().lower())
        except ValueError:
            print("Please respond with 'y' or 'n'.")


# execute a command on CS
def vshell(cmd, dir=".", sync=False):
    if cs_debug:
        print(">>> VT%s: %s: %s" % (("" if sync else "N"), dir, cmd))
        return True
    shell((vt if sync else vtn) + cmd, dir)


# execute a command on CS and return the stdout string
def vshell_out(cmd, dir=".", sync=False):
    if cs_debug:
        print(">>> VT%s: %s: %s" % (("" if sync else "N"), dir, cmd))
        return "NULL"
    return (shell_out((vt if sync else vtn) + cmd, dir))


# mkdir under root dir on ES
def mkdir(dir, root="."):
    try:
        shell("mkdir -p " + dir, root)
    except Exception:
        pass


# send mail
def mail(address, subject, body):
    tmpName = ".mail_body"
    try:
        fd = open(tmpName, "w")
        fd.write(body)
        fd.close()
    except Exception as e:
        print("Cannot write mail body: %s" % e)

    shell("mail -s \"%s\" \"%s\" < %s" % (subject, address, tmpName))
    shell("rm " + tmpName)


# create workspace
def setws(dir, cs, role):
    if not (role in role_map):
        raise Exception("Unsupportted role: " + role)

    cmd = "--Vforce setws -ws %s -cs %s -role %s -res %s" % (dir, cs, role, role_map[role]["res"])
    if "ws_base" in role_map[role]:
        cmd += " -cs_ws_base " + role_map[role]["ws_base"]
    vshell(cmd)


# destroy workspace
def rmws(dir):
    vshell("cleanws --Vforce", dir)


# get working dir on CS
def get_cs_dir(dir):
    return (vshell_out("pwd", dir))


# sync out filelist
def vout(filelist, dir="."):
    vshell("--Vforce --Vtime 30d --Vreason \"bug fix\" sync_out " + filelist, dir, True)


# sync in filelist
def vin(filelist, dir="."):
    vshell("sync_in " + filelist, dir, True)


# request in permission for filelist
def vrin(filelist, dir="."):
    vshell("request -type in -time 30d --reason \"bug fix\" " + filelist, dir)


# request out permission for filelist
def vrout(filelist, dir="."):
    vshell("request -type out -time 30d --reason \"bug fix\" " + filelist, dir)


# create sign ticket
def vsign(token_pwd, dir="."):
    vshell("abraxas-client.SignEngine -r create-ticket -b CBR -k DEV -n 1000 -U %s -P %s"
           % (cec_id, token_pwd),
           dir)


# set ios view on dir
def setview(name, dir="."):
    vshell("ct setview %s-%s" % (cec_id, name), dir)


# set BINOS_ROOT for ios view
def set_binos_root(ios_dir, binos_dir):
    binos_root = "BINOS_ROOT=%s" % get_cs_dir(binos_dir)
    if verbose:
        print(">>> SET: " + binos_root)
    shell("echo \"%s\" >> .VDEROOT/env.cs" % binos_root, ios_dir)


# create ios view
def vstartios(name, dir, branch, label="LATEST"):
    cmd = "-Vforce start_task -d /nobackup/%s -v /vob/ios -a -t %s" % (cec_id, name)

    if label.upper() != "LATEST":
        cmd += " -l " + label
    else:
        cmd += " -b " + branch

    vshell(cmd + " -ni -f", dir)


# create binos view
def vstartbinos(dir, branch, label="LATEST"):
    vshell("acme nw -sb binos -proj " + branch + "%" + label, dir)


# create ws and pull ios view
def ios_view(name, cs, dir, branch, label="LATEST"):
    setws(dir, cs, "cable_ios")
    vstartios(name, dir, branch, label)
    setview(name, dir)
    shell("echo \"CC_DISABLE_FILEOWNERSHIP_CHECK=1\" >> .VDEROOT/env.cs", dir)


# create ws and pull binos_view
def binos_view(cs, dir, branch, label="LATEST"):
    setws(dir, cs, "cable_binos")
    vstartbinos(dir, branch, label)
    shell("echo \"ACME_DISABLE_COPYRIGHT=1\" >> .VDEROOT/env.cs", dir)


# acme patch
def acme_patch(file, reverse=False, force=False, log=False, dir="."):
    shell("cp %s .tmp.diff" % file, dir)
    vin(".tmp.diff", dir)
    shell("rm -f .tmp.diff", dir)
    print("Start ACME %s <%s>:\n" % (("backout" if reverse else "patch"), file))
    vshell("acme patch%s%s -input .tmp.diff%s"
           % ((" -reverse" if reverse else ""),
              (" -noprompt" if force else ""),
              (" | tee patch.log" if log else "")),
           dir)


# cc_patch
def cc_patch(file, reverse=False, force=False, log=False, dir="."):
    print("Start CC %s <%s>:\n" % (("backout" if reverse else "patch"), file))
    vshell("cc_patch%s%s %s%s"
           % ((" -f" if force else ""),
              (" -p_opts -R" if reverse else ""),
              file,
              (" | tee patch.log" if log else "")),
           dir)


# acme diff
def acme_diff(file, echo=False, dir="."):
    print("Start ACME diff to <%s>%s" % (file, (":\n" if echo else "...")))
    vshell("acme diff %s %s" % (("| tee" if echo else ">"), file), dir)


# cc_diff
def cc_diff(file, echo=False, dir="."):
    print("Start CC diff to <%s>%s" % (file, (":\n" if echo else "...")))
    vshell("cc_diff %s %s" % (("| tee" if echo else ">"), file), dir)


# get all the branch green labels from creg
# sort from latest to oldest
def get_creg_greenlabels(branch):
    try:
        return [
            match.group("label")
            for match in re.finditer(
                "<td [^>]+>"
                + branch
                + "</td><td [^>]+>[^<]+</td><td [^>]+>(?P<label>[A-Z0-9_]+)</td><td [^>]+>(?P=label)</td></tr><tr>",
                urllib.urlopen(creg_url).read(),
                flags=re.MULTILINE)
        ]
    except:
        raise Exception("Cannot query green label from CREG.")


# fix the wrong label name posted on creg webpage
def fix_creg_label(label):
    return "BLD_" + label if label.startswith("MCP_DEV_LATEST_") else label


# parse :120000000+2E1BE0 :120000000+13EECF0 :120000000+5579A8 :120000000+52BED8
def convert_ng_trace_string(trace, need_add):
    rtn = ""
    for frame in re.findall("[0-9A-F+]+\+[0-9A-F+]+", trace, flags=re.MULTILINE):
        if need_add:
            value = 0
            for addr in frame.split("+"):
                value += int(addr, 16)
            rtn += "%X " % value
        else:
            rtn += frame.split("+")[1] + " "
    return rtn


# Execute a shell command, with mail notification
def subcmd_build(args):
    try:
        start_time = datetime.datetime.now()

        cmd = product_map[args.product]["cmd"]
        print(cmd)

        # ignore possible build command error
        try:
            vshell(cmd + " | tee make.log")
        except Exception:
            pass

        end_time = datetime.datetime.now()

        mail_subj = "[vtool] Build %s Finished" % args.product
        mail_bdy = ("Product: %s\n"
                    "Dir: %s\n"
                    "Command: %s\n"
                    "Elapsed: %s\n"
                    "\n"
                    "Result:\n"
                    "%s\n"
                    % (args.product, os.getcwd(), cmd, (end_time - start_time),
                       shell_out("tail -n 13 make.log")))
        mail(cec_id + "@cisco.com", mail_subj, mail_bdy)

    except Exception as e:
        print("Abort: %s" % e)


# get_labels subcommand handler
# list all green labels published by creg from oldest to latest
def subcmd_get_labels(args):
    try:
        branch = args.branch
        print("Detecting green labels for branch <%s> ..." % branch)
        for label in reversed(get_creg_greenlabels(branch)):
            print("* " + fix_creg_label(label))
    except Exception as e:
        print("Abort: %s" % e)


# start_task subcommand handler
# - create ios, binos views
# - build product image
def subcmd_start_task(args):
    global verbose
    verbose = True

    name = args.name
    branch = args.branch
    product = args.product
    label = args.label
    clone_task = args.clone_task
    idiff = args.ios_diff
    bdiff = args.binos_diff
    cs = args.codeserver
    token_pwd = args.token_pwd

    try:
        # expand cs if it is an alias
        if cs in cs_map:
            cs = cs_map[cs]

        # check if we need token password for image sign
        need_sign = False
        try:
            need_sign = product_map[product]["sign"]
        except Exception:
            pass

        if need_sign and token_pwd == "":
            raise Exception("No SofToken password for creating Abraxas Ticket!")

        # check if both ios/binos diff and clone task set
        if clone_task != "" and (idiff != "" or bdiff != ""):
            raise Exception("Cannot specify clone task and extra diff at the same time!")

        start_time = datetime.datetime.now()

        # query green label if needed
        if label.upper() == "AUTO":
            print("Detecting latest green label for branch <%s> ..." % branch)
            labels = get_creg_greenlabels(branch)
            if len(labels) == 0:
                raise Exception("Cannot detect green label!")
            else:
                label = fix_creg_label(labels[0])
                print("Get label: " + label)

        # create task dir
        dir = name + "_" + branch
        mkdir(dir)

        # copy the diff files to task dir before change dir
        if idiff != "":
            shell("cp %s %s/ios_diff.diff" % (idiff, dir))
        if bdiff != "":
            shell("cp %s %s/binos_diff.diff" % (bdiff, dir))

        # collect diff from another task root
        if (clone_task != ""):
            print("Collecting diff from <%s>:" % clone_task)
            wsdirs = [path for path in os.listdir(clone_task) if os.path.isdir("%s/%s/.VDEROOT"
                                                                               % (clone_task, path))]
            diff_dir = "%s/%s" % (os.getcwd(), dir)

            for path in wsdirs:
                if path.startswith("ios_"):
                    idiff = diff_dir + "/ios_diff.diff"
                    cc_diff(idiff, dir="%s/%s" % (clone_task, path))
                elif path.startswith("binos_"):
                    bdiff = diff_dir + "/binos_diff.diff"
                    acme_diff(bdiff, dir="%s/%s" % (clone_task, path))

        # enter task root
        os.chdir(dir)

        # store label
        shell("touch " + label)

        # create ios view
        ios_branch = branch_map[branch]["ios"]
        ios_dir = "ios_" + ios_branch
        mkdir(ios_dir)
        ios_view(name, cs, ios_dir, ios_branch, label)

        # create binos view if needed
        has_binos = "binos" in branch_map[branch]

        if has_binos:
            binos_branch = branch_map[branch]["binos"]
            binos_dir = "binos_" + binos_branch
            mkdir(binos_dir)
            binos_view(cs, binos_dir, binos_branch, label)
            if need_sign:
                vsign(token_pwd, binos_dir)
            set_binos_root(ios_dir, binos_dir)

        # patch diffs if needed
        if idiff != "":
            ios_patch_dir = ios_dir + "/ios/sys"
            mkdir(ios_patch_dir)
            shell("mv ios_diff.diff " + ios_patch_dir)
            cc_patch("ios_diff.diff", force=True, log=True, dir=ios_patch_dir)
            cc_diff("ios_patched.diff", dir=ios_patch_dir)
        if bdiff != "":
            shell("mv binos_diff.diff " + binos_dir)
            acme_patch("binos_diff.diff", force=True, log=True, dir=binos_dir)
            acme_diff("binos_patched.diff", dir=binos_dir)

        # build product image if asked
        build_log = "No pre-build"
        if product in product_map:
            if "ext_ios_dir" in product_map[product]:
                mkdir(product_map[product]["ext_ios_dir"], ios_dir)
            if has_binos and ("ext_binos_dir" in product_map[product]):
                mkdir(product_map[product]["ext_binos_dir"], binos_dir)

            build_dir = ios_dir + "/" + product_map[product]["dir"]
            mkdir(build_dir)

            # ignore possible build command error
            try:
                vshell(product_map[product]["cmd"] + " | tee make.log", build_dir)
                build_log = shell_out("tail -n 13 make.log", build_dir)
            except Exception:
                pass

        end_time = datetime.datetime.now()

        print("\nTask created under: " + dir)

        # send mail notification
        verbose = False
        mail_subj = "[vtool] Task %s created" % name
        mail_bdy = ("Task:    %s\n"
                    "Branch:  %s\n"
                    "Label:   %s\n"
                    "CS:      %s\n"
                    "Root:    %s\n"
                    "Elapsed: %s\n"
                    "\n"
                    "Build result:\n"
                    "%s\n"
                    % (name, branch, label, cs, os.getcwd(), (end_time - start_time), build_log))
        mail(cec_id + "@cisco.com", mail_subj, mail_bdy)

    except Exception as e:
        print("Abort: %s" % e)


# remove_task subcommand handler
def subcmd_remove_task(args):
    try:
        # get all ws dir under task root
        wsdirs = [path for path in os.listdir(".") if os.path.isdir(path + "/.VDEROOT")]

        if len(wsdirs) == 0:
            print("Cannot find any fishbowl workspace")
            return

        print("Find below fishbowl workspaces:")
        for path in wsdirs:
            print("* " + path)

        if yes_no_query("Remove above workspaces?"):
            for path in wsdirs:
                print("\nRemoving workspace in <%s>:" % path)
                rmws(path)
                shell("rmdir " + path)

            print("\nRemove workspaces finished.")
    except Exception as e:
        print("Abort: %s" % e)


def subcmd_diff_task(args):
    # get all ws dir under task root
    wsdirs = [path for path in os.listdir(".") if os.path.isdir(path + "/.VDEROOT")]

    # get task name (current folder name)
    task_name = os.path.basename(os.getcwd())

    if len(wsdirs) == 0:
        print("Cannot find any fishbowl workspace")
        return

    for path in wsdirs:
        if path.startswith("ios_"):
            cc_diff("%s/%s_ios.diff" % (os.getcwd(), task_name), dir=path)
        elif path.startswith("binos_"):
            acme_diff("%s/%s_binos.diff" % (os.getcwd(), task_name), dir=path)


'''
# TODO:
# checkout and syncout
# syncin all checked out files
# auto set legofilter by changeset
'''


# acme_patch subcommand handler
def subcmd_acme_patch(args):
    try:
        acme_patch(args.file, args.reverse)
    except Exception as e:
        print("Abort: %s" % e)


# cc_patch subcommand handler
def subcmd_cc_patch(args):
    try:
        cc_patch(args.file, args.reverse)
    except Exception as e:
        print("Abort: %s" % e)


# acme_sa subcommand handler
def subcmd_acme_sa(args):
    try:
        bugid = args.bugid
        print("Collecting diff...")
        vshell("acme diff > .tmp.diff")
        vin(".tmp.diff")
        shell("rm -f .tmp.diff")
        print("Start SA for <%s>:" % bugid)
        vshell("static_binos -diff_file .tmp.diff -bugid " + bugid)
    except Exception as e:
        print("Abort: %s" % e)


def subcmd_ios_sa(args):
    try:
        bugid = args.bugid
        sa_image = sa_image_map[args.product]
        vshell("static_iosbranch -saimages=%s -bugid=%s" % (sa_image, bugid))
    except Exception as e:
        print("Abort: %s" % e)


def subcmd_s2c(args):
    # unlink binos root if ios only
    if args.ios_only:
        shell("mv env.cs env.cs~", "../../.VDEROOT")

    try:
        vshell("cc_fix_copyright -c -l -ni")
        vshell("s2s submit -p %s -y %s" % (args.branch, args.bugid))
    except Exception as e:
        print("Abort: %s" % e)

    # link binos root back
    if args.ios_only:
        shell("mv env.cs~ env.cs", "../../.VDEROOT")


def subcmd_conv_trace(args):
    print(convert_ng_trace_string(args.trace, not(args.no_add)))


def subcmd_rsym(args):
    file = symbol_map[args.symbol] if (args.symbol in symbol_map) else args.symbol

    print("Decode traceback with symbol file <%s>:" % file)

    try:
        while True:
            print("\nEnter traceback:")
            trace = convert_ng_trace_string(raw_input(), not(args.no_add))

            if trace == "":
                print("Invalid traceback.")
                continue

            print("Decoding traceback...")
            shell("echo \"%s\" | " % trace
                  + vtn + "rsym " + file)
    except:
        return


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Sub commands")

    # start_task
    start_task_parser = subparsers.add_parser("start_task",
                                              help="Pull views and build with mail notification")
    start_task_parser.set_defaults(func=subcmd_start_task)
    start_task_parser.add_argument("-b", "--branch", required=True,
                                   choices=sorted(branch_map.keys()),
                                   help="Branch name")
    start_task_parser.add_argument("-p", "--product", default="UNKNOWN",
                                   choices=sorted(product_map.keys()),
                                   help="Product name for pre-build")
    start_task_parser.add_argument("-l", "--label", default="LATEST",
                                   help="Label name. \
                                         Use AUTO to query most recent green label automatically. \
                                         Default is LATEST.")
    start_task_parser.add_argument("-ct", "--clone_task", default="",
                                   help="Patch the changes from specified task root dir to the new view")
    start_task_parser.add_argument("-idiff", "--ios_diff", default="",
                                   help="IOS diff file which will be patched to the new view")
    start_task_parser.add_argument("-bdiff", "--binos_diff", default="",
                                   help="BinOS diff file which will be patched to the new view")
    start_task_parser.add_argument("-cs", "--codeserver", required=True,
                                   help="Code server")
    start_task_parser.add_argument("-pwd", "--token_pwd", default="",
                                   help="SofToken password for creating Abraxas Ticket")
    start_task_parser.add_argument("name",
                                   help="Task name")

    # remove_task
    remove_task_parser = subparsers.add_parser("remove_task",
                                               help="Remove views pulled by this tool, \
                                                     run it under task root directory")
    remove_task_parser.set_defaults(func=subcmd_remove_task)

    # diff_task
    diff_task_parser = subparsers.add_parser("diff_task",
                                             help="Collect diff from views pulled by this tool, \
                                                   run it under task root directory")
    diff_task_parser.set_defaults(func=subcmd_diff_task)

    # acme_patch
    acme_patch_parser = subparsers.add_parser("acme_patch", help="ACME patch")
    acme_patch_parser.set_defaults(func=subcmd_acme_patch)
    acme_patch_parser.add_argument("-r", "--reverse", action="store_true",
                                   help="Backout patch")
    acme_patch_parser.add_argument("file", help="Patch file")

    # cc_patch
    cc_patch_parser = subparsers.add_parser("cc_patch", help="CC patch")
    cc_patch_parser.set_defaults(func=subcmd_cc_patch)
    cc_patch_parser.add_argument("-r", "--reverse", action="store_true",
                                 help="Backout patch")
    cc_patch_parser.add_argument("file", help="Patch file")

    # acme_sa
    acme_sa_parser = subparsers.add_parser("acme_sa", help="ACME SA")
    acme_sa_parser.set_defaults(func=subcmd_acme_sa)
    acme_sa_parser.add_argument("bugid", help="DDTS ID")

    # ios_sa
    ios_sa_parser = subparsers.add_parser("ios_sa", help="IOS SA")
    ios_sa_parser.set_defaults(func=subcmd_ios_sa)
    ios_sa_parser.add_argument("product",
                               choices=sorted(sa_image_map.keys()),
                               help="Product name to perform SA, could be {%s}")
    ios_sa_parser.add_argument("bugid", help="DDTS ID")

    # s2c
    s2c_parser = subparsers.add_parser("s2c", help="Submit to commit (S2C), run under ios/sys")
    s2c_parser.set_defaults(func=subcmd_s2c)
    s2c_parser.add_argument("-i", "--ios_only", action="store_true",
                            help="Only submit IOS changes")
    s2c_parser.add_argument("branch",
                            choices=["mcp_dev", "xe315_throttle", "xe316_throttle"],
                            help="Branch name to perform S2C")
    s2c_parser.add_argument("bugid", help="DDTS ID")

    # get_labels
    get_labels_parser = subparsers.add_parser("get_labels",
                                              help="List green labels for branch")
    get_labels_parser.set_defaults(func=subcmd_get_labels)
    get_labels_parser.add_argument("branch",
                                   choices=sorted(branch_map.keys()),
                                   help="Branch name")

    # conv_trace
    conv_trace_parser = subparsers.add_parser("conv_trace",
                                              help="Convert NG traceback string")
    conv_trace_parser.set_defaults(func=subcmd_conv_trace)

    conv_trace_parser.add_argument("-n", "--no_add", action="store_true",
                                   help="Don't add base with offset (normally for SUP decode)")
    conv_trace_parser.add_argument("trace", help="NG Traceback string")

    # rsym
    rsym_parser = subparsers.add_parser("rsym", help="Decode NG traceback string with rsym")
    rsym_parser.set_defaults(func=subcmd_rsym)
    rsym_parser.add_argument("-n", "--no_add", action="store_true",
                             help="Don't add base with offset (normally for SUP decode)")
    rsym_parser.add_argument("symbol",
                             help="IOS symbol file to decode, or use alias {%s}"
                             % ",".join(sorted(symbol_map.keys())))

    # build
    build_parser = subparsers.add_parser("build", help="Build product with mail notification")
    build_parser.set_defaults(func=subcmd_build)
    build_parser.add_argument("product",
                              choices=sorted(product_map.keys()),
                              help="Product name to build, could be {%s}"
                              % ",".join(sorted(symbol_map.keys())))

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
