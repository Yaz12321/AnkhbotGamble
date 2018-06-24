#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr, sys, json, os, codecs
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import random

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "Gamble"
Website = "https://www.AnkhBot.com"
Creator = "Yaz12321"
Version = "1.0"
Description = "Gamle some points, lose them all, get some points back, or double them points."

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
#   Version Information
#---------------------------------------

# Version:
# > 1.0 <
    # First Release

class Settings:
    # Tries to load settings from file if given 
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig') 
        else: #set variables if no settings file
            self.OnlyLive = False
            self.Command = "!gamble"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.UseCD = True
            self.Cooldown = 0
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.BaseResponse = "{0} just gambled {2} {3}! {0} managed to get {1} {3} back, and now has {4} {3} in total!"
            self.NotEnoughResponse = "{0} you don't have that amount to gamble."
            selt.ratio = "WinLose"
            self.loseall = "LUL {0} has lost every single {3} in gambling!"
            self.Win = "FeelsGoodMan"
            self.Loss = "FeelsBadMan"
            self.Back = "Kappa"
            self.MaxWin = 2
            
            
    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    # Globals
    global MySettings

    # Load in saved settings
    MySettings = Settings(settingsFile)

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return

def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == MySettings.Command:
       
        #check if command is in "live only mode"
        if MySettings.OnlyLive:

            #set run permission
            startCheck = data.IsLive() and Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo)
            
        else: #set run permission
            startCheck = True
        
        #check if user has permission
        if startCheck and  Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo):
            
            #check if command is on cooldown
            if Parent.IsOnCooldown(ScriptName,MySettings.Command) or Parent.IsOnUserCooldown(ScriptName,MySettings.Command,data.User):
               
                #check if cooldown message is enabled
                if MySettings.UseCD: 
                    
                    #set variables for cooldown
                    cooldownDuration = Parent.GetCooldownDuration(ScriptName,MySettings.Command)
                    usercooldownDuration = Parent.GetUserCooldownDuration(ScriptName,MySettings.Command,data.User)
                    
                    #check for the longest CD!
                    if cooldownDuration > usercooldownDuration:
                    
                        #set cd remaining
                        m_CooldownRemaining = cooldownDuration
                        
                        #send cooldown message
                        Parent.SendTwitchMessage(MySettings.OnCooldown.format(data.User,m_CooldownRemaining))
                        
                        
                    else: #set cd remaining
                        m_CooldownRemaining = Parent.GetUserCooldownDuration(ScriptName,MySettings.Command,data.User)
                        
                        #send usercooldown message
                        Parent.SendTwitchMessage(MySettings.OnUserCooldown.format(data.User,m_CooldownRemaining))
            
            else: #check if user got enough points

                sbet = data.GetParam(1)
                if sbet == "all":
                    sbet = Parent.GetPoints(data.User)
                total = Parent.GetPoints(data.User)

                bet = int(sbet)
                              
                if bet <= total:
                    
                    if MySettings.ratio == "WinLose":
                        a = 2
                        b = 0.5

                    if MySettings.ratio == "WinEvenLose":
                        a = 3
                        b = 1

                    if MySettings.ratio == "RangeLoseToDouble":
                        a = MySettings.MaxWin + 1
                        b = 100
                    #remove points from the user triggering the command
                    Parent.RemovePoints(data.User, data.UserName, bet)

                        
                    #add points to all viewers in dict
                    win = int(bet*Parent.GetRandom(0,a)/b)
                    Parent.AddPoints(data.User,data.UserName, win)
                    
                    if win == bet:
                        WL = MySettings.Back
                        winnings = 0
                    if win > bet:
                        WL = MySettings.Win
                        winnings = win - bet
                    if win < bet:
                        WL = MySettings.Loss
                        winnings = bet - win
                    
                    #send successful message
                    if bet != 0 and Parent.GetPoints(data.User) == 0:
                        Parent.SendTwitchMessage(MySettings.loseall.format(data.UserName,win,bet,Parent.GetCurrencyName(),Parent.GetPoints(data.User)))
                    else:
                        Parent.SendTwitchMessage(MySettings.BaseResponse.format(data.UserName,win,bet,Parent.GetCurrencyName(),Parent.GetPoints(data.User),WL,winnings))
                    
                    # add cooldowns
                    Parent.AddUserCooldown(ScriptName,MySettings.Command,data.User,MySettings.UserCooldown)
                    Parent.AddCooldown(ScriptName,MySettings.Command,MySettings.Cooldown)
                
                else:
                    #send not enough currency response
                    Parent.SendTwitchMessage(MySettings.NotEnoughResponse.format(data.UserName,Parent.GetCurrencyName(),MySettings.Command,bet))
    return

def Tick():
    return

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return
