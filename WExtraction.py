
# By: LawlietJH
# WExtraction v1.0.0
# python 3.8

import requests
import json
import bs4

def addTextOutline(chars, colsLen):
	out_str = chars[0]
	for i, x in enumerate(colsLen):
		out_str += chars[1]*x
		if not i == len(colsLen)-1:
			out_str += chars[2]
	out_str += chars[3]
	return out_str + '\n'

def addText(chars, row, colsLen):
	out_str = chars[0]
	for num_c, (col, colLen) in enumerate(zip(row, colsLen)):
		words = col.split('\n')
		for i, word in enumerate(words):
			add = ''
			txt = ''
			if num_c > 0 and len(words) > 1 and i > 0:
				for c in range(num_c):
					add += chars[0]
					add += ' '*(colsLen[c])
					add += chars[1]
				txt += f'\n{add}'	
				out_str += chars[2]
			txt += word.center(colLen)
			out_str += txt
		if not num_c == len(colsLen)-1:
			out_str += chars[1]
	out_str += chars[2]
	return out_str + '\n'

def getTexts(PATH):
	
	if not PATH: return 'Path Error'
	
	# Ejemplo: https://systemmanager.ru/win2k_regestry.en/index.html?page=93504.htm
	URL = f'https://systemmanager.ru/win2k_regestry.en/{PATH}.htm'
	user_agent = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
	
	req = requests.get(URL, headers=user_agent, verify=True, timeout=10)
	
	if req.status_code == 200:
		
		body = bs4.BeautifulSoup(req.text, 'html.parser').body
		
		max_qty_p = 100
		max_qty = 70
		out_str = ''
		
		for elem in body:
			
			if elem == '\n': continue
			
			if str(elem)[1:].startswith(('h','p','table')):
				
				if str(elem)[1:].startswith('table'):
					
					rows = elem.find_all('tr')
					texts = [[] for _ in range(len(rows))]
					colsLen = []
					
					for num_r, row in enumerate(rows):
						
						colsLenPos = 0
						
						for col in row:
							
							if col == '\n': continue
							
							if colsLen[colsLenPos:colsLenPos+1] == []:
								colsLen.append(0)
							
							text = col.text
							text = text.replace('\r\n',' ')
							text = text.strip()
							
							tmp  = text
							words = []
							qty  = max_qty
							
							while tmp[qty:]:
								if not tmp[qty:qty+1] == ' ':
									qty+=1
								else:
									val = tmp[:qty].strip()
									words.append(val)
									tmp = tmp[qty:]
									qty = max_qty
							
							if words:
								for word in words:
									if colsLen[colsLenPos] < len(word):
										colsLen[colsLenPos] = len(word)
								text  = '\n'.join(words)
								text += '\n' + tmp.strip()
							else:
								if colsLen[colsLenPos] < len(text):
									colsLen[colsLenPos] = len(text)
							
							texts[num_r].append(text)
							colsLenPos += 1
							
							# ~ print(text)
					
					outline1 = ['┌─','─','─┬─','─┐']
					outline2 = ['│ ',    ' │ ',' │']
					outline3 = ['├─','─','─┼─','─┤']
					outline4 = ['└─','─','─┴─','─┘']
					
					out_str += addTextOutline(outline1, colsLen)
					for num_r, row in enumerate(texts):
						out_str += addText(outline2, row, colsLen)
						if not num_r == len(texts)-1:
							out_str += addTextOutline(outline3, colsLen)
					out_str += addTextOutline(outline4, colsLen)
					out_str += '\n'
					
				elif str(elem)[1:].startswith('h'):
					text = elem.text
					text = text.replace('\r\n','')
					text = text.strip()
					if str(elem)[1:].startswith('h1'):
						text = ' '+text+' '
						out_str += ('='*len(text)).center(112) + '\n'
						out_str += text.center(112, '=') + '\n'
						out_str += ('='*len(text)).center(112) + '\n\n'
					else:
						out_str += text + ':\n\n'
					
				elif elem.text.strip() in ['Tip','Related Entries']:
					text = elem.text.strip()
					out_str += text + ':\n\n'
				
				else:
					text = elem.text
					if text == '\n': continue
					text = text.replace('\r\n',' ')
					text = text.strip()
					
					tmp  = text
					words = []
					qty  = max_qty_p
					
					while tmp[qty:]:
						if not tmp[qty:qty+1] == ' ':
							qty+=1
						else:
							val = tmp[:qty].strip()
							words.append(val)
							tmp = tmp[qty:]
							qty = max_qty_p
					
					if words:
						text  = '\n '.join(words)
						text += '\n ' + tmp.strip()
					
					out_str += ' ' + text + '\n\n'
		
		return out_str

def getValueNames(keys):
	try:
		keys = keys.split('/') if '/' in keys else keys.split('\\')
		mainpath = keys.pop(0)
		output = paths[mainpath]
		
		if output.__class__.__name__ in ['list','tuple']:
			if len(keys) == 0:
				return {'': output[0], **output[1]}
			else:
				output = output[1]
		
		for pos, path in enumerate(keys):
			output = output[path]
			if output.__class__.__name__ in ['list','tuple']:
				if pos == len(keys)-1:
					return {'': output[0], **output[1]}
				else:
					output = output[1]
	except:
		return f'Path Error {keys}'

def saveData(path, valueName, value, filename):
	
	with open(f'{filename}.txt', 'a', encoding='utf-8') as _file:
		
		if value.__class__.__name__ in ['list','tuple']:
			text = getTexts(value[0])
		else:
			text = getTexts(value)
		
		_file.write('\n')
		_file.write(text)
		_file.write('\\'*114 + '\n')
		_file.write( '|'*115 + '\n')
		_file.write( '/'*114 + '\n')
		
		with open(f'{filename}.txt:info', 'a', encoding='utf-8') as hidden_file:	
			
			if value.__class__.__name__ in ['list','tuple']:
				output = f' {path}\\{valueName}'
			else:
				if not valueName:
					output = f' {path}'
				else:
					output = f' {path}: {valueName}'
			
			print(f'[+]{output}')
			
			hidden_file.write(output+'\n')
			hidden_file.close()
		
		_file.close()

def saveTxt(path, filename='Win2k Registry'):
	
	values = getValueNames(path)
	data = []
	
	try:
		with open(f'{filename}.txt:info', 'r', encoding='utf-8') as hidden_file:
			data = hidden_file.readlines()[4:]
			hidden_file.close()
	except:
		with open(f'{filename}.txt:info', 'w', encoding='utf-8') as hidden_file:
			hidden_file.write('\n By: LawlietJH\n WExtraction v1.0.0\n\n')
			hidden_file.close()
	
	for valueName, value in values.items():
		
		xD = False
		for dat in data:
			if value.__class__.__name__ in ['list','tuple']:
				if f' {path}\\{valueName}' in dat:
					print(f'[+] {path}\\{valueName} (Ignored)')
					xD = True
			else:
				if not valueName:
					if f' {path}' in dat:
						print(f'[+] {path} (Ignored)')
						xD = True
				else:
					if f' {path}: {valueName}' in dat:
						print(f'[+] {path}: {valueName} (Ignored)')
						xD = True
		if xD: continue
		
		saveData(path, valueName, value, filename)

def getListOfPaths(paths, path=''):
	out = []
	for key, val in paths.items():
		if val.__class__.__name__ in ['list','tuple']:
			out.append(path+key)
			out.extend(getListOfPaths(val[1], path+key+'\\'))
	return out

# ~ def getOnlyNums(data):
	# ~ for key, val in data.items():
		# ~ if val.__class__.__name__ in ['list','tuple']:
			# ~ data[key] = val[0]
	# ~ return data


# ~ ┌───┬───┐   ╔═══╦═══╗   ▄▄▄▄▄▄▄▄▄
# ~ │   │   │   ║   ║   ║   █   █   █
# ~ ├───┼───┤   ╠═══╬═══╣   █■■■█■■■█
# ~ │   │   │   ║   ║   ║   █   █   █
# ~ └───┴───┘   ╚═══╩═══╝   ▀▀▀▀▀▀▀▀▀

paths = {
	'HKCU': [51211, {
		'Software': [34802, {
			'Microsoft': [34854, {
				'Windows': [35926, {
					'CurrentVersion': [35927, {
						'Explorer': [36027, {
							'Advanced': [36032, {
								'IntelliMenus': 91640
							}],
							'DesktopProcess': 58864,
							'Shell Folders': [36173, {}],
							'Shutdown Setting': 36031,
							'Tips': [36173, {
								'Show': 68410
							}],
							'User Shell Folders': [36173, {
								'AppData':    36277,
								'Desktop':    36280,
								'Favorites':  36281,
								'NetHood':    36283,
								'Personal':   36284,
								'PrintHood':  36285,
								'Programs':   36286,
								'Recent':     36287,
								'SendTo':     36288,
								'Start Menu': 36289,
								'Startup':    36290
							}],
						}],
						'Policies': [36624, {
							'ActiveDesktop': [93204, {
								'AdminComponent': [95619, {
									'Add':    93215,
									'Delete': 93216
								}],
								'NoAddingComponents':   93217,
								'NoChangingWallPaper':  93252,
								'NoClosingComponents':  93218,
								'NoComponents':         93219,
								'NoDeletingComponents': 93220,
								'NoEditingComponents':  93221,
								'NoHTMLWallPaper':      93225
							}],
							'Comdlg32': [93579, {
								'NoBackButton': 93786,
								'NoFileMru':    93570,
								'NoPlacesBar':  93813
							}],
							'Explorer': [36625, {
								'ClassicShell':               93507,
								'ClearRecentDocsOnExit':      93171,
								'DisableLocalMachineRun':     93576,
								'DisableLocalMachineRunOnce': 93586,
								'DisablePersonalDirChange':   93206,
								'DisallowCpl':                93228,
								'DisallowRun':                93501,
								'EnforceShellExtensionSecurity': 93544,
								'ForceActiveDesktopOn':       93205,
								'ForceStartMenuLogOff':       92883,
								'GreyMSIAds':                 93177,
								'Intellimenus':               93172,
								'LinkResolveIgnoreLinkInfo':  93545,
								'MaxRecentDocs':              93785,
								'MemCheckBoxInRunDlg':        93174,
								'NoActiveDesktop':            93207,
								'NoActiveDesktopChanges':     93208,
								'NoAddPrinter':               93261,
								'NoChangeAnimation':          93787,
								'NoChangeKeyboardNavigationIndicators': 93788,
								'NoChangeStartMenu':          92885,
								'NoClose':                    58867,
								'NoCloseDragDropBands':       93209,
								'NoCommonGroups':             58868,
								'NoComputersNearMe':          93574,
								'NoControlPanel':             93226,
								'NoDeletePrinter':            93260,
								'NoDesktop':                  58869,
								'NoDFSTab':                   93811,
								'NoDriveAutoRun':             58866,
								'NoDrives':                   58871,
								'NoDriveTypeAutoRun':         93502,
								'NoFavoritesMenu':            92855,
								'NoFileAssociate':            94218,
								'NoFileMenu':                 93517,
								'NoFind':                     58873,
								'NoFolderOptions':            93518,
								'NoHardwareTab':              93571,
								'NoInstrumentation':          93173,
								'NoInternetIcon':             93210,
								'NoLogoff':                   93519,
								'NoManageMyComputerVerb':     93572,
								'NoMovingBands':              93211,
								'NoNetConnectDisconnect':     93520,
								'NoNetHood':                  58875,
								'NoNetworkConnections':       92854,
								'NoRecentDocsHistory':        93170,
								'NoRecentDocsMenu':           92853,
								'NoRecentDocsNetHood':        93212,
								'NoResolveSearch':            93175,
								'NoResolveTrack':             93176,
								'NoRun':                      58876,
								'NoRunasInstallPrompt':       93546,
								'NoSaveSettings':             93213,
								'NoSetFolders':               58878,
								'NoSetTaskbar':               58879,
								'NoShellSearchButton':        93789,
								'NoSMHelp':                   92876,
								'NoSMMyDocs':                 95414,
								'NoStartMenuSubFolders':      58881,
								'NoTrayContextMenu':          58882,
								'NoViewContextMenu':          93790,
								'NoViewOnDrive':              93573,
								'NoWelcomeScreen':            93487,
								'NoWindowsUpdate':            92848,
								'PromptRunasInstallNetPath':  93791,
								'RestrictCpl':                93231,
								'RestrictRun':               [93497, {}],
								'Run':                       [94239, {}],
								'StartMenuLogOff':            92884
							}],
							'Network': [ 91519,{
								'NoEntireNetwork': 93569
							}],
							'NonEnum': [ 83753,{
								'{450D8FBA-AD25-11D0-98A8-0800361B1103}': 83754
							}],
							'System': [93224, {
								'ConnectHomeDirToRoot':   93508,
								'DisableChangePassword':  93509,
								'DisableLockWorkstation': 93505,
								'DisableRegistryTools':   93466,
								'DisableTaskMgr':         93504,
								'EnableProfileQuota':     93589,
								'GroupPolicyRefreshTime': 93796,
								'GroupPolicyRefreshTimeOffset': 93797,
								'HideLegacyLogonScripts': 93513,
								'HideLogoffScripts':      93514,
								'HideLogonScripts':       93515,
								'IncludeRegInProQuota':   93592,
								'MaxProfileSize':         93591,
								'NoDispAppearancePage':   93253,
								'NoDispBackgroundPage':   93254,
								'NoDispCpl':              93827,
								'NoDispScrSavPage':       93255,
								'NoDispSettingsPage':     93256,
								'ProfileQuotaMessage':    93590,
								'RunLogonScriptSync':     93823,
								'Shell':                  93488,
								'Wallpaper':              93214,
								'WallpaperStyle':         93239,
								'WarnUser':               93593,
								'WarnUserTimeout':        93594
							}],
							'Uninstall': [93233, {
								'DefaultCategory':     93248,
								'NoAddFromCDorFloppy': 93238,
								'NoAddFromInternet':   93240,
								'NoAddFromNetwork':    93241,
								'NoAddPage':           93236,
								'NoAddRemovePrograms': 93234,
								'NoRemovePage':        93235,
								'NoServices':          93242,
								'NoSupportInfo':       93247,
								'NoWindowsSetupPage':  93237
							}]
						}]
					}]
				}],
				'Windows Help': 36643
			}]
		}]
	}]
}




# ~ path  = 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\'
# ~ path += 'Policies\\Explorer'
# ~ saveTxt(path)

listPaths = getListOfPaths(paths)
for path in listPaths:
	saveTxt(path)



















