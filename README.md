# Python-Django-Testzone
Speedrun!

Trying to learn Python Django web engine frameworks on the go, by following the YouTube tutorials. 

* https://youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
* https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

## Development Software & Tools I'm Using
* Python 3.9.4
* PyCharm
* Sqlite3 (via Python)

## Limitations
* This GitHub repository does not consider cybersecurity measurements 
(including XSS/database query attacks)

## Bugs to be fixed
* ~~Login with a dummy account and password causes~~ `no such column: auth_user.last_login`~~ 
fixed as it seems.
* Had to modify Django `auth` model from local computer `'C:\\Python39\\lib\\site-packages\\django\\contrib\\auth\\migrations\\__init__.py'`. 
 This may not work on other computers/servers.
* Registration causes django.urls.exceptions.NoReverseMatch: Need to modify `urls.py` soon.

## To be completed
* Improve HTML/CSS appearance

## Misc.
- Also first time learning how to configure the GitHub workflow.yml