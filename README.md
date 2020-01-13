[![Build Status](https://dev.azure.com/sjwilczynski/GithubRepos/_apis/build/status/sjwilczynski.xkom-bot?branchName=master)](https://dev.azure.com/sjwilczynski/GithubRepos/_build/latest?definitionId=1&branchName=master)
# xkom-bot

A simple Python script that informs me by SMS about new _hot shot_ discounts available at [X-KOM](https://www.x-kom.pl) store.

Deployed to [Azure functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python) using [Timer trigger](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer) so that I know about all the interesting deals.

To deploy function to Azure use: 
```bash
func azure functionapp publish xkom-hot-shot -i --build remote
```
If you also want to publish `local.settings.json` (containing environment variables) use:
```
func azure functionapp publish xkom-hot-shot --publish-local-settings -i --build remote
```

[Here](https://www.scalyr.com/blog/azure-functions-in-python-a-simple-introduction/) you can find how to test your function locally.