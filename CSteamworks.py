#!/usr/bin/env python
#  Created by Riley Labrecque for Shorebound Studios
#  This script probably requires Python 3.3+
#  This script is licensed under the MIT License
#  See the included LICENSE.txt or the following for more info
#  http://www.tldrlegal.com/license/mit-license

from __future__ import print_function

import os

CPP_HEADER = """
// This file is automatically generated!

#include "CSteamworks.h"
"""[1:]

g_files = [f for f in os.listdir('steam') if os.path.isfile(os.path.join('steam', f))]

# We don't currently support the following interfaces because they don't provide a factory of their own.
# You are expected to call GetISteamGeneric to get them. That's a little too much for this script at this point.
# They are extremely small and rarely used interfaces, It might just be better to do it manually for them.
if 'isteamappticket.h' in g_files:
    g_files.remove('isteamappticket.h')
if 'isteamgamecoordinator.h' in g_files:
    g_files.remove('isteamgamecoordinator.h')
if 'isteamps3overlayrenderer.h' in g_files:
    g_files.remove('isteamps3overlayrenderer.h')

# We don't currently support SteamVR
if 'steamvr.h' in g_files:
    g_files.remove('steamvr.h')

g_files.extend(['isteamgameserverutils.h', 'isteamgameservernetworking.h', 'isteamgameserverhttp.h'])

g_GameServerFilenameDict = {
    'isteamgameserverutils.h': 'isteamutils.h',
    'isteamgameservernetworking.h': 'isteamnetworking.h',
    'isteamgameserverhttp.h': 'isteamhttp.h',
}

g_GameServerIFaceDict = {
    'isteamgameserverutils.h': 'ISteamGameServerUtils',
    'isteamgameservernetworking.h': 'ISteamGameServerNetworking',
    'isteamgameserverhttp.h': 'ISteamGameServerHTTP',
}

try:
    os.makedirs('wrapper/')
except OSError:
    pass

g_methodnames = []

for filename in g_files:
    try:
        emulatedfilename = g_GameServerFilenameDict[filename]
    except KeyError:
        emulatedfilename = filename

    print('Opening: "' + filename + '"')
    with open('steam/' + emulatedfilename, 'r') as f:
        output = []
        depth = 0
        iface = None
        ifacedepth = 0
        bInMultiLineCommentDepth = False
        bDisableCode = False
        for linenum, line in enumerate(f):
            linenum += 1
            bMultiLineCommentCodeOnThisLine = False

            line = line.split('//', 1)[0].strip()
            if len(line) == 0:
                continue

            pos = line.find('/*')
            if pos != -1:
                bInMultiLineCommentDepth = True
                endpos = line.find('*/')
                if endpos != -1:
                    bInMultiLineCommentDepth = False
                else:
                    line = line.split('/*', 1)[0].strip()
                    if len(line) == 0:
                        continue
                    else:
                        bMultiLineCommentCodeOnThisLine = True

            pos = line.find('*/')
            if pos != -1:
                bInMultiLineCommentDepth = False

                line = line[pos + len('*/'):].strip()
                if len(line) == 0:
                    continue

            if bInMultiLineCommentDepth and not bMultiLineCommentCodeOnThisLine:
                continue

            pos = line.find('class ISteam')
            if pos != -1:
                if ';' in line:
                    continue
                elif 'Response' in line:  # We don't have a proper way to call responses yet
                    continue
                
                iface = line[pos + len('class '):].split()[0]
                ifacedepth = depth
                try:
                    iface = g_GameServerIFaceDict[filename]
                except KeyError:
                    pass
                print(iface)

            if iface:
                if line.startswith('#'):
                    output.append(line.strip() + '')
                elif 'virtual' in line and line.endswith('0;'):
                    splitline = line[len('virtual '):].split()
                    state = 0
                    returnvalue = ''
                    methodname = ''
                    realmethodname = ''
                    args = ''
                    for token in splitline:
                        if not token:
                            continue

                        if state == 0:  # Return Value
                            if token.startswith('*'):
                                returnvalue += '*'
                                state = 1
                            elif token.find('(') == -1:
                                returnvalue += token + ' '
                            else:
                                state = 1

                        if state == 1:  # Method Name
                            if token.startswith('*'):
                                token = token[1:]
                            realmethodname = token.split('(', 1)[0]
                            methodname = iface + '_' + realmethodname

                            if methodname in g_methodnames:
                                methodname += '_'
                            g_methodnames.append(methodname)

                            if token[-1] == ')':
                                state = 3
                            elif token[-1] != '(':  # Edge case like f(void arg) - shouldn't be triggered
                                print("[WARNING] A function doesn't have whitespace between the backets.")
                                token = token.split('(')[1]
                                state = 2
                            else:
                                state = 2
                                continue

                        if state == 2:  # Args
                            if token.startswith(')'):
                                state = 3
                            elif token.endswith(')'):  # Edge case like f(void arg) - shouldn't be triggered
                                print("[WARNING] A function doesn't have whitespace between the backets.")
                                args += token[:-1]
                                state = 3
                            else:
                                args += token + ' '

                        if state == 3:  # ) = 0;
                            continue

                    args = args.rstrip()
                    typelessargs = ''
                    if args != '':
                        argssplitted = args.strip().split(' ')
                        for i, token in enumerate(argssplitted):
                            if token == '=' or token == '""':  # Handle defaulted arguments
                                continue
                            if token == '0':  # Like f( int nChannel = 0 )
                                token = argssplitted[i - 2]

                            if token.startswith('**'):
                                typelessargs += token[2:] + ' '
                            elif token.startswith('*'):
                                typelessargs += token[1:] + ' '
                            elif token[-1] == ',':
                                typelessargs += token + ' '
                            elif i == len(argssplitted) - 1:
                                typelessargs += token
                    typelessargs = typelessargs.rstrip()

                    bReturnsCSteamID = False
                    if returnvalue.strip() == 'CSteamID':  # Can not return a class with C ABI
                        bReturnsCSteamID = True
                        returnvalue = 'SteamID_t '  # See CPP_HEADER for more details

                    output.append('SB_API ' + returnvalue + 'S_CALLTYPE ' + methodname + '(' + args + ') {')
                    if bReturnsCSteamID:
                        output.append('\treturn ' + iface[1:] + '()->' + realmethodname + '(' + typelessargs + ').ConvertToUint64();')
                    else:
                        output.append('\treturn ' + iface[1:] + '()->' + realmethodname + '(' + typelessargs + ');')
                    output.append('}')
                    output.append('')

            if '{' in line:
                depth += 1
            if '}' in line:
                depth -= 1
                if iface and depth == ifacedepth:
                    iface = None
                if bDisableCode:
                    output.append('#endif')
                    bDisableCode = False

        if output:
            with open('wrapper/' + os.path.splitext(filename)[0] + '.cpp', 'w') as out:
                print(CPP_HEADER, file=out)
                for line in output:
                    print(line, file=out)
