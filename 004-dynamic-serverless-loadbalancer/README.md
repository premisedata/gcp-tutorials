# Dynamic Serverless Loadbalancer

Google Cloud Platform (GCP) offers support for many different serverless services that include app engine, cloudrun, cloudfunctions, and api gateway. Each service has its pros and cons and often companies will host applications in multiple if not all of these services. One difficulty in managing multiple different types of services is maintaining a robust networking layer.

Our solution at Premise is to maintain one single load balancer that then routes requests to all of our individual services. The difficulty with this approach is that the singular load balancer can become quite complex and tough to maintain. To solve this problem, we leveraged Terraform's GCP serverless load balancer module combined with dynamic blocks. The result is a simple, scalable, and customizable solution to maintain a singular load balancer for any number of serverless applications.


## Written Tutorial

[Tutorial](https://austennovis.medium.com/e15751853312)

## Prerequisites 

* GCP Account
* Terraform

## Setup

Set the following local varibles in `main.tf`. 

    * "domain"
    * "project"
    * "region"
    * "env"
    * "services"

Specify your backend services in the `services` variable.

An example service could be 

```
{
      "service" : "default",
      "type" : "app_engine",
      "path" : "/default/*"
}
```


## Plan 

Test your terraform configuration by running ```terraform plan```

## Deploy 

Deploy your terraform resources by running ```terraform apply```