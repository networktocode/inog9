class: center, middle, title
.footnote-con[BUILT FOR iNOG9]
<br>

# Network Programming & Automation

<br>
<br>

Jason Edelman

CCIE 15394

jason@networktocode.com

Twitter: @jedelman8

Blog: jedelman.com

<br><br>

<img src="slides/media/Footer1.PNG" alt="Blue Logo" style="alight:middle;width:350px;height:60px;">


---
layout: true

.footer-picture[![Network to Code Logo](slides/media/Footer2.PNG)]
.footnote-left[(C) 2015 Network to Code, LLC. All Rights Reserved. ]
.footnote-con[BUILT FOR iNOG9]

---

class: middle, segue


# Why Network Automation?


# Really?



---

# Types Network Automation


- Device Compliance

- Data Collection

- Reporting

- Configuration Management

---

# Getting Started

**What are our options?**


- Native Programming 

- Open Source Tools

- Commercial Tools


**Thinks to think about:**

- Support

- Control

- Extensibility

---


class: middle, segue

### One more thing...

## Be the Automator and not the Automated


---


# Live Demos



Tonight, we will see three mini-demos:

- Automated Cable Verification of Junos vMX Devices using Ansible

- Pushing BGP configuration leveraging a basic OpenConfig BGP model to IOS-XRv with Ansible

- Quick look into RESTCONF on Cisco IOS-XE on CSR 1000V

**Take advantage of virtual network appliances**


---

class: middle, segue

# Before the Demos

## What are these terms, tech, and tools?


---

# Ansible

- Open source tool by Red Hat 
- Lowest barrier to entry for automation
  - Great for network and systems automation
  - Supports IOS, XR, Junos, Cumulus, EOS, and more _out of the box_


---

# OpenConfig 

OpenConfig Working Group (WG) - Working group developing vendor neutral data models.  Here is the sample BGP model being used in the demo:

```bash
<config>
 <bgp xmlns="http://openconfig.net/yang/bgp" nc:operation=create>
  <global>
   <config>
    <as>65512</as>
    <router-id>100.1.1.1</router-id>
   </config>
  </global>
 </bgp>
</config>
```

Unfortunately, there is only one device currently OC-BGP that is **publicly** available (IOS-XR).  Other vendors and/or platforms should support it soon.  Tonight's demo will use IOS-XRv

---

# Postman

Chrome plug-in for working with web based (HTTP) APIs, i.e. REST API

It'll be easier to see in action!


---

class: middle, segue

# Demo Time

---


---


# References

- Slides and playbooks for this presentation including the OC BGP Ansible module  :
  - [https://github.com/networktocode/inog9](https://github.com/networktocode/inog9)

- Tutorials on Network to Code - [http://networktocode.com/products/labs/tutorials/](http://networktocode.com/products/labs/tutorials/)

- Courses (Public & Private) - [http://networktocode.com/products/training/](http://networktocode.com/products/training/)

- [Network Automation Book](http://shop.oreilly.com/product/0636920042082.do) - Matt Oswalt, Scott Lowe, and Jason Edelman

- Slack Team dedicated to Network Automation - self sign up [slack.networktocode.com](slack.networktocode.com)
  - Channels include #ansible, #napalm, #netmiko, #trigger, #nsot for open source projects (just to name a few).  Vendor channels too.
  - 1000+ members and growing

- And remember, Be the Automator...not the automated







