FROM rust:1.76-bookworm AS builder
WORKDIR /app

COPY . .

RUN cargo build --release

FROM debian:bookworm-slim
WORKDIR /app

RUN apt-get update && apt-get install -y sqlite3 ca-certificates && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/release/tutor_calendar .

COPY ./assets ./assets
COPY ./templates ./templates

EXPOSE 4413

CMD ["./tutor_calendar"]
