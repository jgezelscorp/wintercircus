# Azure AI Foundry

In this step, we'll setup AI Foundry where we will deploy and configure our models. As far as LLMs go, we're going to do something special.
<br>

We are going to deploy **model Router** which consist of 
1. **GPT-4.1**
2. **GPT-4.1 Nano**
3. **GPT-4.1 Mini**

These models will be deployed behind an API Endpoint and the router will select the most optimal model to be used.

By using Model Router, we are able to achieve a 60% cost reduction while preserving almost the same accuracy as if we would only use GPT-4.1

For Embedding, we'll deploy the ADA-2 model.

## Log-in

![](images/1_login.png)
