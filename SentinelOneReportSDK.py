from management.mgmtsdk_v2.mgmt import Management
from datetime import datetime

token = input("Please supply token: ")
management = Management(hostname="euce1-swprd2.sentinelone.net", api_token=token)
sites = management.sites.get(limit="25")
if sites.status_code != 200:
    print("Getting sites failed. Aborting.")
    quit()

dateTime = datetime.strftime(datetime.today(),"%d.%m.%Y_%H_%M")
reportName = "SentinelOneSiteAndDeviceReport_"
reportName+=dateTime
reportName+=".csv"
report = open(reportName,"w")

#debugIndex1 = 0
line = ""
for site in sites.data:
    if site.name == "Default site":
        continue
    
    report.write("Site,ActiveLicenses,TotalLicenses\n")
    line = site.name+","+str(site.activeLicenses)+","+str(site.totalLicenses)+"\n\n," #+" ; ID: "+site.id
    report.write(line)
    
    report.write("Host,LastLoggedInUser,AgentVersion,Infected,DiskEncryption,LastActiveDate\n")
    agents = management.agents.get(siteIds=site.id,limit="100")
    if agents.status_code != 200:
        report.write("FAILED TO GET AGENTS\n\n\n\n")
        continue
    
    #debugIndex2 = 0
    for agent in agents.data:
        #if debugIndex1==10 and debugIndex2==0:
        #   print(vars(agent))
        #    debugIndex2+=1
        line = (","+agent.computerName+","+agent.lastLoggedInUserName+","+agent.agentVersion+","
                +str(agent.infected)+","+str(agent.encryptedApplications)+","+agent.lastActiveDate+"\n"
            )
        report.write(line)
    report.write("\n\n\n\n")
    
    #debugIndex1+=1

report.close()