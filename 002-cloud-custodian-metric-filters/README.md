# Cloud Custodian Metric Filters

## Written Tutorial

Tutorial - coming soon

## Setting Up Cloud Custodian 


Cloud Custodian is a Python application and supports Python 3 on Linux, MacOS and Windows.

To install run the following commands: 

`pip install c7n`
`pip install c7n_gcp`

To run cloud custodian you will also need to be authenticated to GCP. If you are not already authenticated you will first need to install gcloud.(the GCP Command Line Interface).

Then run the following command:

`gcloud auth application-default login`
 
Executing the command will open a browser window with prompts to finish configuring your credentials. For more information on this command, view its documentation.
 
## Running Cloud Custodian 

Cloud Custodian uses policies to interact with cloud resources. A policy is simply a YAML file that follows a predetermined schema to describe what you want Custodian to do.
There are three main components to a policy:

* Resource: the type of resource to run the policy against

* Filters: criteria to produce a specific subset of resources

* Actions: directives to take on the filtered set of resources

The example below illustrates a policy that filters for compute engine resources named test, and then performs the “stop” action on each resource that matches that filter.

```yaml
policies:
  - name: my-first-policy
    description: |
      Stops all compute instances that are named "test"
    resource: gcp.instance
    filters:
      - type: value
        key: name
        value: test
    actions:
      - type: stop
```
 
To execute this policy in your project you would simply execute the following command, where custodian.yml is the file that contains your project. 

`GOOGLE_CLOUD_PROJECT="project-id" custodian run --output-dir=. custodian.yml` 

Adding the flag `--dryrun` is useful since it ensures that the actions will not be run, so you can see what resources would be affected by the policy before executing any destructive actions.

## Using Metric Filter Policies

To run any of the included metric policies you would use the following command, while `project-id` is the project you woudld to run the policy aganst and POLICY.yml should be the name of the corresponding policy you would like to run. 

`GOOGLE_CLOUD_PROJECT="project-id" custodian run --output-dir=. POLICY.yml --dryrun` 

Remove the `--dryrun` flag if you are comfortable triggering the actions. 
