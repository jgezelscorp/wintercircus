# Exposing MCP through APIM and APIC : Secure API and MCP handling - pt 1

> **🚨 IMPORTANT PREVIEW NOTICE**  
> MCP support in Azure API Management is currently in **PREVIEW**. To access MCP features, you **MUST**:
> 1. Enable the **"AI Gateway Early"** update group on your APIM instance
> 2. Use the special preview portal URL: `https://portal.azure.com/?Microsoft_Azure_ApiManagement=mcp`
> 3. Wait up to 2 hours after enabling the update group
> 
> **Without these steps, MCP options will NOT be visible in the Azure portal!**

## MCP and the API Management / GenAI Gateway

APIM aka API Management Service can now be used as GenAI Gateway in order to foresee safe and controlled access to your AI endpoints. 
Some of the features it has:
- Throtling of your tokens
- Semantic caching of your results
- MCP endpoint exposure
- Authentication handling
- exposing your AI Foundry and Azure OpenAI models and API's

![GA for GenAI Gateway](.\assets\genaigw.png)

![MCP featues in APIM and APIC](.\assets\mcpexpo.png)

## Exercise
### Pre-requisite for this exercise
Create an Application Insights resource , follow the guide here if needed [Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/create-workspace-resource?tabs=portal)

### Create an API Management services instance capable of MCP

**1.** Log in to https://portal.azure.com
**2.** in the search bar type "API man", this will give you below results: ![API Services](.\assets\apim-search.png) Select **API Managment services**. This will open up the API Management services blade and page.
**3.** Click "Create"
</br>![Click Create](.\assets\apim-clickcreate.png)

**4.** In the create screen fill out all the details **BUT** make sure that you select a **V1** SKU (take a Basic or Standard if you please). This is important for the remainder of the exercise
![API Needed SKU's](.\assets\apim-createsku.png)
    <details>
        <summary><strong>Note</strong></summary>
        <i>
            Currently only V1 support the exposure and creation of MCP servers and the implementation of the MCP Registry
            V2 SKUs will support these features in future releases.
        </i>
    </details>
For the rest of the *Basics* tab fill out as needed
![Basics tab](.\assets\apim-wizard-03-basics-tab.png)

   - **Subscription**: Select your Azure subscription
   - **Resource Group**: Choose an existing resource group or create a new one
   - **Region**: Select the region closest to your users or where your other resources are located
   - **Resource name**: Enter a unique name for your APIM service (this will be part of your gateway URL)
   - **Organization name**: Enter your organization name
   - **Administrator email**: Provide an email address for administrative notifications

Click **"Next"** to continue.

**5.** In the *Monitor + secure* tab make sure you enable a log analytics workspace and enable "Log Analytics (Enhanced monitoring and insights into your APIs)" and "Application Insights" and select there the resources created during the pre-reqs creation (see prereqs and guide above).
![Monitor tab](.\assets\apim-wizard-05-monitor-secure-tab.png)

   - **Enable Log Analytics**: ✅ Check this option
   - **Log Analytics workspace**: Select the workspace created in prerequisites
   - **Enable Application Insights**: ✅ Check this option
   - **Application Insights resource**: Select the Application Insights resource created in prerequisites
   - **Sampling rate**: Leave at default (100%) for comprehensive monitoring
 Click **"Next"** to continue.

**6.** On the "Virtual Network" tab just leave all the defaults and click **"Next"** to continue.
![Network tab](.\assets\apim-wizard-06-networking-tab.png)

**7.** Enable the <i>Managed Identity</i> check box and now click **"Review + Create"** to validate the deployment.
![Identity tab](.\assets\apim-wizard-07-identity-tab.png)

**8.** If all is filled out correctly and complete the **"Create"** button will be enabled (after ARM validation), if not you will see the screen below, then you need to recheck everything to make sure all is filledout correctly.  
![Validation tab](.\assets\apim-wizard-09-review-create.png)

If the **"Create"** button is enabled (blue) then click it and the deployment will start. 
<details>
    <summary><strong>Deployment Timeline</strong></summary>
    <i>
        APIM deployment typically takes 30-60 minutes depending on the SKU selected. Premium SKUs may take longer due to additional features being provisioned.
    </i>
</details>

### Enabling the MCP capabilities on APIM
**9.** Once the deployment has finished you will see your newly created instance apearing in the list of **API Management services** (see step 2 if you forgot how to get there)
![APIM Listing](.\assets\apimlisting.png) 
Click on the APIM instance name to open up the APIM Blade and overview.

**10.** In the left menu, select **Deployment + infrastructure > Service** update settings.
![Service updates](.\assets\Serviceupdate.png)

**11.** Under Update group, review the current setting and select Edit to change it to *AI Gateway Early*.
 Click **"Save"** to enable.
![alt text](.\assets\updategroup.png)

> **🚨 HEADS UP**  
> Now you need to wait up to 2 hours after enabling the update group, to get the MCP side of things working correctly. Hence why we do this as pre-req to not hold you back from the other exercises.
> Continue with the other exercises for now.
> **Without these steps, MCP options will NOT be accessible in the Azure portal!**

## 📋 Quick Reference Checklist

Use this checklist to ensure you've completed all critical steps:

- [ ] ✅ **SKU Selection**: Selected V1 SKU (Basic, Standard, or Premium)
- [ ] ✅ **Deployment**: APIM instance successfully deployed
- [ ] ✅ **Update Group**: Enabled "AI Gateway Early" in Settings > Service updates
- [ ] ⏰ **Wait Time**: Waited up to 2 hours after enabling update group
- [ ] 🔗 **Preview URL**: Used `https://portal.azure.com/?Microsoft_Azure_ApiManagement=mcp`
- [ ] 👀 **MCP Visible**: Can see "MCP Servers" option in APIs menu
- [ ] 🚀 **MCP Created**: Successfully created at least one MCP server
- [ ] ✅ **Testing**: Tested MCP functionality with a client

**🚨 If MCP options are not visible**: Double-check the preview URL and update group settings!

**Congratulations!** You now have a fully functional Azure API Management service with MCP support ready for your AI workloads. The service provides secure, scalable access to your AI endpoints with advanced features like token throttling, semantic caching, and comprehensive monitoring.