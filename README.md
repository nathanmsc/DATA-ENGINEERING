# DATA ENGINEERING

### DATA ENGINEERING TOOLS AND INFRASTRUCTURE

By leveraging Kubernetes and containerization, organizations can build a resilient, scalable, and secure infrastructure for data engineering. This setup not only enhances the efficiency of data processing and analysis but also ensures adaptability to evolving challenges, providing a robust foundation for data-driven decision-making.

---
<p>
  <img src="https://github.com/nathanmsc/DATA-ENGINEERING/blob/main/DOCKER/ZABBIX/src/img/logo.jpg" alt="Logo" width="200" style="margin-right: 20px;"/>
  <img src="https://github.com/nathanmsc/DATA-ENGINEERING/blob/main/DOCKER/ZABBIX/src/img/marca.svg" alt="Brand" width="600"/>
</p>
<div align="center">

# Rewriting the content to a markdown file for download due to the session reset.

# Markdown content for the MindsetCloud banner and services.
file_content = """
# MindsetCloud: Transforming Data into Powerful Insights 🌐

---

**Empowering Businesses with Cutting-Edge Data Engineering Solutions**

At **MindsetCloud**, we specialize in delivering innovative, scalable, and cloud-native data solutions tailored to your business needs. From Big Data processing to IoT integrations, we provide the tools and expertise to turn complex data challenges into actionable insights.

---

## **Our Services**  

### **1. Cloud-Native Data Infrastructure**
- Design and deployment of scalable infrastructures on AWS, Azure, and Google Cloud.
- Cost-optimization strategies for cloud environments.
- Kubernetes-based solutions for containerized and resilient data pipelines.

### **2. Big Data Processing**
- High-performance data processing with **Apache Spark** and **Apache Hadoop**.
- Custom ETL pipelines to handle massive datasets.
- Real-time and batch data processing tailored to your use case.

### **3. Workflow Automation & Orchestration**
- Seamless data pipeline automation using **Apache Airflow**.
- Advanced orchestration of complex workflows.
- Monitoring and maintenance of critical data operations.

### **4. IoT Data Solutions**
- Integration of IoT devices for real-time data collection.
- Stream processing and analytics for IoT-driven insights.
- Secure and efficient data management for smart systems.

### **5. DataOps & Continuous Delivery**
- Implementation of DataOps practices for enhanced collaboration.
- CI/CD pipelines for data-driven applications.
- Version control and automated testing for data workflows.

---

## **Our Expertise**  

- **Kubernetes**: Deploying containerized solutions for seamless scalability.  
- **Apache Spark & Hadoop**: Advanced analytics on massive datasets.  
- **Apache Airflow**: Automating and scheduling robust data workflows.  
- **IoT Integration**: Connecting devices for actionable insights.  
- **Cloud Computing**: Expertise in AWS, Azure, and Google Cloud ecosystems.  

---

## **Why Choose MindsetCloud?**  
✅ **Tailored Solutions:** Every service is customized to meet your business goals.  
✅ **Innovation at Scale:** Scalable architectures for small startups to global enterprises.  
✅ **Proven Expertise:** A team of seasoned professionals with deep technical knowledge.  
✅ **Reliability:** Solutions that are secure, resilient, and future-ready.

---

Let MindsetCloud transform your data into a strategic asset. 🚀  
**Contact us today:** [info@mindsetcloud.com](mailto:info@mindsetcloud.com) | Visit: [www.mindsetcloud.com](http://www.mindsetcloud.com)  
"""

file_path = "/mnt/data/MindsetCloud_Services.md"

# Save the content to a file.
with open(file_path, "w") as file:
    file.write(file_content)

file_path


</div>

---
## Table of Contents

- [Kubernetes](https://github.com/nathanmsc/DATA-ENGINEERING/blob/main/KUBERNETES/README.md)
- [Docker Containers](https://github.com/nathanmsc/DATA-ENGINEERING/tree/main/DOCKER)
- [Useful Commands](#useful-commands)
- [Network Configuration](#network-configuration)
- [Running Docker on WSL](#running-docker-on-wsl)
- [Contributing](#contributing)
- [License](#license)

---

## Useful Commands

### Git Setup

```bash
ssh-keygen -t rsa -b 4096 -C "your@email.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
clip < ~/.ssh/id_rsa.pub
# Add the key to GitHub
git pull git@github.com:username/repository.git
git config --global user.email "your@email.com"
git config --global user.name "your_name"
git push --set-upstream origin master
```

---

## Network Configuration

### Show IP Address of Interfaces

```bash
ip addr
```

### Create Macvlan Network with Docker

```bash
docker network create -d macvlan \
  --subnet=172.27.136.42/20 \
  --ip-range=172.27.142.0/24 \
  --gateway=172.27.128.1 \
  --aux-address="msc-router=172.27.142.1" \
  -o parent=eth0 msc-macvlan
```

### Link Macvlan Interface

```bash
sudo ip link add msc-macvlan link eth0 type macvlan mode bridge
sudo ip addr add 172.27.142.1/24 dev msc-macvlan
sudo ifconfig msc-macvlan up
```

### Create Bridge Network in Docker

```bash
docker network create \
  --driver=bridge \
  --subnet=192.168.32.0/16 \
  --ip-range=192.168.32.0/24 \
  --gateway=192.168.32.1 mindsetcloud-nt
```

#### Example of Custom Network:

```bash
docker network create \
  --subnet=10.10.1.0/24 \
  --ip-range=10.10.1.128/25 \
  --gateway=10.10.1.129 my_custom_network

# Verify the created network:
docker network inspect my_custom_network

# Run a container with a fixed IP:
docker run -d --name my_container \
  --net my_custom_network \
  --ip 10.10.1.130 image_name
```

Reference: [Docker Labs - Macvlan](https://dockerlabs.collabnix.com/beginners/macvlan-010.html)

---

## Running Docker on WSL

### WSL Installation and Setup

```bash
wsl --install
wsl --set-default-version 2
wsl --list --verbose
wsl --unregister <DistributionName>
wsl --list --online
wsl --install <DistributionName>
```

### Network Configuration in Windows

```bash
netsh interface ipv4 set address name="Ethernet" static 192.168.1.10 255.255.255.0 192.168.1.1
netsh interface ipv4 set dnsservers name="Ethernet" static 8.8.8.8 primary
netsh interface ipv4 add dnsservers name="Ethernet" 8.8.4.4 index=2
netsh interface portproxy add v4tov4 listenport=port listenaddress=0.0.0.0 connectport=port connectaddress=wsl_ip
```

---

## Service Permissions on Linux

Add the following lines to the `/etc/sudoers` file or use `visudo`:

```bash
username ALL=NOPASSWD: /usr/sbin/service ssh start
username ALL=NOPASSWD: /usr/sbin/service docker start
```

---

### Configuration in `~/.bashrc`

Add the following commands to the profile file:

```bash
vim ~/.bashrc
sudo service ssh start
sudo service docker start
```

---

## Contributing

Contributions are welcome! Follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

This project is licensed under the [MIT License](LICENSE).
