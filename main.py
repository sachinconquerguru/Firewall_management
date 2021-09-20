#!/usr/bin/python3
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
import os
CONF ={}
console = Console()

def gprint(string):
	console.print(Text(string,style="bold green"))

def rprint(string): 
	console.print(Text(string,style="bold red"))

def fw_reload():
	print(os.popen("sudo firewall-cmd --reload").read())

def fw_get_active_zones():
	zone = os.popen("sudo firewall-cmd --get-active-zones").read()
	CONF["ZONE"] = zone.split("\n")[0]
	print(zone)

def fw_activate():
	gprint("Activating the firewall")
	os.popen("sudo systemctl start firewalld").read()

def display_fw_details():
    gprint("display after ")
    reld = os.popen("sudo firewall-cmd --reload")
    list_all = os.popen("sudo firewall-cmd --list-all --zone=home").read()
    print(list_all)

def fw_get_status():
	state = os.popen("sudo firewall-cmd --state").read()
	if state == "running\n":
		gprint("Firewall is active")
	else:
		rprint("Firewall is not active")
		fw_activate()
	fw_get_active_zones()

def get_zone_list():
	zone_lst = os.popen("sudo firewall-cmd --get-zones").read().split(" ")
	zone_lst[-1] = zone_lst[-1][:-1] 
	return zone_lst

def fw_add_port():
	port = Prompt.ask("Enter port number : ")
	proto = Prompt.ask("Enter protocol :", choices=["tcp","udp"],default="tcp")
	zone =  Prompt.ask("Enter zone :", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-port="+port+"/"+proto+" --zone="+zone+" --permanent "
	print(os.popen(cmd).read())

def fw_get_services():
	gprint("_________________________________________________________")
	gprint("Service List:")
	cmd = "sudo firewall-cmd --get-services"
	print(os.popen(cmd).read())
	gprint("_________________________________________________________")

def fw_add_services():
	fw_get_services()
	fw_get_active_zones()
	print("..................Adding Service................")
	service = Prompt.ask("Enter service name from the above list :")
	zone = Prompt.ask("Enter the zone",choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-service="+service+" --zone="+zone+" --permanent"
	print(os.popen(cmd).read())

def fw_add_sources():
	port_no = Prompt.ask("Enter the port number")
	proto = Prompt.ask("Enter the protocol",choices = ["tcp","udp"],default="tcp")
	fw_get_active_zones()
	zone = Prompt.ask("Enter the zone :",choices = get_zone_list(), default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-source-port="+port_no+"/"+proto+" --zone="+zone+" --permanent"
	print(os.popen(cmd).read())

def fw_add_rule_menu():
	gprint("\t[1]Add Port")
	gprint("\t[2]Add services")
	gprint("\t[3]Add sources")
	gprint("\t[4]Back to Main menu")

def fw_delete_port():
	port_no = Prompt.ask("Enter the port number")
	proto = Prompt.ask("Enter the protocol",choices = ["tcp","udp"],default="tcp")
	fw_get_active_zones()
	zone = Prompt.ask("Enter the zone :",choices = get_zone_list(), default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-port="+port_no+"/"+proto+" --zone="+zone+" --permanent"
	print(os.popen(cmd).read())

def fw_delete_services():
	fw_get_services()
	fw_get_active_zones()
	service = Prompt.ask("Enter service name from the above list :")
	zone = Prompt.ask("Enter the zone",choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-service="+service+" --zone="+zone+" --permanent"
	print(os.popen(cmd).read())

def fw_delete_sources():
	port_no = Prompt.ask("Enter the port number")
	proto = Prompt.ask("Enter the protocol",choices = ["tcp","udp"],default="tcp")
	fw_get_active_zones()
	zone = Prompt.ask("Enter the zone :",choices = get_zone_list(), default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-source-port="+port_no+"/"+proto+" --zone="+zone+" --permanent"
	print(os.popen(cmd).read())

def fw_add_rule():
    fw_add_rule_menu()
    ch = Prompt.ask("Enter your option : ", choices=["1", "2", "3","4"])
    if ch == "1":
        #add port
        fw_add_port()
        display_fw_details()
    elif ch == "2":
        fw_add_services()
        display_fw_details()
		#add services
    elif ch == "3":
		#add sources
        fw_add_sources()
        display_fw_details()
    elif ch == "4":
        main_menu()
    else:
        print("invalid choice")
		
def fw_delete_rules_menu():
	print("\t1.Delete Port")
	print("\t2.Delete Services")
	print("\t3.Delete Sources")
	print("\t4.Back to Main Menu")

def fw_delete_rules():
    fw_delete_rules_menu()
    ch = Prompt.ask("Enter your choice :",choices=["1","2","3","4"])
    if ch == "1":
        fw_delete_port()
        display_fw_details()
    elif ch == "2":
        fw_delete_services()
        display_fw_details()
    elif ch == "3":
        fw_delete_sources()
        display_fw_details()
    elif ch == "4":
        main_menu()
    else:
        print("Wrong choice")

def main_menu():
	print("\t1.Status of firewall")
	print("\t2.Set Rules")
	print("\t3.Delete Rules")
	print("\t4.Exit")

if __name__ == "__main__":
	while True:
		main_menu()
		ch = Prompt.ask("\tEnter your choice :",choices=["1","2","3","4"])
		if ch == "1":
			fw_get_status()
		elif ch == "2":
			fw_add_rule()
		elif ch == "3":
			fw_delete_rules()
		elif ch == "4":
			break
		else:
			console.print(Text("Wrong option! Type option again ",style="bold red"))