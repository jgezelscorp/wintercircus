# Exposing MCP through APIC : API Center MCP Registry
## What is APIC or API Center?
Azure API Center enables tracking all of your APIs in a centralized location for discovery, reuse, and governance. Use an API center to develop and maintain a structured and organized inventory of your organization's APIs - regardless of their type, lifecycle stage, or deployment location - along with related information such as version details, API definition files, and common metadata.

With an API center, stakeholders throughout your organization - including API program managers, IT administrators, application developers, and API developers - can design, discover, reuse, and govern APIs.
![architecture](.\assets\APIMAPIC.png)

![Build](.\assets\apicbuild.png)



## Exercise
### Add an API Center to your APIM
**1.** Log into the Azure portal: portal.azure.com
**2.** In the Azure portal type API Center and select API center
![ Search API Center](.\assets\apic.png)
**3.** Click **"Create"**

![alt text](.\assets\apiccreate.png)

**4.** Fill out the name and resource group and region where you want to host it, and select the *"Free"* pricing plan. 
![APIC Wizard](.\assets\apicwiz.png)
Click **"Review + Create"** and if all looks good ont the validation page then immediately click **"Create"**.

**5.** Once the APIC is created it will appear in the APIC list. Select it in that list. 
![API Center List](.\assets\apiclist.png)
**6.** In the APIC blade search for "settings", this will lead to the setup of the API Center Developer Portal:
![API Center Portal Setup](.\assets\apicportalsetup.png)

**7.** CLick **"Start set up"** , this will open a wizard for setting up the API Center Portal securely with Entra ID. CLick **"Save + publish"**
![APIC Entra ID](.\assets\apicwizentra.png)

**8.** You now can open the API Center Developer Portal by clicking on the link 
![APIC Portal Ready](.\assets\apicportalenabled.png)
Keep the API Center Portal open for now:
![API Center Portal](.\assets\apicportal.png)
>**Important**
>By default, you and other administrators of the API center don't have access to APIs in the API Center portal. Be sure to assign the Azure API Center Data Reader role to yourself and other administrators.
><details><i>
>To enable sign-in, assign the Azure API Center Data Reader role to users or groups in your organization, scoped to your API center.
>
>For detailed prerequisites and steps to assign a role to users and groups, see Assign Azure roles using the Azure portal. Brief steps follow:
>
>1. In the Azure portal, navigate to your API center.
>2. In the left menu, select Access control (IAM) > + Add role assignment.
>3. In the Add role assignment pane, set the values as follows:
>4. On the Role page, search for and select Azure API Center Data Reader. Select Next.
>5. On the Members page, In Assign access to, select User, group, or service principal > + Select members.
>6. On the Select members page, search for and select the users or groups to assign the role to.
>7. Click Select and then Next.
>8. Review the role assignment, and select Review + assign.
>    </i>
></details>

now let's add it to our APIM

**9.** Open up your APIM and select Api Center from the blade and select the just now created API Center in the combobox on that page and click on the **"Synchronize APIs"** button:
![APIC Sync](.\assets\apicsync.png)

**10.** Once they are synced (can take a few seconds to a few minutes), return to the APIC Portal and do a sign in (make sure you followed the steps to allow access for your user), and if all went well you should be able to see all your APIs and MCPs and you would be able to check all definitions et all.
![APIC Portal Listings](.\assets\apicportallisting.png)

**11.** When clickin on the MCP server you can now inspect it , and immediately consume it from VS Code if wanted 
![APIC MCP](.\assets\apicmcpdetails.png)
