# Building a sample workload

To test our simpler path to build and expose a service we'll use the following commands to achieve:

- 5 pods running the game 2048 in a webpage
- 1 service
- 1 load balancer (= Classic AWS ELB)


Create the components in the EKS cluster
```
$ kubectl apply -f cloudformation/apps/sample-app/sample-service.yaml
```
Get the data from the service running
```
$ kubectl get services service-2048 -n data-apps
```
Checking the URL of the ELB
```
$ curl http://<EXTERNAL-IP>:80
```

Now you should be able to access using your browser http://<EXTERNAL-IP>. Example: http://a814fb2687370428fac40a146d3e8848-1420776689.us-east-1.elb.amazonaws.com/

[![2048.png](2048.png)](2048.png)

Run the following commands to drop the components created above:
```
$ kubectl delete -f cloudformation/apps/sample-app/sample-service.yaml
```