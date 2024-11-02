Check  balance of  selectel accounts and receive notifications in the telegram


### Install

```
git clone https://github.com/DorofD/selectel_balance_checker && cd selectel_balance_checker
cp conf.example.json conf.json
```
Set your environment variables in conf.json
```
docker build -t selectel_balance_checker .
docker run -v ./conf.json:/app/conf.json selectel_balance_checker
```
