FROM rust:1.80 as builder

WORKDIR /usr/src/rust_engine

# Install nightly Rust
RUN rustup install nightly && rustup default nightly

COPY rust_engine/Cargo.toml .
COPY rust_engine/src ./src

# Build the Rust project in release mode
RUN cargo build --release

# Final minimal image
FROM debian:bullseye-slim

WORKDIR /app
COPY --from=builder /usr/src/rust_engine/target/release/rust_engine .

CMD ["./rust_engine"]
