# Aircraft Recognition service

## AI project

### Recognition model

Satellite Images were collected on GoogleEarth Pro at various time and locations

The dataset was created on Roboflow and is publicly available at: https://universe.roboflow.com/pvaircraftreco/aircraft-reco-1/dataset/2

The dataset was annotated on Roboflow using [bounding boxes](https://docs.roboflow.com/annotate/annotation-tools#bounding-boxes-vs.-polygons).

The model was subsequently trained using YOLOv11 object detection (Fast).

### Attributes

Annotation was done "on the fly". Types were created based on the most recognizable types of aircraft.
But it lacks consistency at this stage.

We tried to identify different types of aircraft:

- multirole: Su-27/30/34, Mig-29/35 and variants
- bomber: mainly Tu-22M3 at this point, more thorough examination is needed regarding Tu-160
- tu-95: very recognizable as such so an "ad hoc" type was created for the Bear
- trainer: straight wing aircrafts
- unknown swept wing: probably SU-24M
- transport: multi-engine aircrafts
- SU-57: need more examination but an "ad hoc" type was created for the Felon
- helo: Mi-8, Ka-50
- civilian

### Performance

More on that later...
https://blog.roboflow.com/mean-average-precision

![image](https://github.com/user-attachments/assets/206ae31a-35e0-4d5f-864a-38fd4e4772f5)

![image](https://github.com/user-attachments/assets/accb3471-1858-4cfc-9ef5-9d70749d3c11)

# Backend Project

This API provides endpoints for managing and analyzing geographic observations. It integrates with **Roboflow** to analyze aircraft data and stores observations in a PostgreSQL database using SQLAlchemy.

Install the dependencies

```
pip install -r requirements.txt

```

Activate virtual env

```
source my_env/bin/activate

```

Start the Server

```
python app.py

```

## Base URL

```
http://localhost:5000
```

## Endpoints

### 1. Add a New Observation

#### **POST** `/observation`

**Description:**

- Submits a new observation, triggers an external analysis via **Roboflow**, and saves the result.

**Request Body (JSON):**

```json
{
  "geo_id": 1,
  "date": "2024-02-17",
  "asset_url": "https://example.com/asset.jpg",
  "external_url": "https://example.com/info"
}
```

**Response:**

- **201 Created**
  ```json
  {
    "message": "Observation added successfully",
    "id": 123
  }
  ```
- **400 Bad Request** (If required fields are missing)
  ```json
  {
    "error": "Missing required fields"
  }
  ```
- **500 Internal Server Error** (If analysis fails)
  ```json
  {
    "error": "Failed to fetch analysis"
  }
  ```

---

### 2. Get All Geos

#### **GET** `/geos`

**Description:**

- Retrieves all geographic locations stored in the database.

**Response:**

- **200 OK**
  ```json
  [
    { "id": 1, "name": "Location A", "created_at": "2024-01-01T12:00:00" },
    { "id": 2, "name": "Location B", "created_at": "2024-01-02T15:30:00" }
  ]
  ```

---

### 3. Get Geos (Deprecated Method)

#### **GET** `/geos_old`

**Description:**

- Retrieves geographic locations using a raw SQL query (deprecated in favor of SQLAlchemy).

**Response:**

- **200 OK**
  ```json
  [
    { "id": 1, "name": "Location A", "created_at": "2024-01-01T12:00:00" },
    { "id": 2, "name": "Location B", "created_at": "2024-01-02T15:30:00" }
  ]
  ```
- **500 Internal Server Error** (If database connection fails)
  ```json
  {
    "error": "Database connection failed"
  }
  ```

---

## Notes

- The `/observation` endpoint uses **Roboflow** to analyze aircraft images.
- The `/geos_old` endpoint is **deprecated** and will be removed in future versions.

## Running the API

To run the Flask app locally:

```sh
export FLASK_APP=app.py
flask run
```

Ensure you have the required dependencies installed:

```sh
pip install -r requirements.txt
```

## Environment Variables

- `SQLALCHEMY_DATABASE_URI`: PostgreSQL connection string
- `ROBOFLOW_APIKEY`: API key for Roboflow integration
