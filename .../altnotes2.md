1) normalize json array cause dupe data is evillll


parsed JSON sent with web
{
  "Tutor": "Name", <- from prefName
  "Day": "DayOfWeek", <- from schedule
  "Start Time": "13:00", <- from schedule 
  "End Time": "16:00", <- from schedule
  "Courses": \["BIOL 101", "BIOL 102", "CHEM 101"\],
  "Status": "Checked-In",
}

Tutor (
id fName lName perfName
)


```js
const toMinutes = (time) => {
  const [hours, minutes] = time.split(':').map(Number);
  return hours * 60 + minutes;
};

let tutorScheduleMap = new Map();

dataJson.forEach(session => {
  if (!tutorScheduleMap.has(session.Tutor)) {
    tutorScheduleMap.set(session.Tutor, []);
  }
  tutorScheduleMap.get(session.Tutor).push(session);
});


tutorScheduleMap.forEach(session => {
    session.forEach(shift => {
        console.log(shift);
    });
});



let tutorScheduleMap = new Map();

dataJson.forEach(session => {
  if (!tutorScheduleMap.has(session.Tutor)) {
    tutorScheduleMap.set(session.Tutor, []);
  }
  tutorScheduleMap.get(session.Tutor).push(session);
});
let tutorScheduleMapOther = new Map();
tutorScheduleMap.forEach(session => {
    
    session.forEach(shift => {
        if(!tutorScheduleMapOther.has(shift.Tutor+"^^"+shift.Day+"^^"+shift.StartTime)){
            tutorScheduleMapOther.set(shift.Tutor+"^^"+shift.Day+"^^"+shift.StartTime, []);
        }
        tutorScheduleMapOther.get(shift.Tutor+"^^"+shift.Day+"^^"+shift.StartTime).push(shift.Course)
        // console.log(shift);
    });
});



function prettyPrintMap(map) {
  console.log("%c Schedule Overview", "font-weight: bold; font-size: 14px; color: #2196F3;");
  console.log("------------------------------------------------------------");

  map.forEach((courses, key) => {
    // Split the key into Name, Day, and Time
    const [name, day, time] = key.split("^^");

    console.log(`%c ${name.padEnd(10)} |  ${day.padEnd(10)} |  ${time}`, "font-weight: bold; color: #4CAF50;");
    console.log(`   Courses: ${courses.join(", ")}`);
    console.log("------------------------------------------------------------");
  });
}




function organizeByTutor(map) {
  const tutorData = {};

  map.forEach((courses, key) => {
    const [name, day, times,timee] = key.split("^^");
    if (!tutorData[name]) {
      tutorData[name] = {
        "Tutor": name,
        "Schedule": []
      };
    }
    tutorData[name].Schedule.push({
      "Day": day,
      "StartTime": times,
      "EndTime": timee, 
      "Courses": courses 
    });
  });
  return JSON.stringify(Object.values(tutorData), null, 2);
}

const tutorJson = organizeByTutor(tutorScheduleMapOther);
console.log(tutorJson);

```

axum for rust base
sqlx
askama for templating?
serde

maybe server-send events?
JS EventSource
tokio::sync::broadcast

axum::Router:  for handlers! 
axum::extract::State: The extractor used to inject your database connection pool and your SSE broadcast channel into your route handlers so they can be accessed safely across multiple threads.
axum::response::sse::Event: The structure representing a single Server-Sent Event message (e.g., a JSON payload containing Zoya's status update).
axum::response::Sse: The return type for the route that students connect to when they want to listen for live updates.

tokio::sync::broadcast::channel: The function that creates your live-update pipeline. You create this once when the server starts.

tokio::sync::broadcast::Sender: The structure your admin panel will use to push a message into the channel.

tokio::sync::broadcast::Receiver: The structure created for every student that loads the page, listening for messages from the Sender.

sqlx::SqlitePool: The structure managing concurrent connections to your schedule.db file.

sqlx::query! / sqlx::query_as!: The core macros for executing SQL. These are special because they check your SQL syntax against your actual SQLite database at compile time.

sqlx::FromRow: A trait you derive on your Rust structs (e.g., struct Shift) so SQLx can automatically map a database row directly into a Rust object.

askama::Template: The primary trait you derive on a struct to link it to an HTML file (like your base calendar). When you instantiate the struct and call .render(), it generates the raw HTML string blazingly fast.
serde::Serialize / serde::Deserialize: Traits you derive on your data structures so they can be automatically converted back and forth between Rust objects and JSON (critical for your live-update payloads).


calendar_app/
├── Cargo.toml             # Your Rust dependencies
├── Dockerfile             # The multi-stage build file I provided earlier
├── docker-compose.yml     # Your Docker Compose setup
├── .dockerignore          # CRITICAL: Prevents copying huge local build files
├── .env                   # Local environment variables (DATABASE_URL=...)
├── data/                  # Local folder for SQLite (mounted to Docker)
│   └── schedule.db        # Your actual SQLite file
├── assets/                # Static files (CSS, JS, Images) served by Axum
│   ├── style.css
│   └── sse_client.js      # Your frontend logic for receiving live updates
├── templates/             # Askama HTML templates
│   ├── base.html
│   └── index.html         # The master schedule template
└── src/                   # Your Rust code!
    ├── main.rs            # Axum server setup and routing
    ├── db.rs              # SQLx database queries
    ├── models.rs          # Structs defining your Schedule/LiveStatus JSON
    └── admin.rs           # Admin panel logic








use sqlx::{sqlite::SqlitePoolOptions, SqlitePool};
use std::sync::Arc;
use serde::{Deserialize, Serialize};
use sqlx::FromRow;

// This represents a row in the 'shifts' table
#[derive(Debug, Serialize, Deserialize, FromRow)]
pub struct ShiftRow {
    pub id: i64,
    pub tutor_name: String,
    pub day_of_week: String,
    pub start_time: String,
    pub end_time: String,
    pub status: String,
}

// This is the aggregated struct we actually send to the frontend/Askama
#[derive(Debug, Serialize, Deserialize)]
pub struct ShiftDisplay {
    pub id: i64,
    pub tutor_name: String,
    pub day_of_week: String,
    pub time_block: String, // e.g., "16:00 - 17:00"
    pub courses: Vec<String>,
    pub status: String,
}


// 1. Define your AppState
// We wrap it in an Arc (Atomic Reference Counted pointer) so multiple 
// async requests can share the exact same database connection pool safely.
struct AppState {
    db: SqlitePool,
    // Note: This is where you will add your SSE broadcast sender later!
}

#[tokio::main]
async fn main() {
    // 2. Connect to SQLite
    // It looks for the DATABASE_URL environment variable (e.g., sqlite:///app/data/schedule.db)
    let db_url = std::env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    
    let pool = SqlitePoolOptions::new()
        .max_connections(5)
        .connect(&db_url)
        .await
        .expect("Failed to connect to SQLite");

    // 3. Create the shared state
    let shared_state = Arc::new(AppState { db: pool });

    // 4. Build the router and attach the state
    let app = Router::new()
        .route("/api/shifts", get(get_all_shifts))
        .route("/api/import", post(import_legacy_json))
        .with_state(shared_state); // Injecting the state here!

    let listener = tokio::net::TcpListener::bind("0.0.0.0:4413").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

// A route to fetch the schedule from SQLite and return it as JSON
async fn get_all_shifts(
    State(state): State<Arc<AppState>>,
) -> Json<Vec<ShiftDisplay>> {
    
    // 1. Query the core shifts using SQLx's compile-time checked macro
    let shifts = sqlx::query_as!(
        ShiftRow,
        "SELECT id, tutor_name, day_of_week, start_time, end_time, status FROM shifts"
    )
    .fetch_all(&state.db)
    .await
    .unwrap_or_default();

    let mut display_list = Vec::new();

    // 2. For each shift, fetch its associated courses
    for shift in shifts {
        // Query the linked courses
        let courses = sqlx::query_scalar!(
            "SELECT course_name FROM shift_courses WHERE shift_id = ?",
            shift.id
        )
        .fetch_all(&state.db)
        .await
        .unwrap_or_default();

        // 3. Assemble the final display object
        display_list.push(ShiftDisplay {
            id: shift.id,
            tutor_name: shift.tutor_name,
            day_of_week: shift.day_of_week,
            time_block: format!("{} - {}", shift.start_time, shift.end_time),
            courses,
            status: shift.status,
        });
    }

    // Axum automatically converts this Struct into an HTTP JSON Response
    Json(display_list)
}

