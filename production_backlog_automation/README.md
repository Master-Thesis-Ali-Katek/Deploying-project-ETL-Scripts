# **Production Backlog Automation – ETL Pipeline**  
🚀 **Automated ETL Processing for Production Backlog & Power BI Integration**  

---

## **📌 Project Overview**  
The **Production Backlog Automation** pipeline is designed to optimize **backlog tracking** for KATEK’s supply chain by automating the extraction, processing, and visualization of backlog data. The pipeline ensures **real-time reporting in Power BI**, enabling better resource planning and backlog management.

💡 **Key Features**:
- ✅ **Automated Data Extraction** → Retrieves backlog data from **network drives & SharePoint**.
- ✅ **ETL Processing in Docker** → Cleans, transforms, and structures backlog data.
- ✅ **Windows Task Scheduler Automation** → Ensures fully automated execution via batch script.
- ✅ **Power BI Data Gateway Integration** → Enables **daily refreshed backlog reports**.
- ✅ **Version Control & Data Retention** → Stores structured data in **SharePoint** with history tracking.

---

## **📂 Repository Structure**
This repository contains all necessary scripts and configurations for **Production Backlog Automation**.

```
📦 production_backlog_automation
 ┣ 📂 backlog_operations
 ┃ ┣ 📜 data_extraction.py
 ┃ ┣ 📜 clean_rename.py
 ┃ ┣ 📜 data_unpivoting.py
 ┃ ┣ 📜 append.py
 ┣ 📂 config
 ┃ ┗ 📜 config.yaml
 ┣ 📂 logs
 ┣ 📂 output
 ┣ 📜 main.py
 ┣ 📜 requirements.txt
 ┣ 📜 Dockerfile
 ┣ 📜 run_docker.bat
 ┗ 📜 README.md
```

📌 **Key Components**:
- **`main.py`** → The main ETL script that processes production backlog data.
- **`Dockerfile`** → Defines the execution environment inside a Docker container.
- **`run_docker.bat`** → Batch script used to trigger the pipeline via **Windows Task Scheduler**.
- **`config.yaml`** → Configuration file for file paths, logging, and scheduling.
- **`logs/`** → Stores execution logs for debugging and monitoring.
- **`output/`** → Contains processed backlog data for Power BI.

---

## **🔄 Automation Workflow**
The **Production Backlog Automation** pipeline follows an **ETL (Extract, Transform, Load) process** to provide **real-time backlog monitoring**.

### **1️⃣ Data Extraction**
- Extracts raw backlog data from **SharePoint & secured network directories**.
- Uses **Python (pandas, requests, openpyxl)** for structured extraction.
- **Handles missing files, errors, and retry mechanisms**.

### **2️⃣ Data Transformation**
- Cleans and formats extracted datasets:
  - **Standardizes column names & formats.**
  - **Removes duplicate backlog entries.**
  - **Segments backlog data by product line & delay impact.**
- Computes backlog KPIs, including:
  - **Backlog Clearance Rate**
  - **Order Delay Impact**
  - **Resource Utilization Efficiency**
- Saves processed data in **SharePoint for Power BI dashboards**.

### **3️⃣ Dockerized Deployment & Execution**
- The pipeline runs inside a **Docker container** for **scalability & consistency**.
- **Built with**: `Docker`, `Python 3.13`, `pandas`, `numpy`, `openpyxl`.

### **4️⃣ Task Scheduler Integration**
- **Windows Task Scheduler** triggers the ETL pipeline **every Monday at 11:00 PM**.
- Executes the **`run_docker.bat`** script, starting the Docker container.

### **5️⃣ Power BI Data Refresh**
- Processed data is **automatically refreshed in Power BI** using:
  - **Power BI Data Gateway** for scheduled refresh.
  - **Power Automate** to trigger real-time updates when new data is added.

---

## **🛠 Deployment & Installation Guide**
### **📌 Prerequisites**
Before running the **Production Backlog Automation** pipeline, ensure you have:

- **Docker** → [Install Docker](https://www.docker.com/get-started)
- **Python 3.13** with required dependencies (`pip install -r requirements.txt`)
- **Windows Task Scheduler** for automation.

### **📌 Step-by-Step Deployment**
#### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/production_backlog_automation.git
cd production_backlog_automation
```

#### **2️⃣ Build & Run Docker Container**
```sh
docker build -t backlog-automation .
docker run --rm -it -v "$(pwd):/main" backlog-automation
```

#### **3️⃣ Schedule Task in Windows Task Scheduler**
- Open **Task Scheduler** → Create a New Task.
- **Trigger:** Set execution frequency (weekly, Monday at 11:00 PM).
- **Action:** Run the `run_docker.bat` file.

---

## **📊 Results & Impact**
✅ **Time Saved**:
- **Before Automation**: ~5 hours per week (manual backlog updates + Excel reporting).
- **After Automation**: ~5-10 minutes (fully automated backlog processing).

✅ **Accuracy Improvement**:
- **Eliminates manual calculation errors.**
- **Ensures real-time backlog monitoring & forecasting.**

✅ **Operational Efficiency**:
- Provides real-time backlog clearance tracking.
- Helps in **identifying production bottlenecks & optimizing resource allocation**.

---

## **🚀 Future Enhancements**
To further improve automation, the following enhancements are planned:

| **Enhancement** | **Expected Benefit** |
|---------------|---------------------|
| **Microsoft Fabric / Azure Data Factory** | Real-time data streaming & automated refresh |
| **Serverless Execution (AWS Lambda, Azure Functions)** | Fully automated, event-driven ETL processing |
| **Performance Optimization** | Reduce processing time from **5 minutes → 2 minutes** |

📌 **Planned Upgrade**: Move from Windows Task Scheduler → **Cloud-Based Orchestration (Apache Airflow / Azure Logic Apps).**

---

## **👨‍💻 Contributing**
Contributions are welcome! If you'd like to enhance the ETL scripts or improve dashboard integration:
1. **Fork the repository**.
2. **Create a new branch**.
3. **Submit a pull request**.

---

## **📞 Support & Contact**
For any inquiries or support:
📩 **Email**: sadathali-khan.patan@katek-group.com 
🌐 **GitHub Issues**: [Open an Issue](https://github.com/your-username/production_backlog_automation/issues)  

---



---

🚀 **Automate & Optimize Production Backlog Tracking!** 🎯
