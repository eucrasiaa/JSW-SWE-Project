use axum::{
    extract::State,
    response::Html,
    response::sse::Event,
    response::Sse,
    routing::{get, post},
    Json, Router,
};



#[tokio::main]
async fn main() {
    // build our application with a single route
    // let app = Router::new().route("/", get(|| async { "Hello, World!" }));
    let app = Router::new()
        .route("/", get(root))
        .route("/foo", get(get_foo).post(post_foo))
        .route("/foo/bar", get(foo_bar));
    // run our app with hyper, listening globally on port 3000
    let listener = tokio::net::TcpListener::bind("0.0.0.0:4413").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn root() -> Html<&'static str> {
    Html(include_str!("../htmls/index.html"))
}
async fn get_foo() {}
async fn post_foo() {}
async fn foo_bar() {}



