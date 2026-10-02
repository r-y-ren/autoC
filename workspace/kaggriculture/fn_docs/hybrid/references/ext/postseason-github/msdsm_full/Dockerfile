FROM rust:1.88-bookworm AS rust-toolchain

FROM python:3.12-bookworm
COPY --from=rust-toolchain /usr/local/cargo /usr/local/cargo
COPY --from=rust-toolchain /usr/local/rustup /usr/local/rustup
ENV PATH="/usr/local/cargo/bin:${PATH}" \
    RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PYTHONUNBUFFERED=1 \
    XLA_PYTHON_CLIENT_PREALLOCATE=false
WORKDIR /opt/kaggriculture
COPY . .
ARG PYTHON_EXTRAS=gpu,data
RUN python -m pip install --no-cache-dir -e ".[${PYTHON_EXTRAS}]" ./native/engine
RUN python scripts/build_search.py
CMD ["python", "scripts/train_ppo.py", "--help"]
