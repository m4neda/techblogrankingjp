Now testing!
https://techblogrank.com/

### note for me
#### poetry for VSCode
- when you want to use debugger and formatter or somthing like that via VSCode, you need to create .venv file.
```
$ poetry config --list
$ poetry config virtualenvs.in-project true
```
if you already created poetry virtualenv, Remove it then `poetry install` again.
```
$ poetry env list
poetry-xx-py3.9
$ poetry env remove poetry-xx-py3.9
```
