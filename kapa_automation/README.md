# **KAPA Automation – ETL Pipeline for Capacity Planning**  
🚀 **Automated Data Processing & Power BI Integration for KATEK SCM Analytics**  

---

## **📌 Project Overview**  
The **KAPA Automation** pipeline is designed to automate the **Capacity Planning** workflow by extracting, transforming, and loading (ETL) data from KATEK’s internal systems. The ETL scripts process **planned vs. actual capacity data, workforce utilization, and KPI computation**, ensuring **daily data availability with real-time Power BI visualization**.

💡 **Key Features**:
- ✅ **Automated Data Extraction** → Fetches structured data from **SharePoint Online & internal network directories**.
- ✅ **ETL Processing in Docker** → Standardizes, cleans, and formats raw data for analysis.
- ✅ **Task Scheduler Automation** → Windows Task Scheduler triggers ETL execution via batch script.
- ✅ **Power BI Dashboard Integration** → Ensures **daily refreshed capacity reports** using **Power BI Data Gateway**.
- ✅ **Version Control & Retention Policy** → Stores processed data in **SharePoint** with history tracking.

---

## **📂 Repository Structure**
This repository contains all scripts and configurations required for the ETL pipeline.

```
📦 kapa_automation
 ┣ 📂 calculations
 ┃ ┣ 📜 abweichung.py
 ┃ ┣ 📜 mitarbeiterbedarf_brutto.py
 ┃ ┣ 📜 utilization.py
 ┃ ┗ 📜 wartung.py
 ┣ 📂 data_processing
 ┃ ┣ 📜 extract_tables.py
 ┃ ┣ 📜 unpivoted_tables.py
 ┃ ┗ 📜 append_to_master.py
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
- **`main.py`** → Main ETL script that orchestrates the full data pipeline.
- **`Dockerfile`** → Defines the execution environment for ETL processing.
- **`run_docker.bat`** → Batch script used to trigger the pipeline via **Windows Task Scheduler**.
- **`config.yaml`** → Configuration file storing input paths, processing rules, and logging settings.
- **`logs/`** → Stores execution logs for debugging and monitoring.
- **`output/`** → Contains transformed and structured data ready for Power BI.

---

## **🔄 Automation Workflow**
This pipeline automates the **Capacity Planning** data flow through **Dockerized ETL execution** and **Windows Task Scheduler automation**.

### **1️⃣ Data Extraction**
- Fetches raw files from **SharePoint & secured network paths**.
- Uses **Python (pandas, requests, openpyxl)** to extract and structure data.
- **Error handling & retry mechanism** ensures reliable execution.

### **2️⃣ Data Transformation**
- Cleans and formats extracted datasets:
  - **Removes duplicates & handles missing values**.
  - **Unpivots tables** to standardize structure.
  - **Calculates KPIs** such as **Machine Utilization Rate & Workforce Efficiency**.
- Stores processed data in **SharePoint Online**.

### **3️⃣ Dockerized Deployment & Execution**
- The pipeline runs inside a **Docker container** for **consistent execution** across different environments.
- **Built with**: `Docker`, `Python 3.13`, `pip`, `pandas`, `openpyxl`.

### **4️⃣ Task Scheduler Integration**
- **Windows Task Scheduler** executes the ETL pipeline at **11:00 PM daily**.
- Triggers the **`run_docker.bat`** script, which starts the Docker container.

### **5️⃣ Power BI Data Refresh**
- Processed data is **automatically refreshed in Power BI** using:
  - **Power BI Data Gateway** for scheduled refresh.
  - **Power Automate** for real-time updates when data is modified.

---

## **🛠 Deployment & Installation Guide**
### **📌 Prerequisites**
Before running the KAPA ETL pipeline, ensure the following dependencies are installed:

- **Docker** → [Install Docker](https://www.docker.com/get-started)
- **Python 3.13** with required dependencies (`pip install -r requirements.txt`)
- **Windows Task Scheduler** for automation.

### **📌 Step-by-Step Deployment**
#### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/kapa_automation.git
cd kapa_automation
```

#### **2️⃣ Build & Run Docker Container**
```sh
docker build -t kapa-automation-app .
docker run --rm -it -v "$(pwd):/main" kapa-automation-app
```

#### **3️⃣ Schedule Task in Windows Task Scheduler**
- Open **Task Scheduler** → Create a New Task.
- **Trigger:** Set execution frequency (daily at 11:00 PM).
- **Action:** Run the `run_docker.bat` file.

---

## **📊 Results & Impact**
✅ **Time Saved**:
- **Before Automation**: ~5 hours per report (manual data entry + Excel processing).
- **After Automation**: ~5-10 minutes (automated ETL + Power BI refresh).

✅ **Accuracy Improvement**:
- Eliminates human errors from **manual Excel-based calculations**.
- Provides **real-time, rounded KPI values** directly in Power BI.

✅ **Operational Efficiency**:
- Managers now focus on **insights & decision-making** instead of manual reporting.
- **Daily updated data** provides more visibility into capacity planning.

---

## **🚀 Future Enhancements**
To further improve automation, we plan the following enhancements:

| **Enhancement** | **Expected Benefit** |
|---------------|---------------------|
| **Microsoft Fabric / Azure Data Factory** | Real-time streaming & automated Power BI refresh |
| **Serverless Execution (AWS Lambda, Azure Functions)** | Fully automated ETL with auto-scaling |
| **Performance Optimization** | Reduce processing time from **5 minutes → 2 minutes** |

📌 **Planned Upgrade**: Move from Windows Task Scheduler → **Cloud-Based Orchestration (Apache Airflow / Azure Logic Apps).**

---

## **👨‍💻 Contributing**
Contributions are welcome! If you’d like to improve the ETL scripts or Power BI dashboards:
1. **Fork the repository**.
2. **Create a new branch**.
3. **Submit a pull request**.

---

## **📞 Support & Contact**
If you need support or have questions about deployment:
📩 **Email**:  sadathali-khan.patan@katek-group.com
🌐 **GitHub Issues**: [Open an Issue](https://github.com/your-username/kapa_automation/issues)  

---

### **📜 License**
This project is licensed under the **MIT License** – feel free to modify and distribute.

---

🚀 **Automate & Optimize Capacity Planning!** 🎯
