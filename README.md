# Rambutan
The Raspberry Pi Stack for the D.C. Policy Center
This will include
* Scheduling
* Waiau (Lake Management)
    - dc-legislation: Data pulls for the city council
* Dashboard Capabilities


## Scheduling
Scheduling is currently being managed internally to the Raspberry Pi by the Cron system.
This daemon is native to the unix system.  It may be replaced by a self-managed daemon in the
future but for now cron works well.  
### How to
On the RaspPi running the command <code>crontab -l</code> lists the current cron jobs.  Running <code>crontab -e</code>
allows the user to edit the cron jobs.  
### Current cronjobs
|Job description|frequency|Crontab command|
|-|-|-|
|Start noVNC on reboot|Every reboot|@reboot|
|Pull DC legislation|Every night at 6am|0 6|
|Auto push to git repo| Every morning at 7am| 0 7 |


-- Unknown current status, in the process of resetting everything.



