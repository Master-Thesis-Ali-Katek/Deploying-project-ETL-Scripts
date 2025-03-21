# **Deploying Project ETL Scripts**  
🚀 **Automated ETL Pipelines & Power BI Integration for KATEK SCM Analytics**  

---

## **📌 Project Overview**  
This project automates the extraction, transformation, and loading (ETL) of **supply chain data** for **KATEK SCM Analytics**. The ETL pipelines process production capacity, backlog, and PB & SMT production hours, ensuring **real-time data availability, accuracy, and efficiency**.  

💡 **Key Features**:
- ✅ **Automated Data Extraction** → Fetches raw data from internal SharePoint and network directories.
- ✅ **ETL Pipeline Deployment** → Structured and formatted data processing in **Docker containers**.
- ✅ **Scheduled Execution** → Task Scheduler triggers Docker-based ETL scripts at predefined intervals.
- ✅ **Real-Time Power BI Dashboards** → Live data updates using **Power BI Data Gateway** and **Power Automate**.
- ✅ **Data Storage & Retention** → Processed data is stored in **SharePoint Online** with version control.

---

## **📂 Repository Structure**
This repository contains all the necessary ETL scripts, configurations, and deployment files.

```
📦 Master-Thesis-Ali-Katek
 ┣ 📂 kapa_automation
 ┃ ┣ 📂 data_processing
 ┃ ┃ ┣ 📜 extract_tables.py
 ┃ ┃ ┣ 📜 unpivoted_tables.py
 ┃ ┃ ┗ 📜 append_to_master.py
 ┃ ┣ 📂 calculations
 ┃ ┃ ┣ 📜 utilization.py
 ┃ ┃ ┣ 📜 wartung.py
 ┃ ┃ ┗ 📜 abweichung.py
 ┃ ┣ 📜 main.py
 ┃ ┣ 📜 requirements.txt
 ┃ ┣ 📜 Dockerfile
 ┃ ┗ 📜 run_docker.bat
 ┣ 📂 pb_smt_automation
 ┃ ┣ 📜 data_extraction.py
 ┃ ┣ 📜 data_processing.py
 ┃ ┗ 📜 append.py
 ┣ 📂 production_backlog_automation
 ┃ ┣ 📜 clean_rename.py
 ┃ ┣ 📜 data_unpivoting.py
 ┃ ┗ 📜 extraction.py
 ┣ 📜 .gitattributes
 ┣ 📜 README.md
 ┣ 📜 task_internal.pbix  (Power BI Dashboard)
```

📌 **Key Components**:
- **`main.py`** → Main script that orchestrates the entire ETL process.
- **`Dockerfile`** → Defines the container environment for execution.
- **`run_docker.bat`** → Batch script for triggering the ETL pipeline via Windows Task Scheduler.
- **`task_internal.pbix`** → Power BI dashboard for real-time reporting.

---

## **🔄 Automation Workflow**
This ETL pipeline automates data processing through **a combination of Docker and Windows Task Scheduler**.

### **1️⃣ Data Extraction**
- Extracts raw files from **SharePoint and internal network storage**.
- Uses **Python scripts (pandas, openpyxl, requests)** to fetch and structure data.
- Handles **file identification, error logging, and retries**.

### **2️⃣ Data Transformation (ETL)**
- Cleans and formats raw datasets (**removes duplicates, normalizes values**).
- Unpivots tables and **calculates KPIs** (e.g., **Machine Utilization Rate, Workforce Efficiency**).
- Saves transformed data to **SharePoint Online**.

### **3️⃣ Deployment & Execution**
- **Dockerized ETL Pipelines**:
  - Python scripts are **containerized** for consistent execution across environments.
  - **Built with**: `Docker`, `Python 3.13`, `pip`, `pandas`, `openpyxl`.
- **Task Scheduler Integration**:
  - Windows Task Scheduler **automates execution** of ETL pipelines.
  - Triggers a **batch script (`run_docker.bat`)** to execute Docker containers.

### **4️⃣ Power BI Integration**
- **Data Gateway + Power Automate** ensures real-time dashboard updates.
- Power BI automatically fetches data from **SharePoint Online**.
- Visualizes **daily workforce utilization, backlog trends, and PB & SMT production hours**.

---

## **🛠 Deployment & Installation Guide**
### **📌 Prerequisites**
Before running the ETL pipeline, ensure you have:
- **Docker** installed → [Install Docker](https://www.docker.com/get-started)
- **Python 3.13** with required dependencies (`pip install -r requirements.txt`)
- **Windows Task Scheduler** for automation.

### **📌 Step-by-Step Deployment**
#### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/Master-Thesis-Ali-Katek.git
cd Master-Thesis-Ali-Katek
```

#### **2️⃣ Build & Run Docker Container**
```sh
docker build -t kapa-automation-app .
docker run --rm -it -v "$(pwd):/main" kapa-automation-app
```

#### **3️⃣ Schedule Task in Windows Task Scheduler**
- Open **Task Scheduler** → Create a New Task.
- **Trigger:** Set execution frequency (daily/weekly).
- **Action:** Run the `run_docker.bat` file.

---

## **📊 Results & Impact**
✅ **Time Saved**:
- **Manual Processing**: ~5 hours per report.
- **Automated Processing**: ~5-10 minutes.

✅ **Accuracy Improvement**:
- Eliminates human errors from **manual Excel-based calculations**.
- Provides **real-time, rounded KPI values** directly in Power BI.

✅ **Usability & Efficiency**:
- Allows **Supply Chain Managers** to focus on insights rather than manual reporting.
- Provides **daily data availability** instead of monthly manual entry.

---

## **🚀 Future Enhancements**
We plan to further optimize automation by integrating:
| **Enhancement** | **Expected Benefit** |
|---------------|---------------------|
| **Real-time Data Streaming** (Microsoft Fabric/Azure Data Factory) | Live updates without scheduled refresh |
| **Serverless Execution** (AWS Lambda, Azure Functions) | Cost-effective, on-demand ETL processing |
| **Optimized Python Scripts** | Reduce ETL processing time from **5 minutes to 2 minutes** |

📌 **Planned Upgrade**: Move from Windows Task Scheduler → **Fully Cloud-Based Orchestration (Azure Logic Apps / Apache Airflow).**

---

## **👨‍💻 Contributing**
Contributions are welcome! If you’d like to improve the ETL scripts or Power BI dashboards:
1. **Fork the repository**.
2. **Create a new branch**.
3. **Submit a pull request**.

---

## **📞 Support & Contact**
If you need support or have questions about deployment:
📩 **Email**: sadathali-khan.patan@katek-group.com
🌐 **GitHub Issues**: [Open an Issue](https://github.com/your-username/Master-Thesis-Ali-Katek/issues)  

---


---

🚀 **Happy Automating!** 🎯
