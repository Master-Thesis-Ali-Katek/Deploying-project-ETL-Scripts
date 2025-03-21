# **PB & SMT Production Hours Automation – ETL Pipeline**  
🚀 **Automated ETL for Production Hours & Power BI Integration**  

---

## **📌 Project Overview**  
The **PB & SMT Production Hours Automation** pipeline is designed to streamline **production hours tracking** for **Printed Board (PB) and Surface Mount Technology (SMT)** operations at KATEK. The pipeline extracts, processes, and loads production data into **SharePoint**, enabling real-time **Power BI dashboards** for analysis.

💡 **Key Features**:
- ✅ **Automated Data Extraction** → Retrieves production hour records from **network drives & SharePoint**.
- ✅ **ETL Processing in Docker** → Cleans, transforms, and normalizes raw data for structured reporting.
- ✅ **Windows Task Scheduler Automation** → Automates execution using a batch script.
- ✅ **Power BI Data Gateway Integration** → Ensures **daily refreshed production reports**.
- ✅ **Version Control & Data Retention** → Stores structured data in **SharePoint** with history tracking.

---

## **📂 Repository Structure**
This repository contains all scripts and configurations required for the **PB & SMT Production Hours** ETL pipeline.

```
📦 pb_smt_automation
 ┣ 📂 pb_operations
 ┃ ┣ 📜 data_extraction.py
 ┃ ┣ 📜 clean_rename.py
 ┃ ┣ 📜 data_unpivoting.py
 ┃ ┣ 📜 append.py
 ┃ ┗ 📜 seperating_first_line.py
 ┣ 📂 smt_operations
 ┃ ┣ 📜 extraction.py
 ┃ ┣ 📜 clean_rename.py
 ┃ ┣ 📜 data_unpivoting.py
 ┃ ┣ 📜 append.py
 ┣ 📂 smt_load_operations
 ┃ ┣ 📜 extraction.py
 ┃ ┣ 📜 clean_rename.py
 ┃ ┣ 📜 data_unpivoting.py
 ┃ ┣ 📜 data_exporting.py
 ┃ ┗ 📜 append.py
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
- **`main.py`** → The core ETL script that orchestrates production data extraction, transformation, and loading.
- **`Dockerfile`** → Defines the execution environment for ETL processing inside a container.
- **`run_docker.bat`** → Batch script used to trigger the pipeline via **Windows Task Scheduler**.
- **`config.yaml`** → Configuration file storing input paths, logging settings, and scheduling configurations.
- **`logs/`** → Stores execution logs for monitoring and debugging.
- **`output/`** → Contains transformed datasets ready for Power BI visualization.

---

## **🔄 Automation Workflow**
This pipeline automates the **PB & SMT Production Hours** data flow through **Dockerized ETL execution** and **Windows Task Scheduler automation**.

### **1️⃣ Data Extraction**
- Extracts raw data from **SharePoint & secured network directories**.
- Uses **Python (pandas, requests, openpyxl)** for structured extraction.
- **Handles missing files, errors, and retry mechanisms**.

### **2️⃣ Data Transformation**
- Cleans and formats extracted datasets:
  - **Removes duplicates & standardizes columns**.
  - **Unpivots tables for structured time-series reporting**.
  - **Computes KPIs** such as **Machine Utilization Rate & Production Efficiency**.
- Saves processed data in **SharePoint for Power BI integration**.

### **3️⃣ Dockerized Deployment & Execution**
- The pipeline runs inside a **Docker container** for **scalability & consistency**.
- **Built with**: `Docker`, `Python 3.13`, `pandas`, `numpy`, `openpyxl`.

### **4️⃣ Task Scheduler Integration**
- **Windows Task Scheduler** triggers the ETL pipeline **daily at 10:30 PM**.
- Executes the **`run_docker.bat`** script, starting the Docker container.

### **5️⃣ Power BI Data Refresh**
- Processed data is **automatically refreshed in Power BI** using:
  - **Power BI Data Gateway** for scheduled refresh.
  - **Power Automate** to trigger real-time updates on file modifications.

---

## **🛠 Deployment & Installation Guide**
### **📌 Prerequisites**
Before running the **PB & SMT Production Hours** ETL pipeline, install the following dependencies:

- **Docker** → [Install Docker](https://www.docker.com/get-started)
- **Python 3.13** with required dependencies (`pip install -r requirements.txt`)
- **Windows Task Scheduler** for automation.

### **📌 Step-by-Step Deployment**
#### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/pb_smt_automation.git
cd pb_smt_automation
```

#### **2️⃣ Build & Run Docker Container**
```sh
docker build -t pb-smt-automation .
docker run --rm -it -v "$(pwd):/main" pb-smt-automation
```

#### **3️⃣ Schedule Task in Windows Task Scheduler**
- Open **Task Scheduler** → Create a New Task.
- **Trigger:** Set execution frequency (daily at 10:30 PM).
- **Action:** Run the `run_docker.bat` file.

---

## **📊 Results & Impact**
✅ **Time Saved**:
- **Before Automation**: ~3-5 hours per report (manual data entry + Excel calculations).
- **After Automation**: ~5-10 minutes (automated ETL + Power BI refresh).

✅ **Accuracy Improvement**:
- **Eliminates human errors** from manual data processing.
- **Ensures real-time KPI updates** in Power BI.

✅ **Operational Efficiency**:
- Enables managers to **focus on insights rather than manual data updates**.
- **Daily refreshed production hours** enhance decision-making.

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
If you need support or have questions about deployment:
📩 **Email**: sadathali-khan.patan@katek-group.com
🌐 **GitHub Issues**: [Open an Issue](https://github.com/your-username/pb_smt_automation/issues)  

---


---

🚀 **Automate & Optimize Production Hours Processing!** 🎯
