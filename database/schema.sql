CREATE TABLE instrument (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    exchange VARCHAR(20),
    instrument_type VARCHAR(20)
);

CREATE TABLE candle (
    id BIGSERIAL PRIMARY KEY,
    instrument_id INTEGER REFERENCES instrument(id),
    timeframe VARCHAR(10) NOT NULL,
    candle_time TIMESTAMP NOT NULL,

    open NUMERIC(12,2),
    high NUMERIC(12,2),
    low NUMERIC(12,2),
    close NUMERIC(12,2),

    volume BIGINT,

    UNIQUE(instrument_id, timeframe, candle_time)
);