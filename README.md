# Salary Tracking

The goal of this project is to capture salary receipt data from PDFs and store it in a database. The stored data is then
processed to provide metrics and identify any errors that may be present.

## Installation

1. Clone the repository: `git clone https://github.com/MarcoCaizzi/salaryTracking.git`
2. Install the required dependencies: `pip install -r requirements.txt`

## Usage

1. Place the salary receipts in the `pdfs` directory
2. Run the `main.py` script: `python main.py`
3. The processed data will be stored in the database

## Database Schema

The `database.db` database has the following schema:

### Table: `months_years_loaded`

| Column Name | Data Type | Description                             |
|-------------|-----------|-----------------------------------------|
| `id`        | INTEGER   | Primary key                             |
| month	      | TEXT	     | The month of the year (e.g., "January") |
| year	       | TEXT      | 	The year (e.g., "2023")                |

Column Type Description
id INTEGER Unique identifier for the row
month TEXT The month of the year (e.g., "January")
year TEXT The year (e.g., "2023")

### Table: `salary`

| Column Name                | Data Type | Description                             |
|----------------------------|-----------|-----------------------------------------|
| `id`                       | INTEGER   | Primary key                             |
| `id_month_year`            | INTEGER   | Foreign key to `months_years_loaded.id` |
| `codigo`                   | INTEGER   | Code of the salary concept              |
| `descripcion_del_concepto` | TEXT      | Description of the salary concept       |
| `unidad`                   | INTEGER   | Number of units                         |
| `haberes_con_aporte`       | REAL      | Income with contribution                |
| `haberes_sin_aporte`       | REAL      | Income without contribution             |
| `descuentos`               | REAL      | Discounts                               |

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

